import time
import random

from webdriver.firefox.addons.base_addon import AddonFirefox
from webdriver.firefox.driver import Firefox


class NoConnectToVpn(Exception):
    pass


class BrowsecVpn(AddonFirefox):

    def __init__(self, web_driver: Firefox):
        self.addon_name: str = "browsec@browsec.com.xpi"
        super(BrowsecVpn, self).__init__(web_driver)
        self.id_addon: str = self.search_addon(self.addon_name)
        self.open_page_enable_vpn()

    def open_page_enable_vpn(self):
        self.web_driver.get("moz-extension://{id_addon}/popup/popup.html".format(id_addon=self.id_addon))

    def is_active_vpn(self):
        self.open_page_enable_vpn()
        self.web_driver.wait_selector("page-switch", 10)
        js_is_active = 'return document.querySelector("page-switch").shadowRoot' \
                       '.querySelector("main-index").shadowRoot' \
                       '.querySelector("c-switch").className;'
        return self.web_driver.execute_script(js_is_active) == "on"

    def enable_vpn(self):
        if self.is_active_vpn():
            return

        self.open_page_enable_vpn()
        self.web_driver.wait_selector("page-switch", 10)

        js_enable_vpn = 'document.querySelector("page-switch").shadowRoot' \
                        '.querySelector("main-index").shadowRoot' \
                        '.querySelector("index-home").shadowRoot' \
                        '.querySelector("div.Inactive_Button").click()'

        js_change_server = 'document.querySelector("page-switch").shadowRoot' \
                           '.querySelector("main-index").shadowRoot' \
                           '.querySelector("index-home").shadowRoot' \
                           '.querySelector(".ChangeButton").click()'

        js_click_server = 'document.querySelector("page-switch").shadowRoot' \
                          '.querySelector("main-index").shadowRoot' \
                          '.querySelector("index-locations").shadowRoot' \
                          '.querySelector(".Sections > div:nth-child({random1to4}) > index-locations-element")' \
                          '.shadowRoot.querySelector(".In").click()'

        js_click_server = js_click_server.format(random1to4=random.randint(1, 4))

        self.web_driver.execute_script(js_enable_vpn)
        time.sleep(2)
        if not self.is_active_vpn():
            raise NoConnectToVpn

        self.web_driver.execute_script(js_change_server)
        time.sleep(1)
        self.web_driver.execute_script(js_click_server)
        time.sleep(1)

