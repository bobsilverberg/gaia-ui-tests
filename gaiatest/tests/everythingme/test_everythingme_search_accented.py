# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestEverythingMeSearchAccented(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _search_box_locator = ('id', 'search-q')
    _search_tip_locator = ('css selector', '#helper ul li[data-index]')

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')

    # Search string
    _test_string = u"Özdemir Erdoğan"

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()

    def test_launch_everything_me_search(self):

        # swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

        # Find the search box and clear it
        self.wait_for_element_displayed(*self._search_box_locator)
        search_input = self.marionette.find_element(*self._search_box_locator)
        search_input.clear()

        # Enter the string to search
        search_input.send_keys(self._test_string)
        search_input.click()

        # Wait for the search suggestions and then tap on the first one
        self.wait_for_element_present(*self._search_tip_locator)
        search_tips = self.marionette.find_elements(*self._search_tip_locator)
        self.assertGreater(len(search_tips), 0, 'No search suggestions found')
        self.wait_for_element_displayed(*self._search_tip_locator)
        # TODO: Convert to el.tap() when bug #877174 is fixed
        self.marionette.tap(search_tips[0])

        # Wait for the apps to appear
        self.wait_for_element_present(*self._shortcut_items_locator)
        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')
        self.keyboard.tap_enter()
