# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class ReadEmail(Base):

    _body_locator = ('css selector', '.card.center .msg-body-content')
    _subject_locator = ('css selector', '.card.center .msg-envelope-subject')

    @property
    def body(self):
        return self.marionette.find_element(*self._body_locator).text

    @property
    def subject(self):
        return self.marionette.find_element(*self._subject_locator).text
