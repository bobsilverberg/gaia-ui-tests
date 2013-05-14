# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestWallpaper(GaiaTestCase):

    # settings menu
    _display_locator = ('id', 'menuItem-display')

    # display menu
    _visible_display_menu_locator = ('css selector', '#display.current')
    _wallpaper_preview_locator = ('id', 'wallpaper-preview')
    _wallpaper_button_locator = ('css selector', "a[data-value='0']")
    _wallpaper_title_locator = ('css selector', "h1[data-l10n-id='select-wallpaper']")
    _stock_wallpapers_locator = ('css selector', "div[class='wallpaper']")
    _wallpaper_frame_locator = ('css selector', "iframe[src^='app://wallpaper'][src$='pick.html']")
    _settings_frame_locator = ('css selector', "iframe[src^='app://settings'][src$='index.html#root']")

    # default wallpaper
    _default_wallpaper_src = None

    def setUp(self):
        GaiaTestCase.setUp(self)

    def test_change_wallpaper(self):
        # https://moztrap.mozilla.org/manage/case/3449/

        # launch the Settings app
        self.app = self.apps.launch('Settings')

        self.wait_for_element_displayed(*self._display_locator)
        display_item = self.marionette.find_element(*self._display_locator)

        # TODO Bug 847946 - scrollIntoView() or scrollIntoView(true) scrolls to the element next to the giving one
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [display_item])
        self.marionette.tap(display_item)

        #  Wait for the display menu to be visible
        self.wait_for_element_displayed(*self._visible_display_menu_locator)

        # wait for the wallpaper preview to be visible
        self.wait_for_element_displayed(*self._wallpaper_preview_locator)

        # save the default wallpaper's src
        wallpaper_preview = self.marionette.find_element(*self._wallpaper_preview_locator)
        self._default_wallpaper_src = wallpaper_preview.get_attribute('src')

        # Send the pick event to system
        self.marionette.tap(wallpaper_preview)

        # switch to the system app
        self.marionette.switch_to_frame()

        # choose the source as wallpaper app
        self.wait_for_element_displayed(*self._wallpaper_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._wallpaper_button_locator))

        # switch to the wallpaper app
        self.wait_for_element_displayed(*self._wallpaper_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._wallpaper_frame_locator))

        # pick a wallpaper
        self.wait_for_element_displayed(*self._stock_wallpapers_locator)
        stock_wallpapers = self.marionette.find_elements(*self._stock_wallpapers_locator)
        self.assertGreater(len(stock_wallpapers), 0, 'no stock wallpapers found')
        self.marionette.tap(stock_wallpapers[3])

        # switch to the system app
        self.marionette.switch_to_frame()

        # switch to the setting app
        self.marionette.switch_to_frame(self.marionette.find_element(*self._settings_frame_locator))
        self.wait_for_element_displayed(*self._wallpaper_preview_locator)

        # save the new wallpaper's src
        new_wallpaper = self.marionette.find_element(*self._wallpaper_preview_locator).get_attribute('src')

        # verify the change of wallpaper
        self.assertFalse(new_wallpaper == self._default_wallpaper_src, 'Wallpaper has not changed from default.')

    def tearDown(self):
        # reset to the default wallpaper only if we have saved it
        if self._default_wallpaper_src is not None:
            self.marionette.execute_script("navigator.mozSettings.createLock().set({'wallpaper.image' : arguments[0]});", [self._default_wallpaper_src])

        GaiaTestCase.tearDown(self)
