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


class WMRFast(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "%7B9cb595df-8912-4a54-bf3e-5da5bdfa5999%7D.xpi"
        super(WMRFast, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)

    def open_main_page(self):
        if self.web_driver.current_url \
                != "moz-extension://{id_addon}/popup/wmrfast.html".format(id_addon=self.id_addon):
            self.web_driver.get("moz-extension://{id_addon}/popup/wmrfast.html".format(id_addon=self.id_addon))

        # WebDriverWait(self.web_driver, 20).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".rules-controls"))
        # )

