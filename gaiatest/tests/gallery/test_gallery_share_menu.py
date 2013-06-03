# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestGalleryShareMenu(GaiaTestCase):

    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_image_locator = ('css selector', '#frame2 > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')
    _share_button_locator = ('id', 'fullscreen-share-button')
    _back_button_locator = ('id', 'fullscreen-back-button')

    _share_with_list_locator = ('css selector', '#list-menu-root a[role="button"]')
    _cancel_button_locator = ('css selector', '#list-menu-root button[data-action="cancel"]')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_click_share_button(self):
        self.wait_for_element_displayed(*self._gallery_items_locator)

        first_gallery_item = self.marionette.find_elements(*self._gallery_items_locator)[0]

        first_gallery_item.tap()
        self.wait_for_element_displayed(*self._current_image_locator)

        current_image = self.marionette.find_element(*self._current_image_locator)
        photos_toolbar = self.marionette.find_element(*self._photos_toolbar_locator)

        self.assertIsNotNone(current_image.get_attribute('src'))
        self.assertTrue(photos_toolbar.is_displayed())

        # click on share button and check the element is correct
        self.marionette.find_element(*self._share_button_locator).tap()

        # switch to home frame and check the result
        self.marionette.switch_to_frame()

        # wait for Share with Menu is rendered
        self.wait_for_element_displayed(*self._share_with_list_locator)
        share_with_list = self.marionette.find_elements(*self._share_with_list_locator)
        self.wait_for_element_displayed(*self._cancel_button_locator)

        self.assertGreater(len(share_with_list), 0)

        self.marionette.find_element(*self._cancel_button_locator).tap()

        self.marionette.switch_to_frame(self.app.frame_id)

        self.wait_for_element_displayed(*self._back_button_locator)
        self.marionette.find_element(*self._back_button_locator).tap()

        self.wait_for_element_displayed(*self._gallery_items_locator)
        first_gallery_item = self.marionette.find_elements(*self._gallery_items_locator)[0]
        self.assertTrue(first_gallery_item.is_displayed())

    def tearDown(self):
        GaiaTestCase.tearDown(self)
