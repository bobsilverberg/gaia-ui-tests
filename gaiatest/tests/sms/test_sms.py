# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestSms(GaiaTestCase):

    # Summary page
    _summary_header_locator = ('xpath', "//h1[text()='Messages']")
    _create_new_message_locator = ('id', 'icon-add')

    # Message composition
    _recipients_list_locator = ('id', 'messages-recipients-list')
    _receiver_input_locator = ('css selector', '#messages-recipients-list span.recipient')
    _message_field_locator = ('id', 'messages-input')
    _send_message_button_locator = ('id', 'messages-send-button')
    _message_sending_spinner_locator = (
        'css selector',
        "img[src='style/images/spinningwheel_small_animation.gif']")

    # Conversation view
    _all_messages_locator = ('css selector', '#messages-container li.message')
    _received_message_content_locator = ('css selector', "#messages-container li.message.received")

    def test_sms_send(self):
        """
        This test sends a text message to itself. It waits for a reply message.
        It does not yet clean up after itself but it can handle it.
        https://moztrap.mozilla.org/manage/case/1322/
        """

        _text_message_content = "Automated Test %s" % str(time.time())

        # delete any existing SMS messages to start clean
        self.data_layer.delete_all_sms()

        # temporary workaround for bug 837029
        # launch and then kill messags app, to clear any left-over sms msg notifications
        self.app = self.apps.launch('Messages', False)
        self.apps.kill(self.app)

        # launch the app
        self.app = self.apps.launch('Messages')

        self.wait_for_element_displayed(*self._summary_header_locator)

        # click new message
        create_new_message = self.marionette.find_element(*self._create_new_message_locator)
        create_new_message.tap()

        self.wait_for_element_displayed(*self._recipients_list_locator)
        # First tap on the section to make the field active
        self.marionette.find_element(*self._recipients_list_locator).tap()

        contact_field = self.marionette.find_element(*self._receiver_input_locator)
        contact_field.send_keys(self.testvars['carrier']['phone_number'])

        message_field = self.marionette.find_element(*self._message_field_locator)
        # change the focus to the message field to enable the send button
        message_field.tap()
        message_field.send_keys(_text_message_content)

        #click send
        send_message_button = self.marionette.find_element(*self._send_message_button_locator)
        send_message_button.tap()
        self.wait_for_element_not_present(*self._message_sending_spinner_locator, timeout=120)

        self.wait_for_element_displayed(*self._received_message_content_locator)
        # get the most recent listed and most recent received text message
        received_message = self.marionette.find_elements(
            *self._received_message_content_locator)[-1]

        last_message = self.marionette.find_elements(*self._all_messages_locator)[-1]

        # Check the most recent received message has the same text content
        self.assertEqual(_text_message_content, received_message.text)

        # Check that most recent message is also the most recent received message
        self.assertEqual(received_message.get_attribute('id'),
                         last_message.get_attribute('id'))
