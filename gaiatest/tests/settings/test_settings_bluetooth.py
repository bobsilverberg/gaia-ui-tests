# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestBluetoothSettings(GaiaTestCase):

    # Bluetooth settings locators
    _bluetooth_settings_locator = ('id', 'menuItem-bluetooth')
    _bluetooth_checkbox_locator = ('css selector', '#bluetooth-status input')
    _bluetooth_label_locator = ('css selector', '#bluetooth-status span')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_toggle_bluetooth_settings(self):
        """ Toggle Bluetooth via Settings - Networks & Connectivity

        https://moztrap.mozilla.org/manage/case/3346/

        """

        # Navigate to Bluetooth settings
        self.wait_for_element_displayed(*self._bluetooth_settings_locator)
        bluetooth_menu_item = self.marionette.find_element(*self._bluetooth_settings_locator)
        bluetooth_menu_item.tap()

        # Enable Bluetooth
        self.wait_for_element_displayed(*self._bluetooth_label_locator)
        checkbox = self.marionette.find_element(*self._bluetooth_checkbox_locator)
        self.assertIsNone(checkbox.get_attribute('checked'))

        label = self.marionette.find_element(*self._bluetooth_label_locator)
        label.tap()
        self.wait_for_condition(lambda m: m.find_element(*self._bluetooth_checkbox_locator).get_attribute('checked') == 'true')
        self.assertTrue(self.data_layer.get_setting('bluetooth.enabled'))

    def tearDown(self):

        # Disable Bluetooth
        self.data_layer.set_setting('bluetooth.enabled', False)

        GaiaTestCase.tearDown(self)
