# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestSettingsCellData(GaiaTestCase):

    # Cell Data Settings locators
    _cell_data_menu_item_locator = ('id', 'menuItem-cellularAndData')
    _carrier_name_locator = ('id', 'dataNetwork-desc')
    _cell_data_enabled_input_locator = ('xpath', "//input[@name='ril.data.enabled']")
    _cell_data_enabled_label_locator = ('xpath', "//input[@name='ril.data.enabled']/..")
    _cell_data_prompt_turn_on_button_locator = ('css selector', '#carrier-dc-warning button[type="submit"]')
    _cell_data_prompt_container_locator = ('css selector', '#carrier-dc-warning')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_enable_cell_data_via_settings_app(self):
        """ Enable cell data via the Settings app

        https://moztrap.mozilla.org/manage/case/1373/

        """
        # navigate to cell data settings
        self.wait_for_element_displayed(*self._cell_data_menu_item_locator)
        cell_data_menu_item = self.marionette.find_element(*self._cell_data_menu_item_locator)
        cell_data_menu_item.tap()

        # verify that a carrier is displayed
        self.wait_for_element_displayed(*self._carrier_name_locator)
        self.assertTrue(len(self.marionette.find_element(*self._carrier_name_locator).text) > 0)

        # enable cell data
        enabled_checkbox = self.marionette.find_element(*self._cell_data_enabled_input_locator)
        self.assertFalse(enabled_checkbox.get_attribute('checked'))

        # we have to tap on the label rather than the input
        enabled_label = self.marionette.find_element(*self._cell_data_enabled_label_locator)
        enabled_label.tap()

        # Sleep a little after the tap. It's cleaner than an if/waiting/except block
        time.sleep(1)

        # deal with prompt that sometimes appears (on first setting)
        # The prompt container and its contents return True is_displayed erroneously
        if 'current' in self.marionette.find_element(*self._cell_data_prompt_container_locator).get_attribute('class'):
            self.assertFalse(enabled_checkbox.get_attribute('checked'))
            self.assertFalse(self.data_layer.get_setting('ril.data.enabled'), "Cell data was enabled before responding to the prompt")
            turn_on_prompt_button = self.marionette.find_element(*self._cell_data_prompt_turn_on_button_locator)
            turn_on_prompt_button.tap()

        self.wait_for_condition(
            lambda m: m.find_element(*self._cell_data_enabled_input_locator).get_attribute('checked') == 'true'
        )

        # verify that cell data is now on
        self.assertTrue(self.data_layer.is_cell_data_enabled, "Cell data was not enabled via Settings app")
        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected,
                                message="Cell data was not connected via Settings app")
