# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.email.app import Email


class TestSetupActiveSync(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_setup_active_sync_email(self):
        # setup ActiveSync account

        self.email = Email(self.marionette)
        self.email.launch()

        setup = self.email.tap_manual_setup()
        setup.type_name(self.testvars['email']['ActiveSync']['name'])
        setup.type_email(self.testvars['email']['ActiveSync']['email'])
        setup.type_password(self.testvars['email']['ActiveSync']['password'])

        setup.select_account_type('ActiveSync')

        setup.type_activesync_hostname(self.testvars['email']['ActiveSync']['active_sync_hostname'])
        setup.type_activesync_name(self.testvars['email']['ActiveSync']['active_sync_username'])

        setup.tap_next()
        setup.wait_for_setup_complete()
        setup.tap_continue()
        self.email.wait_for_header_area()

        # check header area
        self.assertTrue(self.email.header.is_compose_visible)
        self.assertTrue(self.email.header.is_menu_visible)
        self.assertEqual(self.email.header.label, 'Inbox')

        # check toolbar area
        self.assertTrue(self.email.toolbar.is_edit_visible)
        self.assertTrue(self.email.toolbar.is_refresh_visible)

        # check account has emails
        self.email.wait_for_emails_to_sync()
        self.assertGreater(len(self.email.mails), 0)
