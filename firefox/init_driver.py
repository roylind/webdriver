import os.path
import glob
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from os.path import basename, isfile
import re

import psutil
from selenium.webdriver.firefox.webdriver import WebDriver as Original_WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

from webdriver.other.check_open_port import search_close_port
from webdriver.firefox.profile_firefox_read_only import FileProfileFirefoxReadOnly as FirefoxProfiles
from webdriver.firefox.exceptions import *
from webdriver.other.process_control import kill_only_child_proc, kill_proc_conditions
from webdriver.firefox.common import *
from webdriver.firefox.fork_firefox_profile import NotMoveFirefoxProfile


class InitFirefox(Original_WebDriver):

    def __init__(self, profile, disable_img=False, private=False, proxy: str = ""):
        if proxy != "":
            template = "^(http|https|socks4|socks5):\/\/(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)" \
                       "{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):([0-9]{1,5})$"
            valid = re.match(template, proxy)
            if valid is not None:
                if int(valid.group(5)) > 65535 or int(valid.group(5)) < 0:
                    raise BadProxy
            else:
                raise BadProxy

        self.path_geckodriver = PATH_GECKODRIVER
        self.firefox_binary_full_path = FIREFOX_BINARY_FULL_PATH
        self.firefox_binary = FirefoxBinary(self.firefox_binary_full_path)
        self.profile = profile

        self.path_profile = self._get_path_prof()

        # Иначе настройки set_preference багуют
        if isfile(self.path_profile + "/user.js"):
            os.remove(self.path_profile + "/user.js")
        if isfile(self.path_profile + "/Invalidprefs.js"):
            os.remove(self.path_profile + "/Invalidprefs.js")
        for file in glob.glob(self.path_profile + "/user.geckodriver_backup*"):
            os.remove(file)
        self.port_marionette = search_close_port()
        self.path_profile = self.path_profile.replace("\\", "/")
        firefox_profile = NotMoveFirefoxProfile(profile_directory=self.path_profile)

        # print(port_marionette)
        firefox_profile.set_preference("marionette.port", self.port_marionette)
        firefox_profile.set_preference("dom.webdriver.enabled", False)
        firefox_profile.set_preference("marionette.enabled", False)

        # Что бы не выскакивало окно при поаторной отправке формыв, версия выше 84
        firefox_profile.set_preference("dom.confirm_repost.testing.always_accept", True)

        firefox_profile.set_preference("dom.allow_scripts_to_close_windows", True)

        if proxy == "":
            firefox_profile.set_preference("network.proxy.type", 5)
            firefox_profile.set_preference("network.proxy.share_proxy_settings", False)
        else:
            firefox_profile.set_preference("network.proxy.type", 1)
            proxy_address = proxy.split("//")[1].split(":")[0]
            proxy_port = int(proxy.split("//")[1].split(":")[1])
            if proxy.find("http://") == 0 or proxy.find("https://") == 0:

                firefox_profile.set_preference("network.proxy.share_proxy_settings", True)
                firefox_profile.set_preference("network.proxy.http", proxy_address)
                firefox_profile.set_preference("network.proxy.http_port", proxy_port)
                firefox_profile.set_preference("network.proxy.ftp", proxy_address)
                firefox_profile.set_preference("network.proxy.ftp_port", proxy_port)
                firefox_profile.set_preference("network.proxy.ssl", proxy_address)
                firefox_profile.set_preference("network.proxy.ssl_port", proxy_port)
                firefox_profile.set_preference("network.proxy.socks", "")
                firefox_profile.set_preference("network.proxy.socks_port", 0)
                firefox_profile.set_preference("network.proxy.socks_version", 5)

            elif proxy.find("socks4://") == 0 or proxy.find("socks5://") == 0:
                firefox_profile.set_preference("network.proxy.http", "")
                firefox_profile.set_preference("network.proxy.http_port", 0)
                firefox_profile.set_preference("network.proxy.ftp", "")
                firefox_profile.set_preference("network.proxy.ftp_port", 0)
                firefox_profile.set_preference("network.proxy.ssl", "")
                firefox_profile.set_preference("network.proxy.ssl_port", 0)
                firefox_profile.set_preference("network.proxy.share_proxy_settings", False)

                firefox_profile.set_preference("network.proxy.socks", proxy_address)
                firefox_profile.set_preference("network.proxy.socks_port", proxy_port)
                if proxy.find("socks4://") == 0:
                    firefox_profile.set_preference("network.proxy.socks_version", 4)
                elif proxy.find("socks5://") == 0:
                    firefox_profile.set_preference("network.proxy.socks_version", 5)

                pass
            else:
                raise BadProxy
        if disable_img:
            firefox_profile.set_preference("permissions.default.image", 2)
        else:
            firefox_profile.set_preference("permissions.default.image", 1)

        firefox_profile.update_preferences()
        self.firefox_options = Options()

        self.firefox_options.add_argument('-profile')
        self.firefox_options.add_argument(self.path_profile)

        if private:
            self.firefox_options.add_argument('-private')

        # self._terminate_others_process_firefox()

        super().__init__(
            firefox_binary=self.firefox_binary,
            service_args=["--marionette-port", str(self.port_marionette)],
            executable_path=self.path_geckodriver,
            options=self.firefox_options,
            # firefox_profile=firefox_profile
        )

    def _terminate_others_process_firefox(self):
        kill_proc_conditions(basename(self.firefox_binary_full_path), self.path_profile)

    def _get_path_prof(self):
        t_fp = FirefoxProfiles()
        t_fp.filling(self.profile)
        if len(t_fp) > 1:
            raise MoreProfileFirefox
        elif len(t_fp) == 0:
            raise NotFoundProfileFirefox
        else:
            return t_fp[0].full_path

    def kill(self):
        # Внимание функция убивает все дочерние процессы
        kill_only_child_proc(psutil.Process(pid=os.getpid()), basename(self.firefox_binary_full_path), self.path_profile)

    def __del__(self):
        self.quit()
        self.kill()
        pass
