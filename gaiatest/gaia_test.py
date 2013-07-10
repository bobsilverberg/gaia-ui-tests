# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import base64
import json
import os
import sys
import time
import traceback

from marionette import MarionetteTestCase
from marionette import Marionette
from marionette import MarionetteTouchMixin
import mozdevice


class GaiaData(object):

    def __init__(self, marionette, testvars=None):
        self.marionette = marionette
        self.testvars = testvars or {}
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_data_layer.js"))
        self.marionette.import_script(js)
        self.marionette.set_search_timeout(10000)

    @property
    def is_carrier_connected(self):
        card_state = self.marionette.execute_script("return GaiaDataLayer.cardState()")
        print 'card_state: %s' % card_state
        return card_state == 'ready'


class GaiaDevice(object):

    def __init__(self, marionette):
        self.marionette = marionette

    @property
    def manager(self):
        if hasattr(self, '_manager') and self._manager:
            return self._manager

        if not self.is_android_build:
            raise Exception('Device manager is only available for devices.')

        dm_type = os.environ.get('DM_TRANS', 'adb')
        if dm_type == 'adb':
            self._manager = mozdevice.DeviceManagerADB()
        elif dm_type == 'sut':
            host = os.environ.get('TEST_DEVICE')
            if not host:
                raise Exception('Must specify host with SUT!')
            self._manager = mozdevice.DeviceManagerSUT(host=host)
        else:
            raise Exception('Unknown device manager type: %s' % dm_type)
        return self._manager

    @property
    def is_android_build(self):
        if not hasattr(self, '_is_android_build'):
            self._is_android_build = 'Android' in self.marionette.session_capabilities['platform']
        return self._is_android_build

    @property
    def has_mobile_connection(self):
        return self.marionette.execute_script('return window.navigator.mozMobileConnection !== undefined')

    @property
    def has_wifi(self):
        if not hasattr(self, '_has_wifi'):
            self._has_wifi = self.marionette.execute_script('return window.navigator.mozWifiManager !== undefined')
        return self._has_wifi

    def push_file(self, source, count=1, destination='', progress=None):
        if not destination.count('.') > 0:
            destination = '/'.join([destination, source.rpartition(os.path.sep)[-1]])
        self.manager.mkDirs(destination)
        self.manager.pushFile(source, destination)

        if count > 1:
            for i in range(1, count + 1):
                remote_copy = '_%s.'.join(iter(destination.split('.'))) % i
                self.manager._checkCmd(['shell', 'dd', 'if=%s' % destination, 'of=%s' % remote_copy])
                if progress:
                    progress.update(i)

            self.manager.removeFile(destination)

    def restart_b2g(self):
        self.stop_b2g()
        time.sleep(2)
        self.start_b2g()

    def start_b2g(self):
        if self.marionette.instance:
            # launch the gecko instance attached to marionette
            self.marionette.instance.start()
        elif self.is_android_build:
            self.manager.shellCheckOutput(['start', 'b2g'])
        else:
            raise Exception('Unable to start B2G')
        self.marionette.wait_for_port()
        self.marionette.start_session()
        if self.is_android_build:
            self.marionette.set_script_timeout(60000)
            self.marionette.execute_async_script("""
window.addEventListener('mozbrowserloadend', function loaded(aEvent) {
  if (aEvent.target.src.indexOf('ftu') != -1 || aEvent.target.src.indexOf('homescreen') != -1) {
    window.removeEventListener('mozbrowserloadend', loaded);
    marionetteScriptFinished();
  }
});""")

    def stop_b2g(self):
        if self.marionette.instance:
            # close the gecko instance attached to marionette
            self.marionette.instance.close()
        elif self.is_android_build:
            self.manager.shellCheckOutput(['stop', 'b2g'])
        else:
            raise Exception('Unable to stop B2G')
        self.marionette.client.close()
        self.marionette.session = None
        self.marionette.window = None


class GaiaTestCase(MarionetteTestCase):

    _script_timeout = 60000
    _search_timeout = 10000

    # deafult timeout in seconds for the wait_for methods
    _default_timeout = 30

    def __init__(self, *args, **kwargs):
        self.restart = kwargs.pop('restart', False)
        MarionetteTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        MarionetteTestCase.setUp(self)
        self.marionette.__class__ = type('Marionette', (Marionette, MarionetteTouchMixin), {})

        self.data_layer = GaiaData(self.marionette)
        self.device = GaiaDevice(self.marionette)
        if self.restart and (self.device.is_android_build or self.marionette.instance):
            self.device.stop_b2g()
            if self.device.is_android_build:
                # revert device to a clean state
                self.device.manager.removeDir('/data/local/indexedDB')
                self.device.manager.removeDir('/data/b2g/mozilla')
            self.device.start_b2g()

        self.marionette.setup_touch()

        # the emulator can be really slow!
        self.marionette.set_script_timeout(self._script_timeout)
        self.marionette.set_search_timeout(self._search_timeout)
        self.data_layer = GaiaData(self.marionette, self.testvars)

    def tearDown(self):
        if any(sys.exc_info()):
            # test has failed, gather debug
            test_class, test_name = self.marionette.test_name.split()[-1].split('.')
            xml_output = self.testvars.get('xml_output', None)
            debug_path = os.path.join(xml_output and os.path.dirname(xml_output) or 'debug', test_class)
            if not os.path.exists(debug_path):
                os.makedirs(debug_path)

            # screenshot
            try:
                with open(os.path.join(debug_path, '%s_screenshot.png' % test_name), 'w') as f:
                    # TODO: Bug 818287 - Screenshots include data URL prefix
                    screenshot = self.marionette.screenshot()[22:]
                    f.write(base64.decodestring(screenshot))
            except:
                traceback.print_exc()

            # page source
            try:
                with open(os.path.join(debug_path, '%s_source.txt' % test_name), 'w') as f:
                    f.write(self.marionette.page_source.encode('utf-8'))
            except:
                traceback.print_exc()

            # settings
            # Switch to top frame in case we are in a 3rd party app
            # There is no more debug gathering is not specific to the app
            self.marionette.switch_to_frame()

            try:
                with open(os.path.join(debug_path, '%s_settings.json' % test_name), 'w') as f:
                    f.write(json.dumps(self.data_layer.all_settings))
            except:
                traceback.print_exc()

        self.data_layer = None
        MarionetteTestCase.tearDown(self)
