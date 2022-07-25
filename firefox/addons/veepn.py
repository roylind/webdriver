import time
import random

from selenium.webdriver.common.by import By

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox

random.seed(version=2)


class ConnectedTimeOut(Exception):
    pass


class NotFoundRegion(Exception):
    pass


class WrongRegion(Exception):
    pass


class Regions:
    Paris = "Paris"
    Amsterdam = "Amsterdam"
    Singapore = "Singapore"
    Queenstown = "Queenstown"
    London = "London"
    Moscow = "Moscow"
    Virginia = "Virginia"
    Oregon = "Oregon"

    def __init__(self):
        self.regions = [
            self.Paris,
            self.Amsterdam,
            self.Singapore,
            self.Queenstown,
            self.London,
            self.Moscow,
            self.Virginia,
            self.Oregon
        ]

    def __getitem__(self, item):
        return self.regions[item]

    def __len__(self):
        return len(self.regions)


class VeePN(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "%7B94ed9bbf-a1e2-4e58-81ae-cd16dad818d8%7D.xpi"
        super(VeePN, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)

    def _open_main_page(self):
        if self.web_driver.current_url \
                != "moz-extension://{id_addon}/html/foreground.html".format(id_addon=self.id_addon):
            self.web_driver.get("moz-extension://{id_addon}/html/foreground.html".format(id_addon=self.id_addon))

    def run_vpn(self, region: str = ""):
        if region == "":
            region = random.choice(Regions())
        if region not in Regions():
            raise WrongRegion
        self._open_main_page()
        self.web_driver.wait_any_selector(["#mainBtn", ".next"], timeout=10)
        if self.web_driver.check_selector(".next"):
            self.web_driver.click("button.next")
            self.web_driver.click("button.next")
            self.web_driver.click("button.next")
        self.web_driver.click(".current-region")
        for el_regions in self.web_driver.find_elements(By.CSS_SELECTOR, "#region-list > .region-item")[:8]:
            if region in el_regions.get_attribute("innerText"):
                if "active" in el_regions.get_attribute("class"):
                    self.web_driver.click(".compContainer")
                else:
                    el_regions.click()
                break
        else:
            raise NotFoundRegion

        self.web_driver.wait_selector("#mainBtn", timeout=5)
        if self.web_driver.find_element(By.CSS_SELECTOR, "#mainBtn").get_attribute("class") == "connected":
            return True
        self.web_driver.click("#mainBtn")
        for _ in range(30):
            time.sleep(1)
            if self.web_driver.find_element(By.CSS_SELECTOR, "#mainBtn").get_attribute("class") == "connected":
                break
        else:
            raise ConnectedTimeOut



