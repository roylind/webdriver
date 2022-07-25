from pydantic import BaseModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox


class uBlock(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "uBlock0@raymondhill.net.xpi"
        super(uBlock, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)
        self._open_settings_page()

    def _open_settings_page(self):
        if self.web_driver.current_url \
                != "moz-extension://{id_addon}/settings.html".format(id_addon=self.id_addon):
            self.web_driver.get("moz-extension://{id_addon}/settings.html".format(id_addon=self.id_addon))

        WebDriverWait(self.web_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.fieldset:nth-child(1)"))
        )

    def _open_white_list_page(self):
        # Эту страницу необходимо перезагружать всегда иначе будет баг
        self.web_driver.get("moz-extension://{id_addon}/whitelist.html".format(id_addon=self.id_addon))
        WebDriverWait(self.web_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#whitelist"))
        )

    def add_white_list(self, url: str):
        self._open_white_list_page()
        text_while_list = self.web_driver.find_element(By.CSS_SELECTOR, "textarea")
        ActionChains(self.web_driver) \
            .move_to_element(text_while_list) \
            .key_down(Keys.CONTROL) \
            .key_down(Keys.END) \
            .key_up(Keys.END) \
            .key_up(Keys.CONTROL) \
            .send_keys(Keys.ENTER) \
            .perform()
        text_while_list.send_keys(url)
        self.web_driver.find_element(By.CSS_SELECTOR, "#whitelistApply").click()

    def disable_java_script(self):
        self._open_settings_page()
        checkbox_js = self.web_driver.find_element(By.XPATH, '//input[@data-setting-name="noScripting"]')
        if not checkbox_js.is_selected():
            checkbox_js.click()

    def block_media_elements(self, size_kb: int):
        self._open_settings_page()

        input_media_size = self.web_driver.find_element(By.XPATH, '//input[@data-setting-name="largeMediaSize"]')
        for _ in range(10):
            input_media_size.send_keys(Keys.BACKSPACE)
        input_media_size.send_keys(str(size_kb))

        checkbox_media = self.web_driver.find_element(By.XPATH, '//input[@data-setting-name="noLargeMedia"]')
        if not checkbox_media.is_selected():
            checkbox_media.click()
