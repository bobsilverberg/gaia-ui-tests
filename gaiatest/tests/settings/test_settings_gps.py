# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsGPS(GaiaTestCase):

    # GPS Settings locators
    _gps_enabled_input_locator = ('xpath', "//input[@name='geolocation.enabled']")
    _gps_enabled_label_locator = ('xpath', "//input[@name='geolocation.enabled']/..")

    def setUp(self):

        GaiaTestCase.setUp(self)

        # make sure GPS is on for the beginning of the test
        self.data_layer.set_setting('geolocation.enabled', 'true')

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_enable_gps_via_settings_app(self):
        """ Enable GPS via the Settings app

        https://moztrap.mozilla.org/manage/case/2885/

        """
        # locate the GPS switch
        self.wait_for_element_displayed(*self._gps_enabled_label_locator)
        enabled_switch = self.marionette.find_element(*self._gps_enabled_input_locator)

        # should be on by default
        self.wait_for_condition(
            lambda m: m.find_element(*self._gps_enabled_input_locator).get_attribute('checked')
        )

        # turn off - we have to tap on the label rather than the input
        enabled_label = self.marionette.find_element(*self._gps_enabled_label_locator)
        enabled_label.tap()
        self.wait_for_condition(
            lambda m: not self.marionette.find_element(*self._gps_enabled_input_locator).get_attribute('checked')
        )

        # should be off
        self.assertFalse(self.data_layer.get_setting('geolocation.enabled'), "GPS was not enabled via Settings app")

        # turn back on
        enabled_label = self.marionette.find_element(*self._gps_enabled_label_locator)
        enabled_label.tap()
        enabled_switch = self.marionette.find_element(*self._gps_enabled_input_locator)
        self.wait_for_condition(
            lambda m: m.find_element(*self._gps_enabled_input_locator).get_attribute('checked') == 'true'
        )

        # should be on
        self.assertTrue(self.data_layer.get_setting('geolocation.enabled'), "GPS was not disabled via Settings app")
