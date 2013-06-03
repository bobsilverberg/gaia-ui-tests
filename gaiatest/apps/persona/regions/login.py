# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base


class Login(Base):
    # iframes
    _persona_frame_locator = ('css selector', "iframe.screen[data-url*='persona.org/sign_in#NATIVE']")

    # persona login
    _body_loading_locator = ('css selector', 'body.loading')
    _email_input_locator = ('id', 'authentication_email')
    _password_input_locator = ('id', 'authentication_password')
    _continue_button_locator = ('css selector', '.continue.right')
    _returning_button_locator = ('css selector', 'button.isReturning')
    _sign_in_button_locator = ('id', 'signInButton')
    _this_session_only_button_locator = ('id', 'this_is_not_my_computer')
    _this_is_not_me_locator = ('id', 'thisIsNotMe')

    _create_password_locator = ('id', 'password')
    _confirm_password_locator = ('id', 'vpassword')
    _verify_user_locator = ('id', 'verify_user')

    _form_section_locator = ('css selector', 'div.vertical div.form_section')

    def switch_to_persona_frame(self):
        self.wait_for_element_present(*self._persona_frame_locator)
        self.frame = self.marionette.find_element(*self._persona_frame_locator)
        self.marionette.switch_to_frame(self.frame)

        self.wait_for_element_not_present(*self._body_loading_locator)

    def type_email(self, value):
        email_field = self.marionette.find_element(*self._email_input_locator)
        email_field.send_keys(value)
        self.dismiss_keyboard()

    def type_password(self, value):
        password_field = self.marionette.find_element(*self._password_input_locator)
        password_field.send_keys(value)
        self.dismiss_keyboard()

    def type_create_password(self, value):
        password_field = self.marionette.find_element(*self._create_password_locator)
        password_field.send_keys(value)

    def type_confirm_password(self, value):
        password_field = self.marionette.find_element(*self._confirm_password_locator)
        password_field.send_keys(value)

    def tap_continue(self):
        continue_button = self.marionette.find_element(*self._continue_button_locator)
        self.wait_for_element_displayed(*self._continue_button_locator)
        continue_button.tap()
        self.wait_for_element_not_displayed(*self._continue_button_locator)

    def tap_verify_user(self):
        self.marionette.find_element(*self._verify_user_locator).tap()

    def tap_sign_in(self):
        self.marionette.find_element(*self._sign_in_button_locator).tap()

    def tap_this_is_not_me(self):
        self.marionette.find_element(*self._this_is_not_me_locator).tap()

    def tap_returning(self):
        self.marionette.find_element(*self._returning_button_locator).tap()

    def tap_this_session_only(self):
        self.marionette.find_element(*self._this_session_only_button_locator).tap()

    @property
    def form_section_id(self):
        self.wait_for_element_displayed(*self._form_section_locator)
        return self.marionette.find_element(*self._form_section_locator).get_attribute('id')

    def wait_for_sign_in_button(self):
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def wait_for_email_input(self):
        self.wait_for_element_displayed(*self._email_input_locator)

    def wait_for_password_input(self):
        self.wait_for_element_displayed(*self._password_input_locator)
