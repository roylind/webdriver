from abc import ABC
import random
import time

from selenium.webdriver.common.by import By

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox


class NotFoundBrowser(Exception):
    pass


class NotFoundInputApplyAllWindows(Exception):
    pass


class Browsers(ABC):
    NAME = None
    WEIGHTS = None

    @property
    def name(self):
        return self.NAME

    @property
    def weights(self):
        return self.WEIGHTS


class Chrome(Browsers):
    NAME = "Google Chrome"
    WEIGHTS = 63


class Opera(Browsers):
    NAME = "Opera"
    WEIGHTS = 2


class Firefox(Browsers):
    NAME = "Mozilla Firefox"
    WEIGHTS = 4


class Edge(Browsers):
    NAME = "Microsoft Edge"
    WEIGHTS = 3


class UserAgentSwitcherRay(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "%7Ba6c4a591-f1b2-4f03-b3ff-767e5bedf4e7%7D.xpi"
        self.allow_browsers = [
            # Chrome(),
            # Opera(),
            Firefox(),
            # Edge()
        ]
        super(UserAgentSwitcherRay, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)
        self.open_page_popup()

    def open_page_popup(self):
        self.web_driver.get("moz-extension://{id_addon}/data/popup/index.html".format(id_addon=self.id_addon))

    def _random_browser(self):
        return random.choices(self.allow_browsers, weights=[browser.weights for browser in self.allow_browsers])[0]

    def _set_browser(self, browser: Browsers):
        self.open_page_popup()
        self._select_browser(browser)
        time.sleep(0.5)
        self._select_version()
        time.sleep(0.5)
        self._apply_all_windows()
        time.sleep(1)

    def _select_browser(self, browser: Browsers):
        self.web_driver.wait_selector("#browser")
        self.web_driver.click("#browser")
        for el_list_browser in self.web_driver.find_elements(By.CSS_SELECTOR, "#browser "
                                                                              "> optgroup:nth-child(1) > option"):
            if el_list_browser.get_attribute("value") in browser.name:
                el_list_browser.click()
                return
        raise NotFoundBrowser

    def _select_version(self):
        self.web_driver.wait_selector("#list > table:nth-child(1) > tbody:nth-child(3) > "
                                      "tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")
        random.choice(self.web_driver.find_elements(By.CSS_SELECTOR,
                    "#list > table:nth-child(1) > tbody:nth-child(3) > tr > td:nth-child(2) > input")[5:25]).click()

    def _apply_all_windows(self):
        for el_input in self.web_driver.find_elements(By.CSS_SELECTOR, "#agent > input"):
            if el_input.get_attribute("data-localized-value") == "applyAllWindows":
                el_input.click()
                return
        raise NotFoundInputApplyAllWindows

    def change_user_agent(self):
        self._set_browser(self._random_browser())




