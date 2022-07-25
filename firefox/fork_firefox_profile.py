import os
import copy
import json
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

WEBDRIVER_EXT = "webdriver.xpi"
WEBDRIVER_PREFERENCES = "webdriver_prefs.json"
EXTENSION_NAME = "fxdriver@googlecode.com"


class NotMoveFirefoxProfile(FirefoxProfile):
    ANONYMOUS_PROFILE_NAME = "WEBDRIVER_ANONYMOUS_PROFILE"
    DEFAULT_PREFERENCES = None

    def __init__(self, profile_directory=None):

        if not FirefoxProfile.DEFAULT_PREFERENCES:
            with open(os.path.join(os.path.dirname(__file__),
                                   WEBDRIVER_PREFERENCES)) as default_prefs:
                FirefoxProfile.DEFAULT_PREFERENCES = json.load(default_prefs)

        self.default_preferences = copy.deepcopy(
            FirefoxProfile.DEFAULT_PREFERENCES['mutable'])
        self.native_events_enabled = True
        self.profile_dir = profile_directory
        if self.profile_dir is None:
            self.profile_dir = self._create_tempfolder()
        else:
            self._read_existing_userjs(os.path.join(self.profile_dir, "user.js"))
        self.extensionsDir = os.path.join(self.profile_dir, "extensions")
        self.userPrefs = os.path.join(self.profile_dir, "user.js")
        if os.path.isfile(self.userPrefs):
            os.chmod(self.userPrefs, 0o644)
