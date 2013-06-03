# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts


class TestContacts(GaiaTestCase):

    # Select from: dialog
    _gallery_button_locator = ('xpath', "//a[text()='Gallery']")

    # Gallery
    _gallery_frame_locator = ('css selector', "iframe[src^='app://gallery'][src$='index.html#pick']")
    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _gallery_crop_done_button_locator = ('id', 'crop-done-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.contact = MockContact()
        self.data_layer.insert_contact(self.contact)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

    def test_add_photo_from_gallery_to_contact(self):
        # https://moztrap.mozilla.org/manage/case/5551/

        contacts_app = Contacts(self.marionette)
        contacts_app.launch()

        contact_details = contacts_app.contact(self.contact['givenName']).tap()

        full_name = ' '.join([self.contact['givenName'], self.contact['familyName']])

        self.assertEqual(full_name, contact_details.full_name)

        saved_contact_image_style = contact_details.image_style

        edit_contact = contact_details.tap_edit()

        self.assertEqual('Edit contact', edit_contact.title)

        saved_picture_style = edit_contact.picture_style

        edit_contact.tap_picture()

        # switch to the system app
        self.marionette.switch_to_frame()

        # choose the source as gallery app
        self.wait_for_element_displayed(*self._gallery_button_locator)
        self.marionette.find_element(*self._gallery_button_locator).tap()

        # switch to the gallery app
        self.wait_for_element_displayed(*self._gallery_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._gallery_frame_locator))

        self.wait_for_element_displayed(*self._gallery_items_locator)
        gallery_items = self.marionette.find_elements(*self._gallery_items_locator)
        self.assertGreater(len(gallery_items), 0, 'No photos were found in the gallery.')
        gallery_items[0].tap()

        self.wait_for_element_displayed(*self._gallery_crop_done_button_locator)
        self.marionette.find_element(*self._gallery_crop_done_button_locator).tap()

        # switch back to the contacts app
        contacts_app.launch()

        self.assertEqual('Edit contact', edit_contact.title)

        edit_contact.wait_for_image_to_load()

        new_picture_style = edit_contact.picture_style
        self.assertNotEqual(new_picture_style, saved_picture_style,
                            'The picture associated with the contact was not changed.')

        contact_details = edit_contact.tap_update()

        self.assertEqual(full_name, contact_details.full_name)

        self.assertNotEqual(contact_details.image_style, saved_contact_image_style,
                            'The picture associated with the contact was not changed.')
