from abc import ABC
import random
import time

from selenium.webdriver.common.by import By

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox


class NotFoundCheckBoxAdvancedSettings(Exception):
    pass


class CanvasBlocker(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "CanvasBlocker@kkapsner.de.xpi"

        super(CanvasBlocker, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)

    def _open_page_preset(self):
        self.web_driver.get("moz-extension://{id_addon}/options/presets.html".format(id_addon=self.id_addon))

    def _open_page_options(self):
        self.web_driver.get("moz-extension://{id_addon}/options/options.html".format(id_addon=self.id_addon))

    def set_maximum_protection(self):
        self._open_page_preset()
        self.web_driver.click("div.max_protection > button", timeout=10)
        self.web_driver.click("div.recaptcha > button", timeout=10)

    def _enable_advanced_settings(self):
        self._open_page_options()
        _css_selector_checkbox = "input.setting[data-storage-name='displayAdvancedSettings']"
        self.web_driver.wait_selector(_css_selector_checkbox, timeout=10)
        if not self.web_driver.find_element(By.CSS_SELECTOR, _css_selector_checkbox).is_selected():
            self.web_driver.find_element(By.CSS_SELECTOR, _css_selector_checkbox).click()

    def set_persistent_random(self):
        self._enable_advanced_settings()
        self.web_driver.click("select.setting[data-storage-name='rng']", timeout=10)
        self.web_driver.click("select.setting[data-storage-name='rng'] > option[value='persistent']", timeout=10)
        _css_selector_checkbox_save_rnd = "input.setting[data-storage-name='storePersistentRnd']"
        if not self.web_driver.find_element(By.CSS_SELECTOR, _css_selector_checkbox_save_rnd).is_selected():
            self.web_driver.click(_css_selector_checkbox_save_rnd, timeout=10)
