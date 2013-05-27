# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class NewEmail(Base):
    # Write new email

    _to_locator = ("css selector", "#cardContainer .card.center .cmp-to-text.cmp-addr-text")
    _cc_locator = ("css selector", "#cardContainer .card.center .cmp-cc-text.cmp-addr-text")
    _bcc_locator = ("css selector", "#cardContainer .card.center .cmp-bcc-text.cmp-addr-text")
    _subject_locator = ("css selector", "#cardContainer .card.center .cmp-subject-text")
    _body_locator = ("css selector", "#cardContainer .card.center .cmp-body-text")
    _send_locator = ("css selector", "#cardContainer .card.center .icon.icon-send")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._to_locator)

    def type_to(self, value):
        el = self.marionette.find_element(*self._to_locator)
        el.clear()
        el.send_keys(value)

    def type_cc(self, value):
        el = self.marionette.find_element(*self._cc_locator)
        el.clear()
        el.send_keys(value)

    def type_bcc(self, value):
        el = self.marionette.find_element(*self._bcc_locator)
        el.clear()
        el.send_keys(value)

    def type_subject(self, value):
        el = self.marionette.find_element(*self._subject_locator)
        el.clear()
        el.send_keys(value)

    def type_body(self, value):
        el = self.marionette.find_element(*self._body_locator)
        el.clear()
        el.send_keys(value)

    def tap_send(self):
        self.marionette.find_element(*self._send_locator).tap()
        from gaiatest.apps.email.app import Email
        email = Email(self.marionette)
        email.wait_for_header_area()
        return email
