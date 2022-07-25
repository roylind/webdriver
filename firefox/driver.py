from os.path import basename
import subprocess
import time
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
import psutil

from webdriver.firefox.profile_firefox_read_only import FileProfileFirefoxReadOnly as FirefoxProfiles
from webdriver.firefox.exceptions import *
from webdriver.firefox.common import *
from webdriver.firefox.init_driver import InitFirefox
from webdriver.other.process_control import kill_proc_all_child


class GetCallback:
    GET = "get"
    REFRESH = "refresh"


class CreateProfileFirefox:
    def __init__(self, profile: str):
        self.profile = profile
        self.exist_profile()
        self.firefox_binary_full_path = FIREFOX_BINARY_FULL_PATH
        subprocess.call([self.firefox_binary_full_path, "-CreateProfile", self.profile])
        subprocess.Popen([self.firefox_binary_full_path, "-P", self.profile], stdout=subprocess.PIPE)
        time.sleep(int(os.getenv("WAIT_FIREFOX_CREATE_PROFILE", default="5")))
        self.kill_running_process_firefox()

    def exist_profile(self):
        t_fp = FirefoxProfiles()
        t_fp.filling(self.profile)
        if len(t_fp) != 0:
            raise ErrorExistProfile(self.profile)

    def kill_running_process_firefox(self):

        for proc in psutil.process_iter():
            try:
                if proc.name() == basename(self.firefox_binary_full_path) and self.profile in proc.cmdline():
                    kill_proc_all_child(proc)
                elif proc.name() == basename(self.firefox_binary_full_path + "-bin") and self.profile in proc.cmdline():
                    kill_proc_all_child(proc)
            except psutil.NoSuchProcess:
                continue


class Firefox(InitFirefox):

    def __init__(self, profile, disable_img=False, private=False, proxy: str =""):
        super(Firefox, self).__init__(profile, disable_img, private, proxy)

    def get(self, url, **kwargs):
        return super().get(url, **kwargs)

    def refresh(self):
        try:
            super().refresh()
        except Exception as e:
            # Иногда вылазит алерт непонятный
            if str(e).lower().count("alert"):
                self.get(super().current_url)
            else:
                raise ErrorRefresh(str(e))
        self.check_anti_ddos()

    def check_anti_ddos(self):
        detect_text_cloudflare = "One more step"
        if self.all_html().count(detect_text_cloudflare):
            raise DetectCloudflare

    def get_and_wait(self, url, css_selector, count_wait=3, timeout=30, callback="refresh"):
        self.get(url)
        timeout_one = timeout
        for temp_index_waiting in range(0, count_wait, 1):
            try:
                self.check_anti_ddos()
                self.wait_selector(css_selector, timeout=timeout_one)
                return True
            except Exception as e:
                logger.debug("Error get_and_wait: " + str(e))
                if callback == GetCallback.REFRESH:
                    self.refresh()
                    continue
                if callback == GetCallback.GET:
                    self.get(url)
                    continue
                raise InvalidCallback

        raise TimeoutException

    def switch_to_windows(self, url):
        for window_handle in super().window_handles:
            super().switch_to.window(window_handle)
            if url in super().current_url:
                return
        # super().switch_to.window(super().window_handles[0])
        raise NotFoundTab(url)

    def open_window(self):
        if self.current_url == "about:blank":
            return
        super().execute_script("window.open()")
        time.sleep(1)
        self.switch_to_windows("about:blank")

    def all_html(self):
        return self.find_element(By.CSS_SELECTOR, "html").get_attribute("outerHTML")

    def get_html(self, css_selector, timeout=-1):
        if timeout > 0:
            self.wait_selector(css_selector, timeout)
        return self.find_element(By.CSS_SELECTOR, css_selector).get_attribute("outerHTML")

    def check_selector(self, css_selector):
        try:
            self.find_element(By.CSS_SELECTOR, css_selector)
            return True
        except NoSuchElementException:
            return False

    def wait_selector(self, css_selector, timeout=120):
        WebDriverWait(super(), timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def wait_load_image(self, css_selector, timeout=120):
        image = self.find_element(By.CSS_SELECTOR, css_selector)
        for _ in range(timeout):
            time.sleep(1)
            if image.size["height"] != 0 or  image.size["width"] != 0:
                return
        raise TimeOutLoadImage

    def wait_any_selector(self, css_selectors: list, timeout=120):
        WebDriverWait(super(), timeout).until(
            ec. visibility_of_any_elements_located((By.CSS_SELECTOR, ", ".join(css_selectors)))
        )

    def wait_selector_count(self, css_selector, count_wait=3, timeout=30):
        for index_wait_selector_count in range(0, count_wait, 1):
            try:
                self.wait_selector(css_selector, timeout)
                return True
            except TimeoutException as E:
                self.refresh()
                time.sleep(2)
        raise TimeoutException

    def only_one_tab(self):
        for window_handle in self.window_handles[1:]:
            self.switch_to.window(window_handle)
            self.close()
        self.switch_to.window(self.window_handles[0])

    def click(self, css_selector, timeout=-1):
        if timeout > 0:
            WebDriverWait(super(), timeout).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            ).click()
        else:
            self.find_element(By.CSS_SELECTOR, css_selector).click()


if __name__ == "__main__":
    CreateProfileFirefox("test7")
    driver = Firefox("test7")
    driver.get("https://ifconfig.io")
    input()
    pass
