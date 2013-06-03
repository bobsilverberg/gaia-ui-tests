# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys
from gaiatest.apps.base import Base


class Marketplace(Base):

    # Default to the Dev app
    name = 'Marketplace Dev'

    _marketplace_iframe_locator = ('css selector', 'iframe[src*="marketplace"]')

    _loading_fragment_locator = ('css selector', 'div.loading-fragment')
    _error_title_locator = ('css selector', 'div.modal-dialog-message-container > h3.title')
    _error_message_locator = ('css selector', 'div.modal-dialog-message-container .message')
    _settings_button_locator = ('css selector', 'a.header-button.settings')

    # Marketplace search on home page
    _search_locator = ('id', 'search-q')
    _signed_in_notification_locator = ('css selector', '#notification.show')

    def __init__(self, marionette, app_name=False):
        Base.__init__(self, marionette)
        if app_name:
            self.name = app_name

    def switch_to_marketplace_frame(self):
        """Only Marketplace production has a frame for the app."""
        self.marionette.switch_to_frame(self.marionette.find_element(*self._marketplace_iframe_locator))

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._loading_fragment_locator)

    @property
    def error_title_text(self):
        return self.marionette.find_element(*self._error_title_locator).text

    @property
    def error_message_text(self):
        return self.marionette.find_element(*self._error_message_locator).text

    def search(self, term):
        search_box = self.marionette.find_element(*self._search_locator)

        # search for the app
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)
        from gaiatest.apps.marketplace.regions.search_results import SearchResults
        return SearchResults(self.marionette)

    def tap_settings(self):
        self.marionette.find_element(*self._settings_button_locator).tap()
        from gaiatest.apps.marketplace.regions.settings import Settings
        return Settings(self.marionette)

    def wait_for_setting_displayed(self):
        self.wait_for_element_displayed(*self._settings_button_locator)

    def wait_for_signed_in_notification(self):
        self.wait_for_element_displayed(*self._signed_in_notification_locator)

    def tap_signed_in_notification(self):
        self.marionette.find_element(*self._signed_in_notification_locator).tap()
