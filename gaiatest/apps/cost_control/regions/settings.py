# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class Settings(Base):

    _settings_iframe_locator = ('id', "settings-view-placeholder")
    _settings_title_locator = ('css selector', 'section#settings-view h1')

    _data_alert_label_locator = ('xpath', "//ul[preceding-sibling::header[@id='data-usage-settings']]/li[2]/label")
    _data_alert_switch_locator = ('css selector', 'input[data-option="dataLimit"]')
    _when_use_is_above_button_locator = ('css selector', 'button[data-widget-type="data-limit"]')
    _unit_button_locator = ('css selector', '#data-limit-dialog form button')
    _size_input_locator = ('css selector', '#data-limit-dialog form input')
    _usage_done_button_locator = ('id', 'data-usage-done-button')

    _reset_button_locator = ('id', 'reset-data-usage')
    _reset_confirm_locator = ('css selector', 'section#reset-confirmation-dialog button.danger')
    _done_button_locator = ('css selector', 'section#settings-view button#close-settings')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        # go into iframe of usage app settings
        self.wait_for_element_displayed(*self._settings_iframe_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._settings_iframe_locator))
        self.wait_for_element_displayed(*self._settings_title_locator)

    def toggle_data_alert_switch(self, value):
        self.wait_for_element_displayed(*self._data_alert_label_locator)
        switch = self.marionette.find_element(*self._data_alert_switch_locator)
        if switch.is_selected() is not value:
            label = self.marionette.find_element(*self._data_alert_label_locator)
            label.tap()

    def select_when_use_is_above_unit_and_value(self, unit, value):

        when_use_is_above_button = self.marionette.find_element(*self._when_use_is_above_button_locator)
        self.wait_for_condition(
            lambda m: m.find_element(*self._when_use_is_above_button_locator).get_attribute('disabled') == 'false'
        )
        when_use_is_above_button.tap()

        self.wait_for_element_displayed(*self._unit_button_locator)
        current_unit = self.marionette.find_element(*self._unit_button_locator)
        if current_unit.text is not unit:
            current_unit.tap()
            # We need to wait for the javascript to do its stuff
            self.wait_for_condition(lambda m: m.find_element(*self._unit_button_locator).text == unit)

        # clear the original assigned value and set it to the new value
        self.wait_for_element_displayed(*self._size_input_locator)
        size = self.marionette.find_element(*self._size_input_locator)
        size.clear()
        size.send_keys(value)
        done = self.marionette.find_element(*self._usage_done_button_locator)
        done.tap()

    def reset_data_usage(self):
        self.wait_for_element_displayed(*self._settings_title_locator)
        self.marionette.find_element(*self._reset_button_locator).tap()
        self.wait_for_element_displayed(*self._reset_confirm_locator)
        self.marionette.find_element(*self._reset_confirm_locator).tap()
        self.wait_for_element_displayed(*self._settings_title_locator)

    def tap_done(self):
        self.wait_for_element_displayed(*self._done_button_locator)
        self.marionette.find_element(*self._done_button_locator).tap()
        # Switch back to Cos Control app frame
        from gaiatest.apps.cost_control.app import CostControl
        CostControl(self.marionette).launch()
