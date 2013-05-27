# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion
from gaiatest.apps.email.regions.setup import SetupEmail
from gaiatest.apps.email.regions.setup import ManualSetupEmail
from gaiatest.apps.email.regions.settings import Settings


class Email(Base):

    name = 'E-Mail'

    _header_area_locator = ('css selector', '.msg-list-header.msg-nonsearch-only')
    _email_locator = ('css selector', '.msg-header-item')
    _syncing_locator = ('css selector', '.msg-messages-syncing > .small')
    _manual_setup_locator = ('css selector', '.sup-manual-config-btn')

    def basic_setup_email(self, name, email, password):

        setup = SetupEmail(self.marionette)
        setup.type_name(name)
        setup.type_email(email)
        setup.type_password(password)
        setup.tap_next()

        setup.wait_for_setup_complete()

        setup.tap_continue()
        self.wait_for_condition(lambda m: self.is_element_displayed(*self._header_area_locator))

    def setup_IMAP_email(self, imap):
        setup = self.tap_manual_setup()
        setup.type_name(imap['name'])
        setup.type_email(imap['email'])
        setup.type_password(imap['password'])

        setup.select_account_type('IMAP+SMTP')

        setup.type_imap_hostname(imap['imap_hostname'])
        setup.type_imap_name(imap['imap_name'])
        setup.type_imap_port(imap['imap_port'])

        setup.type_smtp_hostname(imap['smtp_hostname'])
        setup.type_smtp_name(imap['smtp_name'])
        setup.type_smtp_port(imap['smtp_port'])

        setup.tap_next()
        setup.wait_for_setup_complete()
        setup.tap_continue()
        self.wait_for_header_area()

    def delete_email_account(self, index):

        toolbar = self.header.tap_menu()
        toolbar.tap_settings()
        settings = Settings(self.marionette)
        account_settings = settings.email_accounts[index].tap()
        delete_confirmation = account_settings.tap_delete()
        delete_confirmation.tap_delete()

    def tap_manual_setup(self):
        self.wait_for_element_displayed(*self._manual_setup_locator)
        self.marionette.find_element(*self._manual_setup_locator).tap()
        return ManualSetupEmail(self.marionette)

    @property
    def header(self):
        return Header(self.marionette)

    @property
    def toolbar(self):
        return ToolBar(self.marionette)

    @property
    def mails(self):
        return [Message(self.marionette, mail) for mail in self.marionette.find_elements(*self._email_locator)]

    def wait_for_emails_to_sync(self):
        self.wait_for_element_not_displayed(*self._syncing_locator)

    def wait_for_header_area(self):
        self.wait_for_element_displayed(*self._header_area_locator)


class Header(Base):
    _menu_button_locator = ('css selector', '.card.center .msg-folder-list-btn')
    _compose_button_locator = ('css selector', '.card.center .msg-compose-btn')
    _label_locator = ('css selector', '.card.center .msg-list-header-folder-label.header-label')

    def tap_menu(self):
        self.marionette.find_element(*self._menu_button_locator).tap()
        toolbar = ToolBar(self.marionette)
        self.wait_for_condition(lambda m: toolbar.is_settings_visible)
        return toolbar

    def tap_compose(self):
        self.marionette.find_element(*self._compose_button_locator).tap()
        from gaiatest.apps.email.regions.new_email import NewEmail
        return NewEmail(self.marionette)

    @property
    def label(self):
        return self.marionette.find_element(*self._label_locator).text

    @property
    def is_menu_visible(self):
        return self.is_element_displayed(*self._menu_button_locator)

    @property
    def is_compose_visible(self):
        return self.is_element_displayed(*self._compose_button_locator)


class ToolBar(Base):
    _refresh_locator = ('css selector', '.msg-refresh-btn')
    _search_locator = ('css selector', '.msg-search-btn')
    _edit_locator = ('css selector', '.msg-edit-btn')
    _settings_locator = ('css selector', '.fld-nav-settings-btn')

    def tap_refresh(self):
        self.marionette.find_element(*self._refresh_locator).tap()

    def tap_search(self):
        self.marionette.find_element(*self._search_locator).tap()

    def tap_edit(self):
        self.marionette.find_element(*self._edit_locator).tap()

    def tap_settings(self):
        # TODO: el.tap() if not tapping settings button
        self.marionette.find_element(*self._settings_locator).click()

    @property
    def is_refresh_visible(self):
        return self.is_element_displayed(*self._refresh_locator)

    @property
    def is_search_visible(self):
        return self.is_element_displayed(*self._search_locator)

    @property
    def is_edit_visible(self):
        return self.is_element_displayed(*self._edit_locator)

    @property
    def is_settings_visible(self):
        return self.is_element_displayed(*self._settings_locator)


class Message(PageRegion):
    _subject_locator = ('css selector', '.msg-header-subject')

    @property
    def subject(self):
        return self.root_element.find_element(*self._subject_locator).text

    def tap_subject(self):
        el = self.root_element.find_element(*self._subject_locator)
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [el])
        self.marionette.tap(self.root_element.find_element(*self._subject_locator))
        from gaiatest.apps.email.regions.read_email import ReadEmail
        return ReadEmail(self.marionette)
