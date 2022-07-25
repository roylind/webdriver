import time

import pyperclip
from pydantic import BaseModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox


class Rule(BaseModel):
    url: str
    script: str = ""


class CodeInjector(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "%7Bb12a78ef-3319-45fa-800e-a7efa56b6da4%7D.xpi"
        super(CodeInjector, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)

    def _open_main_page(self):
        if self.web_driver.current_url \
                != "moz-extension://{id_addon}/html/browser-action.html".format(id_addon=self.id_addon):
            self.web_driver.get("moz-extension://{id_addon}/html/browser-action.html".format(id_addon=self.id_addon))

        WebDriverWait(self.web_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".rules-controls"))
        )

    def get_rules_only_url(self):
        self._open_main_page()
        result_list = []
        for el in self.web_driver.find_elements(By.CSS_SELECTOR, ".rules-list > .rule"):
            result_list.append(Rule(url=el.find_element(By.CSS_SELECTOR, ".r-name").get_attribute('innerText')))
        return result_list

    def add_rule_script(self, url: str, script: str, on_page_load: bool = True):
        self._open_main_page()

        WebDriverWait(self.web_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-name="btn-rules-add"]'))
        ).click()

        WebDriverWait(self.web_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#editor"))
        )
        self.web_driver.find_element(By.XPATH, '//input[@data-name="txt-editor-selector"]').send_keys(url)

        editor_js = self.web_driver.find_element(By.CSS_SELECTOR,
                                                 "#editor-js > div.monaco-editor,no-user-select,showUnused,vs")
        pyperclip.copy(script)
        actions = ActionChains(self.web_driver)
        actions.move_to_element(editor_js)
        actions.click(editor_js)
        actions.key_down(Keys.CONTROL)
        actions.key_down("a")
        actions.key_up("a")
        actions.key_up(Keys.CONTROL)
        actions.key_down(Keys.CONTROL)
        actions.key_down("v")
        actions.key_up("v")
        actions.key_up(Keys.CONTROL)
        actions.perform()

        if not on_page_load:
            self.web_driver.find_element(By.XPATH, '//input[@data-name="cb-editor-onload"]').click()

        button_save = self.web_driver.find_element(By.XPATH, '//button[@data-name="btn-editor-save"]')
        ActionChains(self.web_driver).move_to_element(button_save).click().perform()
        time.sleep(10)
