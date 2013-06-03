# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase


class TestAirplaneMode(GaiaTestCase):

    _data_text_locator = ('id', 'data-desc')
    _airplane_switch_locator = ('css selector', 'ul> li:nth-child(1) label')
    _wifi_text_locator = ('id', 'wifi-desc')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.data_layer.connect_to_cell_data()
        self.data_layer.connect_to_wifi()
        self.data_layer.set_setting('geolocation.enabled', 'true')
        self.app = self.apps.launch('Settings')

    def test_toggle_airplane_mode(self):

        self.wait_for_element_displayed(*self._airplane_switch_locator)

        # Switch on Airplane mode
        self.marionette.find_element(*self._airplane_switch_locator).tap()

        # wait for Cell Data to be disabled, this takes the longest when airplane mode is switched on
        self.wait_for_condition(lambda s: 'SIM card not ready' in self.marionette.find_element(*self._data_text_locator).text)

        # check Wifi is disabled
        self.assertFalse(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was still connected after switching on Airplane mode")

        # check that Cell Data is disabled
        self.assertFalse(self.data_layer.get_setting('ril.data.enabled'), "Cell Data was still connected after switching on Airplane mode")

        # check GPS is disabled
        self.assertFalse(self.data_layer.get_setting('geolocation.enabled'), "GPS was still connected after switching on Airplane mode")

        # switch back to app frame
        self.marionette.switch_to_frame(self.app.frame)

        # Switch off Airplane mode
        self.marionette.find_element(*self._airplane_switch_locator).tap()

        #wait for wifi to be connected, because this takes the longest to connect after airplane mode is switched off
        self.wait_for_condition(lambda s: 'Connected' in self.marionette.find_element(*self._wifi_text_locator).text)

        # check Wifi is enabled
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected after switching off Airplane mode")

        # check that Cell Data is enabled
        self.assertTrue(self.data_layer.get_setting('ril.data.enabled'), "Cell data was not connected after switching off Airplane mode")

        # check GPS is enabled
        self.assertTrue(self.data_layer.get_setting('geolocation.enabled'), "GPS was not enabled after switching off Airplane mode")
