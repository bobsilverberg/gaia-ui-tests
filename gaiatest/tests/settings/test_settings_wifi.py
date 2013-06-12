# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsWifi(GaiaTestCase):

    # Wifi Settings locators
    _wifi_menu_item_locator = ('id', 'menuItem-wifi')
    _wifi_enabled_label_locator = ('css selector', '#wifi-enabled label')
    _wifi_enabled_checkbox_locator = ('css selector', '#wifi-enabled input')
    _available_networks_locator = ('css selector', '#wifi-availableNetworks > li > aside[class*="wifi-signal"]')
    _password_input_locator = ('css selector', '#wifi-auth input[type="password"]')
    _password_ok_button_locator = ('css selector', '#wifi-auth button[type="submit"]')
    _connected_message_locator = ('css selector', '#wifi-availableNetworks li.active small')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_connect_to_wifi_via_settings_app(self):
        """ Connect to a wifi network via the Settings app

        https://github.com/mozilla/gaia-ui-tests/issues/342

        """
        # navigate to wifi settings
        self.wait_for_element_present(*self._wifi_menu_item_locator)
        wifi_menu_item = self.marionette.find_element(*self._wifi_menu_item_locator)
        wifi_menu_item.tap()
        self.wait_for_condition(lambda m: wifi_menu_item.location['x'] + wifi_menu_item.size['width'] == 0)

        # enable wifi
        self.wait_for_element_present(*self._wifi_enabled_checkbox_locator)
        enabled_checkbox = self.marionette.find_element(*self._wifi_enabled_checkbox_locator)
        self.assertIsNone(enabled_checkbox.get_attribute('checked'))
        # we have to tap on the label rather than the input
        enabled_label = self.marionette.find_element(*self._wifi_enabled_label_locator)
        enabled_label.tap()

        # Wait for some networks to be found
        self.wait_for_condition(lambda m: len(m.find_elements(*self._available_networks_locator)) > 0,
                                message="No networks listed on screen")

        this_network_locator = ('xpath', "//li/a[text()='%s']" % self.testvars['wifi']['ssid'])
        wifi_network = self.marionette.find_element(*this_network_locator)
        wifi_network.tap()

        if self.testvars['wifi'].get('keyManagement'):
            password = self.testvars['wifi'].get('psk') or self.testvars['wifi'].get('wep')
            if not password:
                self.fail('No psk or wep key found in testvars for secured wifi network.')

            self.wait_for_element_displayed(*self._password_input_locator)
            password_input = self.marionette.find_element(*self._password_input_locator)
            password_input.send_keys(password)
            ok = self.marionette.find_element(*self._password_ok_button_locator)
            ok.tap()

        self.wait_for_condition(
            lambda m: m.find_element(*self._connected_message_locator).text == "Connected")

        # verify that wifi is now on
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via Settings app")
