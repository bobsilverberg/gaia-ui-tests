# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.email.app import Email


class TestSetupManualEmail(GaiaTestCase):

    email_configured = False

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

        self.email = Email(self.marionette)
        self.email.launch()

    def test_setup_imap_email(self):
        # setup IMAP account

        setup = self.email.tap_manual_setup()
        setup.type_name(self.testvars['email']['IMAP']['name'])
        setup.type_email(self.testvars['email']['IMAP']['email'])
        setup.type_password(self.testvars['email']['IMAP']['password'])

        setup.select_account_type('IMAP+SMTP')

        setup.type_imap_hostname(self.testvars['email']['IMAP']['imap_hostname'])
        setup.type_imap_name(self.testvars['email']['IMAP']['imap_name'])
        setup.type_imap_port(self.testvars['email']['IMAP']['imap_port'])

        setup.type_smtp_hostname(self.testvars['email']['IMAP']['smtp_hostname'])
        setup.type_smtp_name(self.testvars['email']['IMAP']['smtp_name'])
        setup.type_smtp_port(self.testvars['email']['IMAP']['smtp_port'])

        setup.tap_next()
        setup.wait_for_setup_complete()
        setup.tap_continue()
        self.email.wait_for_header_area()

        self.email_configured = True

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

    def tearDown(self):
        GaiaTestCase.tearDown(self)
