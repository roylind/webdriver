import glob
import time
import json

from webdriver.firefox.driver import Firefox
from webdriver.firefox.exceptions import NotFoundAddon


class AddonFirefox:

    def __init__(self, web_driver: Firefox):
        self.web_driver = web_driver
        time.sleep(3)
        self.list_id_addons = []

    def search_addon(self, name):
        try:
            return self._search_addon_in_prefs(name)
        except NotFoundAddon:
            return self._search_addon_in_prefs(name)

    def _search_addon_in_prefs(self, name):
        t_name = name.replace("%7B", "{").replace("%7D", "}").rstrip(".xpi")
        with open(self.web_driver.path_profile + "/prefs.js", "r") as f:
            for line in f:
                if line.find('user_pref("extensions.webextensions.uuids", ') == 0:
                    line = line.replace('user_pref("extensions.webextensions.uuids", "', '')
                    line = line.rstrip()
                    line = line.rstrip("\");")
                    line = line.replace('\\\"', '"')
                    extensions_uuids = json.loads(line)
                    if t_name in extensions_uuids.keys():
                        return extensions_uuids[t_name]
                    else:
                        raise NotFoundAddon
        raise NotFoundAddon

    def _search_addon_in_storage(self, name):
        self._get_list_id_addons()
        for id_addon in self.list_id_addons:
            self.web_driver.get("moz-extension://{id_addon}/".format(id_addon=id_addon))
            if name in self.web_driver.all_html():
                return id_addon
        raise NotFoundAddon

    def _get_list_id_addons(self):
        self.list_id_addons = []
        for path in glob.glob(self.web_driver.path_profile + "/storage/default/moz-extension*"):
            id_addon = path.replace("\\", "/").split("/")[-1].split("moz-extension+++")[1].split("^")[0]
            self.list_id_addons.append(id_addon)


