# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestChangeLanguage(GaiaTestCase):

    # Language settings locators
    _settings_header_text_locator = ('css selector', '#root > header > h1')
    _language_settings_locator = ('id', 'menuItem-languageAndRegion')
    _language_section_locator = ('id', 'languages')
    _select_language_locator = ('css selector', '#languages li:nth-child(2) .fake-select button')
    _back_button_locator = ('css selector', ".current header > a")

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_change_language_settings(self):

        # Navigate to Language settings
        self.wait_for_element_present(*self._language_settings_locator)
        language_item = self.marionette.find_element(*self._language_settings_locator)

        # Select Language
        # TODO bug 878017 - remove the explicit scroll once bug is fixed
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [language_item])
        language_item.tap()

        self.wait_for_element_displayed(*self._language_section_locator)
        self.wait_for_element_displayed(*self._select_language_locator)

        select_box = self.marionette.find_element(*self._select_language_locator)
        select_box.tap()

        self._select(u'Fran\u00E7ais')

        # Go back to Settings menu
        go_back = self.marionette.find_element(*self._back_button_locator)
        go_back.tap()

        after_language_change = self.marionette.find_element(*self._settings_header_text_locator).text

        # Verify that language has changed
        self.assertEqual(after_language_change, u'Param\u00E8tres')
        self.assertEqual(self.data_layer.get_setting('language.current'), "fr")

    def _select(self, match_string):
        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text

        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        self.wait_for_condition(lambda m: len(self.marionette.find_elements('css selector', '#value-selector-container li')) > 0)

        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        # Loop options until we find the match
        for option in options:
            if option.text == match_string:
                # TODO: remove the explicit scroll once bug 833370 is fixed
                self.marionette.execute_script("arguments[0].scrollIntoView(false);", [option])
                option.click()
                break

        close_button.tap()

        self.marionette.switch_to_frame(self.app.frame)
