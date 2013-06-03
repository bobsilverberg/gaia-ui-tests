# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.cost_control.app import CostControl


class FTUStep3(CostControl):

    _data_alert_title_locator = ('css selector', '#non-vivo-step-2 h1[data-l10n-id="fte-onlydata3-title"]')
    _ftu_usage_locator = ('css selector', '#non-vivo-step-2 span.tag')
    _ftu_data_alert_switch_locator = ('css selector', '#non-vivo-step-2 label.end input')
    _ftu_data_alert_label_locator = ('css selector', '#non-vivo-step-2 label.end')
    _unit_button_locator = ('css selector', '#data-limit-dialog form button span')
    _size_input_locator = ('css selector', '#data-limit-dialog form input')
    _usage_done_button_locator = ('id', 'data-usage-done-button')
    _go_button_locator = ('css selector', '#non-vivo-step-2 button.recommend')

    def __init__(self, marionette):
        CostControl.__init__(self, marionette)
        self.wait_for_element_displayed(*self._data_alert_title_locator)

    def toggle_data_alert_switch(self, value):
        self.wait_for_element_displayed(*self._ftu_data_alert_label_locator)
        switch = self.marionette.find_element(*self._ftu_data_alert_switch_locator)
        if switch.is_selected() is not value:
            label = self.marionette.find_element(*self._ftu_data_alert_label_locator)
            label.tap()

    def select_when_use_is_above_unit_and_value(self, unit, value):
        self.wait_for_element_displayed(*self._ftu_usage_locator)
        usage = self.marionette.find_element(*self._ftu_usage_locator)
        usage.tap()

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

    def tap_lets_go(self):
        self.wait_for_element_displayed(*self._go_button_locator)
        self.marionette.find_element(*self._go_button_locator).tap()
