# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.marionette import Actions
from gaiatest import GaiaTestCase


class TestDeleteApp(GaiaTestCase):

    MANIFEST = 'http://mozqa.com/data/webapps/mozqa.com/manifest.webapp'
    APP_NAME = 'Mozilla QA WebRT Tester'
    APP_INSTALLED = False

    _icon_locator = ('css selector', 'li.icon[aria-label="%s"]' % APP_NAME)
    _delete_app_locator = ('css selector', 'span.options')

    # App install popup
    _yes_button_locator = ('id', 'app-install-install-button')
    _notification_banner_locator = ('id', 'system-banner')

    # Delete popup
    _confirm_delete_locator = ('id', 'confirm-dialog-confirm-button')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.homescreen = self.apps.launch('Homescreen')

    def test_delete_app(self):

        # install app
        self.marionette.switch_to_frame()
        self.marionette.execute_script(
            'navigator.mozApps.install("%s")' % self.MANIFEST)

        # click YES on the installation dialog and wait for icon displayed
        self.wait_for_element_displayed(*self._yes_button_locator)
        yes = self.marionette.find_element(*self._yes_button_locator)
        self.marionette.tap(yes)
        self.APP_INSTALLED = True

        # wait for the app to be installed and the notification banner to be available
        self.wait_for_element_displayed(*self._notification_banner_locator)
        notification = self.marionette.find_element(*self._notification_banner_locator).text
        self.assertEqual('%s installed' % self.APP_NAME, notification)
        self.wait_for_element_not_displayed(*self._notification_banner_locator)

        self.marionette.switch_to_frame(self.homescreen.frame)
        self.assertTrue(self.is_element_present(*self._icon_locator), "The installed app can't be found")

        # switch pages until the app is found
        while not self.marionette.find_element(*self._icon_locator).is_displayed():
            self._go_to_next_page()

        # check that the app is available
        app_icon = self.marionette.find_element(*self._icon_locator)
        self.assertTrue(app_icon.is_displayed())

        # go to edit mode
        Actions(self.marionette). \
            press(app_icon). \
            wait(3). \
            release(). \
            perform()

        # delete the app
        delete_button = app_icon.find_element(*self._delete_app_locator)
        self.marionette.tap(delete_button)

        self.wait_for_element_displayed(*self._confirm_delete_locator)
        delete = self.marionette.find_element(*self._confirm_delete_locator)
        self.marionette.tap(delete)
        self.APP_INSTALLED = False

        self.wait_for_element_not_present(*self._icon_locator)

        # return to normal mode
        self.marionette.switch_to_frame()
        self._touch_home_button()

        # check that the app is no longer available
        with self.assertRaises(AssertionError):
            self.apps.launch(self.APP_NAME)

    def _touch_home_button(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def tearDown(self):
        if self.APP_INSTALLED:
            self.apps.uninstall(self.APP_NAME)
        GaiaTestCase.tearDown(self)
