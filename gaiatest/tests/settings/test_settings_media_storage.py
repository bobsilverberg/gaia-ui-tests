# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsMediaStorage(GaiaTestCase):

    # Settings locators
    _media_storage_locator = ('id', 'menuItem-mediaStorage')

    # Media storage locators
    _music_space_locator = ('css selector', '.color-music > a > .size')
    _pictures_space_locator = ('css selector', '.color-pictures > a > .size')
    _movies_space_locator = ('css selector', '.color-videos > a > .size')

    def test_settings_media_storage(self):

        # Access 'Media storage' in Settings
        self.access_media_storage_settings()

        music = self.marionette.find_element(*self._music_space_locator)
        pictures = self.marionette.find_element(*self._pictures_space_locator)
        movies = self.marionette.find_element(*self._movies_space_locator)

        # Check that no media is on the device
        self.assertEqual(music.text, '0 B')
        self.assertEqual(pictures.text, '0 B')
        self.assertEqual(movies.text, '0 B')

        # Close the settings application
        self.apps.kill(self.app)

        # Push media to the device
        self.push_resource('VID_0001.3gp', destination='DCIM/100MZLLA')
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')
        self.push_resource('MUS_0001.mp3', destination='DCIM/100MZLLA')

        # Access 'Media storage' in Settings
        self.access_media_storage_settings()

        music = self.marionette.find_element(*self._music_space_locator)
        pictures = self.marionette.find_element(*self._pictures_space_locator)
        movies = self.marionette.find_element(*self._movies_space_locator)

        # Check that media storage has updated to reflect the newly pushed media
        self.assertEqual(music.text, '120 KB')
        self.assertEqual(pictures.text, '348 KB')
        self.assertEqual(movies.text, '120 KB')

    def access_media_storage_settings(self):

        # Launch the Settings application
        self.app = self.apps.launch('Settings')

        # Wait for Media storage menu to be displayed
        self.wait_for_element_displayed(*self._media_storage_locator)
        media_storage_item = self.marionette.find_element(*self._media_storage_locator)

        # Tap on 'Media storage'
        media_storage_item.tap()

        self.wait_for_element_displayed(*self._music_space_locator)
        self.wait_for_element_displayed(*self._pictures_space_locator)
        self.wait_for_element_displayed(*self._movies_space_locator)
