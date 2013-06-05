# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class SearchResults(Base):

    _search_results_area_locator = ('id', 'search-results')
    _search_results_loading_locator = ('css selector', 'div.loading')
    _search_result_locator = ('css selector', '#search-results li.item')
    _filter_button_locator = ('css selector', '#site-header .header-button.filter')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_not_present(*self._search_results_loading_locator)

    def tap_filter(self):
        self.marionette.find_element(*self._filter_button_locator).tap()
        return FilterResults(self.marionette)

    @property
    def search_results(self):
        return [self.Result(marionette=self.marionette, element=result)
                for result in self.marionette.find_elements(*self._search_result_locator)]

    class Result(PageRegion):

        _name_locator = ('css selector', '.info > h3')
        _author_locator = ('css selector', '.info .author')
        _install_button_locator = ('css selector', '.button.product.install')
        _price_locator = ('css selector', '.premium.button.product')

        @property
        def name(self):
            return self.root_element.find_element(*self._name_locator).text

        @property
        def author(self):
            return self.root_element.find_element(*self._author_locator).text

        @property
        def install_button_text(self):
            return self.root_element.find_element(*self._install_button_locator).text

        def tap_install_button(self):
            self.root_element.find_element(*self._install_button_locator).tap()
            self.marionette.switch_to_frame()

        @property
        def price(self):
            return self.root_element.find_element(*self._price_locator).text


class FilterResults(Base):

    _apply_locator = ('css selector', '.footer-action > .apply')
    _all_price_filter_locator = ('css selector', '#filter-prices > li:nth-child(1) > a')
    _free_price_filter_locator = ('css selector', '#filter-prices > li:nth-child(2) > a')
    _paid_price_filter_locator = ('css selector', '#filter-prices > li:nth-child(3) > a')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._apply_locator)

    def by_price(self, filter_name):
        self.marionette.find_element(*getattr(self, '_%s_price_filter_locator' % filter_name)).tap()

    def tap_apply(self):
        self.marionette.find_element(*self._apply_locator).tap()
        return SearchResults(self.marionette)
