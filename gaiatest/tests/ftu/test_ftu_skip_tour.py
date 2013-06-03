# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import re


class TestFtu(GaiaTestCase):

    _activation_section_locator = ('id', 'activation')
    _main_title_locator = ('id', 'main_title')

    _next_button_locator = ('id', 'forward')

    # Step Languages section
    _section_languages_locator = ('id', 'languages')
    _listed_languages_locator = ('css selector', "#languages ul li input[name='language.current']")

    # Step Cell data section
    _section_cell_data_locator = ('id', 'data_3g')
    _enable_data_checkbox_locator = ('css selector', '#data_3g .pack-end')

    # Step Wifi
    _section_wifi_locator = ('id', 'wifi')
    _found_wifi_networks_locator = ('css selector', 'ul#networks-list li')
    _network_state_locator = ('xpath', 'p[2]')
    _password_input_locator = ('id', 'wifi_password')
    _join_network_locator = ('id', 'wifi-join-button')

    # Step Date & Time
    _section_date_time_locator = ('id', 'date_and_time')
    _timezone_continent_locator = ('css selector', '#time-form li:nth-child(1) > .change.icon.icon-dialog')
    _timezone_city_locator = ('css selector', '#time-form li:nth-child(2) > .change.icon.icon-dialog')
    _time_zone_title_locator = ('id', 'time-zone-title')

    # Section Import contacts
    _section_import_contacts_locator = ('id', 'import_contacts')
    _import_from_sim_locator = ('id', 'sim-import-button')
    _sim_import_feedback_locator = ('css selector', '.ftu p')

    # Section About Your rights
    _section_ayr_locator = ('id', 'about-your-rights')

    # Section Welcome Browser
    _section_welcome_browser_locator = ('id', 'welcome_browser')
    _enable_statistic_checkbox_locator = ('id', 'form_share_statistics')

    # Section Privacy Choices
    _section_browser_privacy_locator = ('id', 'browser_privacy')
    _email_field_locator = ('css selector', 'input[type="email"]')

    # Section Finish
    _section_finish_locator = ('id', 'finish-screen')
    _skip_tour_button_locator = ('id', 'skip-tutorial-button')
    _take_tour_button_locator = ('id', 'lets-go-button')

    # Section Tour
    _step1_header_locator = ('id', 'step1Header')
    _step2_header_locator = ('id', 'step2Header')
    _step3_header_locator = ('id', 'step3Header')
    _step4_header_locator = ('id', 'step4Header')
    _step5_header_locator = ('id', 'step5Header')
    _tour_next_button_locator = ('id', 'forwardTutorial')
    _tour_back_button_locator = ('id', 'backTutorial')

    # Section Tutorial Finish
    _section_tutorial_finish_locator = ('id', 'tutorialFinish')
    _lets_go_button_locator = ('id', 'tutorialFinished')

    # Pattern for import sim contacts message
    _pattern_contacts = re.compile("^No contacts detected on SIM to import$|^Imported one contact$|^Imported [0-9]+ contacts$")
    _pattern_contacts_0 = re.compile("^No contacts detected on SIM to import$")
    _pattern_contacts_1 = re.compile("^Imported one contact$")
    _pattern_contacts_N = re.compile("^Imported ([0-9]+) contacts$")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # We need WiFi enabled but not connected to a network
        self.data_layer.enable_wifi()
        self.data_layer.forget_all_networks()

        # launch the First Time User app
        self.app = self.apps.launch('FTU')

    def create_language_locator(self, language):
        return ('css selector', "#languages ul li input[name='language.current'][value='%s'] ~ p" % language)

    def test_ftu_skip_tour(self):
        # https://moztrap.mozilla.org/manage/case/3876/
        # 3876, 3879

        self.wait_for_element_displayed(*self._section_languages_locator)

        listed_languages = self.marionette.find_elements(*self._listed_languages_locator)
        self.assertGreater(len(listed_languages), 0, "No languages listed on screen")

        # select en-US due to the condition of this test is only for en-US
        language_item = self.marionette.find_element(*self.create_language_locator("en-US"))
        language_item.tap()

        # Tap next
        self.wait_for_element_displayed(*self._next_button_locator)
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_cell_data_locator)

        # Tap enable data
        self.marionette.find_element(*self._enable_data_checkbox_locator).tap()

        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected,
                                message="Cell data was not connected by FTU app")

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_wifi_locator)

        # Wait for some networks to be found
        self.wait_for_condition(lambda m: len(m.find_elements(*self._found_wifi_networks_locator)) > 0,
                                message="No networks listed on screen")

        wifi_network = self.marionette.find_element('id', self.testvars['wifi']['ssid'])
        wifi_network.tap()

        # This is in the event we are using a Wifi Network that requires a password
        # We cannot be sure of this thus need the logic
        if self.testvars['wifi'].get('keyManagement'):

            self.wait_for_element_displayed(*self._password_input_locator)
            password = self.marionette.find_element(*self._password_input_locator)
            password.send_keys(self.testvars['wifi'].get('psk') or self.testvars['wifi'].get('wep'))
            self.marionette.find_element(*self._join_network_locator).tap()

        self.wait_for_condition(
            lambda m: m.find_element(
                'id', self.testvars['wifi']['ssid']).find_element(*self._network_state_locator).text == "Connected"
        )

        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']),
                        "WiFi was not connected via FTU app")

        # is_wifi_connected() calls switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_date_time_locator)

        # Set timezone
        continent_select = self.marionette.find_element(*self._timezone_continent_locator)
        # Click to activate the b2g select element (tap does not work see bug 833061)
        continent_select.click()
        self._select("Asia")

        city_select = self.marionette.find_element(*self._timezone_city_locator)
        # Click to activate the b2g select element (tap does not work see bug 833061)
        city_select.click()
        self._select("Almaty")

        self.assertEqual(self.marionette.find_element(*self._time_zone_title_locator).text,
                         "UTC+06:00 Asia/Almaty")

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_import_contacts_locator)

        # Tap import from SIM
        # You can do this as many times as you like without db conflict
        self.marionette.find_element(*self._import_from_sim_locator).tap()

        # pass third condition when contacts are 0~N
        self.wait_for_condition(lambda m: self._pattern_contacts.match(m.find_element(*self._sim_import_feedback_locator).text) is not None,
                                message="Contact did not import from sim before timeout")
        # Find how many contacts are imported.
        import_sim_message = self.marionette.find_element(*self._sim_import_feedback_locator).text
        import_sim_count = None
        if self._pattern_contacts_0.match(import_sim_message) is not None:
            import_sim_count = 0
        elif self._pattern_contacts_1.match(import_sim_message) is not None:
            import_sim_count = 1
        elif self._pattern_contacts_N.match(import_sim_message) is not None:
            count = self._pattern_contacts_N.match(import_sim_message).group(1)
            import_sim_count = int(count)

        self.assertEqual(len(self.data_layer.all_contacts), import_sim_count)

        # all_contacts switches to top frame; Marionette needs to be switched back to ftu
        self.marionette.switch_to_frame(self.app.frame)

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_welcome_browser_locator)

        # Tap the statistics box and check that it sets a setting
        # TODO assert via settings API that this is set. Currently it is not used
        self.marionette.find_element(*self._enable_statistic_checkbox_locator).tap()

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_browser_privacy_locator)

        # Enter a dummy email address and check it set inside the os
        # TODO assert that this is preserved in the system somewhere. Currently it is not used
        self.marionette.find_element(*self._email_field_locator).send_keys("testuser@mozilla.com")

        # Tap next
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_finish_locator)

        # Skip the tour
        self.marionette.find_element(*self._skip_tour_button_locator).tap()

        # Switch back to top level now that FTU app is gone
        self.marionette.switch_to_frame()

    def tearDown(self):

        # TODO flush any settings set by the FTU app

        self.data_layer.disable_wifi()

        GaiaTestCase.tearDown(self)

    def _select(self, match_string):
        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text

        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        # Loop options until we find the match
        for li in options:
            if li.text == match_string:
                li.tap()
                break

        close_button.tap()

        # Now back to app
        self.marionette.switch_to_frame(self.app.frame)
