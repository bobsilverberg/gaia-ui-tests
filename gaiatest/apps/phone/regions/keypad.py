# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from marionette.marionette import Actions
from gaiatest.apps.phone.app import Phone
from gaiatest.apps.phone.regions.call_screen import CallScreen


class Keypad(Phone):

    #locators
    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _call_bar_locator = ('id', 'keypad-callbar-call-action')

    def __init__(self, marionette):
        Phone.__init__(self, marionette)
        self.wait_for_element_displayed(*self._keyboard_container_locator)

    @property
    def phone_number(self):
        return self.marionette.find_element(*self._phone_number_view_locator).get_attribute('value')

    def dial_phone_number(self, value):
        for i in value:
            if i == "+":
                zero_button = self.marionette.find_element('css selector', 'div.keypad-key[data-value="0"]')
                Actions(self.marionette).long_press(zero_button, 1.2).perform()
            else:
                self.marionette.find_element('css selector', 'div.keypad-key[data-value="%s"]' % i).tap()
                time.sleep(0.25)

    def call_number(self, value):
        self.dial_phone_number(value)
        return self.tap_call_button()

    def tap_call_button(self, switch_to_call_screen=True):
        self.marionette.find_element(*self._call_bar_locator).tap()
        if switch_to_call_screen:
            return CallScreen(self.marionette)
