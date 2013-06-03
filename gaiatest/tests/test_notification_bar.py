# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import time


class TestNotificationBar(GaiaTestCase):

    # notification data
    _notification_title = 'TestNotificationBar_TITLE'
    _notification_body = 'TestNotificationBar_BODY'

    # status bar
    _statusbar_locator = ('id', 'statusbar')
    _statusbar_notification_locator = ('id', 'statusbar-notification')
    _notification_toaster_locator = ('id', 'notification-toaster')

    # expanded status bar
    _notification_container_locator = ('id', 'desktop-notifications-container')
    _notification_clear_locator = ('id', 'notification-clear')
    _notification_body_in_container_locator = ('xpath', '//div[@id="desktop-notifications-container"]/div[@class="notification"]/div[@class="detail"]')
    _notifications_in_container_locator = ('css selector', 'div#desktop-notifications-container > div.notification')

    def setUp(self):
        GaiaTestCase.setUp(self)

    def test_notification_bar(self):

        self.wait_for_element_displayed(*self._statusbar_locator)
        # Push a notification
        self.marionette.execute_script('navigator.mozNotification.createNotification("%s", "%s").show();' % (self._notification_title, self._notification_body))

        # Assert the notification pops up and then collapses
        notification_toaster = self.marionette.find_element(*self._notification_toaster_locator)

        # TODO Re-enable this when Bug 861874
        # self.wait_for_element_displayed(*self._notification_toaster_locator)
        self.wait_for_condition(lambda m: m.find_element(*self._notification_toaster_locator).location['y'] == 0)

        # TODO Re-enable this when Bug 861874
        # self.wait_for_element_not_displayed(*self._notification_toaster_locator)
        self.wait_for_condition(lambda m: m.find_element(*self._notification_toaster_locator).location['y'] == -50)

        # Expand the notification bar
        self.wait_for_element_displayed(*self._statusbar_notification_locator)
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        self.wait_for_condition(lambda m: m.find_element(*self._notification_container_locator).location['y'] == 50)

        # Assert there is one notification is listed in notifications-container
        notifications_in_container = self.marionette.find_elements(*self._notifications_in_container_locator)
        self.assertEqual(1, len(notifications_in_container), 'Expected one notification.')
        # Assert notification is listed in notifications-container
        notification_body_in_container = self.marionette.find_element(*self._notification_body_in_container_locator)
        self.assertEqual(self._notification_body, notification_body_in_container.text, 'The notification body should be "%s", not "%s".' % (self._notification_body, notification_body_in_container.text))

        # Clear the notification by "Clear all"
        notification_clear = self.marionette.find_element(*self._notification_clear_locator)
        notification_clear.tap()

        # Assert there is no notification is listed in notifications-container
        time.sleep(1)
        notifications_in_container = self.marionette.find_elements(*self._notifications_in_container_locator)
        self.assertEqual(0, len(notifications_in_container), 'Expected 0 notifications.')
