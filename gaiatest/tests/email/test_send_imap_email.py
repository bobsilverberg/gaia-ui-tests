# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.email.app import Email


class TestSendIMAPEmail(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

        self.email = Email(self.marionette)
        self.email.launch()

        # setup IMAP account
        self.email.setup_IMAP_email(self.testvars['email']['IMAP'])

    def test_send_imap_email(self):

        curr_time = repr(time.time()).replace('.', '')
        new_email = self.email.header.tap_compose()

        new_email.type_to(self.testvars['email']['IMAP']['email'])
        new_email.type_subject('test email %s' % curr_time)
        new_email.type_body('Lorem ipsum dolor sit amet %s' % curr_time)

        self.email = new_email.tap_send()

        # wait for the email to be sent before we tap refresh
        time.sleep(10)
        self.email.toolbar.tap_refresh()
        self.email.wait_for_emails_to_sync()

        # assert that the email app subject is in the email list
        self.assertIn('test email %s' % curr_time, [mail.subject for mail in self.email.mails])

        read_email = self.email.mails[0].tap_subject()

        self.assertEqual('Lorem ipsum dolor sit amet %s' % curr_time, read_email.body)
        self.assertEqual('test email %s' % curr_time, read_email.subject)

    def tearDown(self):
        GaiaTestCase.tearDown(self)
