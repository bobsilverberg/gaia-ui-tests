# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsDoNotTrack(GaiaTestCase):

    # Do Not Track Settings locators
    _donottrack_menu_item_locator = ('id', 'menuItem-doNotTrack')
    _donottrack_label_locator = ('css selector', '#doNotTrack label')
    _donottrack_checkbox_locator = ('css selector', '#doNotTrack input')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # make sure Do Not Track is off for the beginning of the test
        self.data_layer.set_setting('privacy.donottrackheader.enabled', False)

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_enable_do_not_track_via_settings_app(self):
        """Enable do not track via the Settings app"""

        # navigate to Do Not Track settings
        self.wait_for_element_present(*self._donottrack_menu_item_locator)
        donottrack_menu_item = self.marionette.find_element(*self._donottrack_menu_item_locator)

        # TODO: remove the explicit scroll once bug 833370 is fixed
        # see https://bugzilla.mozilla.org/show_bug.cgi?id=833370
        self.marionette.execute_script('arguments[0].scrollIntoView(false);',
                                       [donottrack_menu_item])
        donottrack_menu_item.tap()

        # locate the Do Not Track label and checkbox
        self.wait_for_element_displayed(*self._donottrack_label_locator)
        donottrack_label = self.marionette.find_element(*self._donottrack_label_locator)
        donottrack_checkbox = self.marionette.find_element(*self._donottrack_checkbox_locator)

        # turned off by default
        self.wait_for_condition(
            lambda m: m.find_element(*self._donottrack_checkbox_locator).get_attribute('checked') is None
        )

        # turn on - tap on the label
        donottrack_label.tap()
        self.wait_for_condition(
            lambda m: m.find_element(*self._donottrack_checkbox_locator).get_attribute('checked')
        )

        # should be on
        self.assertTrue(self.data_layer.get_setting('privacy.donottrackheader.enabled'),
                        'Do Not Track was not enabled via Settings app')

        # turn back off
        donottrack_label.tap()
        self.wait_for_condition(
            lambda m: m.find_element(*self._donottrack_checkbox_locator).get_attribute('checked') is None
        )

        # should be off
        self.assertFalse(self.data_layer.get_setting('privacy.donottrackheader.enabled'),
                         'Do Not Track was not disabled via Settings app')

    def tearDown(self):

        # make sure Do Not Track is off at the end of the test
        self.data_layer.set_setting('privacy.donottrackheader.enabled', False)

        GaiaTestCase.tearDown(self)
