# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class SetupEmail(Base):

    _name_locator = ('css selector', 'section.card-setup-account-info input.sup-info-name')
    _email_locator = ('css selector', 'section.card-setup-account-info input.sup-info-email')
    _password_locator = ('css selector', 'section.card-setup-account-info input.sup-info-password')
    _next_locator = ('css selector', '.sup-info-next-btn')
    _continue_button_locator = ('class name', 'sup-show-mail-btn sup-form-btn recommend')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._name_locator)

    def type_name(self, value):
        self.marionette.find_element(*self._name_locator).send_keys(value)

    def type_email(self, value):
        self.marionette.find_element(*self._email_locator).send_keys(value)

    def type_password(self, value):
        self.marionette.find_element(*self._password_locator).send_keys(value)

    def tap_next(self):
        self.marionette.tap(self.marionette.find_element(*self._next_locator))

    def wait_for_setup_complete(self):
        self.wait_for_element_displayed(*self._continue_button_locator)

    def tap_continue(self):
        self.marionette.tap(self.marionette.find_element(*self._continue_button_locator))


class ManualSetupEmail(Base):

    name = 'E-Mail'  # hack to be able to use select

    _name_locator = ('css selector', 'section.card-setup-manual-config input.sup-info-name')
    _email_locator = ('css selector', 'section.card-setup-manual-config input.sup-info-email')
    _password_locator = ('css selector', 'section.card-setup-manual-config input.sup-info-password')

    _account_type_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-account-type')

    _imap_username_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-imap-username')
    _imap_hostname_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-imap-hostname')
    _imap_port_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-imap-port')

    _smtp_username_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-smtp-username')
    _smtp_hostname_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-smtp-hostname')
    _smtp_port_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-smtp-port')

    _activesync_username_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-activesync-hostname')

    _activesync_hostname_locator = ('css selector', 'section.card-setup-manual-config .sup-manual-activesync-username')

    _next_locator = ('css selector', '.sup-manual-next-btn')
    _continue_button_locator = ('class name', 'sup-show-mail-btn sup-form-btn recommend')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._name_locator)

    def type_name(self, value):
        el = self.marionette.find_element(*self._name_locator)
        el.clear()
        el.send_keys(value)

    def type_email(self, value):
        el = self.marionette.find_element(*self._email_locator)
        el.clear()
        el.send_keys(value)

    def type_password(self, value):
        el = self.marionette.find_element(*self._password_locator)
        el.clear()
        el.send_keys(value)

    def select_account_type(self, value):
        self.marionette.find_element(*self._account_type_locator).click()
        self.select(value)

    def type_imap_name(self, value):
        el = self.marionette.find_element(*self._imap_username_locator)
        el.clear()
        el.send_keys(value)

    def type_imap_hostname(self, value):
        el = self.marionette.find_element(*self._imap_hostname_locator)
        el.clear()
        el.send_keys(value)

    def type_imap_port(self, value):
        el = self.marionette.find_element(*self._imap_port_locator)
        el.clear()
        el.send_keys(value)

    def type_smtp_name(self, value):
        el = self.marionette.find_element(*self._smtp_username_locator)
        el.clear()
        el.send_keys(value)

    def type_smtp_hostname(self, value):
        el = self.marionette.find_element(*self._smtp_hostname_locator)
        el.clear()
        el.send_keys(value)

    def type_smtp_port(self, value):
        el = self.marionette.find_element(*self._smtp_port_locator)
        el.clear()
        el.send_keys(value)

    def type_activesync_name(self, value):
        el = self.marionette.find_element(*self._activesync_username_locator)
        el.clear()
        el.send_keys(value)

    def type_activesync_hostname(self, value):
        el = self.marionette.find_element(*self._activesync_hostname_locator)
        el.clear()
        el.send_keys(value)

    def type_activesync_port(self, value):
        el = self.marionette.find_element(*self._activesync_port_locator)
        el.clear()
        el.send_keys(value)

    def tap_next(self):
        self.marionette.tap(self.marionette.find_element(*self._next_locator))

    def wait_for_setup_complete(self):
        self.wait_for_element_displayed(*self._continue_button_locator)

    def tap_continue(self):
        self.marionette.tap(self.marionette.find_element(*self._continue_button_locator))
