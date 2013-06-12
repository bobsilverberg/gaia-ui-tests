# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.settings.app import Settings


class SettingsPanel(Settings):

    _back_button_locator = ('css selector', ".current header > a")

    def go_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()
        settings = Settings(self.marionette)
        settings.launch()
        return settings
