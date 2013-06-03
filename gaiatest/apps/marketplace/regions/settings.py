# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Settings(Base):

    _email_account_field_locator = ('id', 'email')
    _save_locator = ('css selector', 'footer > p > button')
    _sign_in_button_locator = ('css selector', 'a.button.persona')
    _sign_out_button_locator = ('css selector', 'a.button.logout')
    _back_button_locator = ('id', 'nav-back')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._save_locator)

    def tap_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()
        from gaiatest.apps.marketplace.app import Marketplace
        return Marketplace(self.marionette)

    def wait_for_sign_in_displayed(self):
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def tap_sign_in(self):
        # TODO: click works but not tap
        self.marionette.find_element(*self._sign_in_button_locator).click()
        from gaiatest.apps.persona.app import Persona
        return Persona(self.marionette)

    def wait_for_sign_out_button(self):
        self.wait_for_element_displayed(*self._sign_out_button_locator)

    def tap_sign_out(self):
        sign_out_button = self.marionette.find_element(*self._sign_out_button_locator)
        # TODO: remove scrollIntoView hack
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [sign_out_button])
        sign_out_button.tap()

    @property
    def email(self):
        return self.marionette.find_element(*self._email_account_field_locator).get_attribute('value')
