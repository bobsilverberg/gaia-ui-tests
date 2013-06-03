# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.phone.app import Phone


class TestDialerAddContact(GaiaTestCase):

    # Dialer app
    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _add_new_contact_button_locator = ('id', 'keypad-callbar-add-contact')
    _contacts_view_locator = ('id', 'option-contacts')
    _create_new_contact_locator = ('id', 'create-new-contact-menuitem')

    # Header buttons
    _done_button_locator = ('id', 'save-button')

    # New/Edit contact fields
    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _phone_field_locator = ('id', 'number_0')

    # Contact details panel
    _contact_list_locator = ('css selector', '#contacts-list-G li')
    _contact_name_title_locator = ('id', 'contact-name-title')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    # frames
    _new_contact_frame_locator = ('css selector', "iframe[src^='app://communications'][src$='contacts/index.html?new']")
    _contact_frame_locator = ('css selector', '#iframe-contacts')
    _keypad_frame_locator = ('css selector', "iframe[src^='app://communications'][src$='dialer/index.html#keyboard-view']")

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.contact = MockContact()

        # launch the Phone app
        self.phone = Phone(self.marionette)
        self.phone.launch()

    def test_dialer_add_contact(self):

        self.wait_for_element_displayed(*self._keyboard_container_locator)

        # Dial number
        self.phone.keypad.dial_phone_number(self.contact['tel']['value'])

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(*self._phone_number_view_locator)
        self.assertEqual(phone_view.get_attribute('value'), self.contact['tel']['value'])

        # Click Add contact button
        self.wait_for_element_displayed(*self._add_new_contact_button_locator)
        self.marionette.find_element(*self._add_new_contact_button_locator).tap()

        # Tap on "Create New Contact"
        self.wait_for_element_displayed(*self._create_new_contact_locator)
        create_new_contact = self.marionette.find_element(*self._create_new_contact_locator)
        self.marionette.tap(create_new_contact)

        # Switch to add contacts frame
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._new_contact_frame_locator)
        new_contact_frame = self.marionette.find_element(*self._new_contact_frame_locator)
        self.marionette.switch_to_frame(new_contact_frame)

        # Enter data into fields
        self.wait_for_element_displayed(*self._done_button_locator)
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])

        # Click Done button
        self.marionette.find_element(*self._done_button_locator).tap()

        # Switch back to keypad-view
        self.marionette.switch_to_frame()

        self.wait_for_element_present(*self._keypad_frame_locator)
        keypad_frame = self.marionette.find_element(*self._keypad_frame_locator)
        self.marionette.switch_to_frame(keypad_frame)

        #Go to Contact list and Verify result
        self.marionette.find_element(*self._contacts_view_locator).tap()

        # switch to contact frame
        self.wait_for_element_present(*self._contact_frame_locator)
        contact_frame = self.marionette.find_element(*self._contact_frame_locator)
        self.marionette.switch_to_frame(contact_frame)

        # Check only one contact is created
        self.wait_for_element_displayed(*self._contact_list_locator)
        contact_list = self.marionette.find_elements(*self._contact_list_locator)
        self.assertEqual(1, len(contact_list))

        #  Tap on the new contact
        contact_list[0].tap()

        # wait for contact details to be loaded
        self.wait_for_element_displayed(*self._call_phone_number_button_locator)

        # Verify full name
        full_name = self.contact['givenName'] + " " + self.contact['familyName']
        self.assertEqual(self.marionette.find_element(*self._contact_name_title_locator).text,
                         full_name)

        # Verify phone number
        self.assertEqual(self.marionette.find_element(*self._call_phone_number_button_locator).text,
                         self.contact['tel']['value'])
