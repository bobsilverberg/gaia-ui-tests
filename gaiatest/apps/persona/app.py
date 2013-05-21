# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.persona.regions.login import Login


class Persona(Base):

    # Trusty UI on home screen
    _tui_container_locator = ('id', 'trustedui-frame-container')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._tui_container_locator)

    def login(self, email, password):
        login = Login(self.marionette)

        login.switch_to_persona_frame()

        # This is a hack until we are able to run test with a clean profile
        # if a user was logged in tap this is not me
        if login.form_section_id == "selectEmail":
            login.wait_for_sign_in_button()
            login.tap_this_is_not_me()

        login.wait_for_email_input()
        login.type_email(email)
        login.tap_continue()

        # if we login with an unverified user we have to confirm the password
        if login.form_section_id == "authentication_form":
            login.wait_for_password_input()
            login.type_password(password)
            login.tap_returning()
        elif login.form_section_id == "set_password":
            login.type_create_password(password)
            login.type_confirm_password(password)
            login.tap_verify_user()
        else:
            raise Exception('Could not log into Persona')
