class NotFoundPrefsJSInProfile(Exception):
    def __init__(self, profile: str):
        self.profile = profile

    def __str__(self):
        return "Prefs.js file not found profile: {profile}".format(profile=self.profile)


class BadProxy(Exception):
    pass

class TimeOutLoadImage(Exception):
    pass

class MoreProfileFirefox(Exception):
    def __str__(self):
        return "More than one suitable profile firefox"


class NotFoundProfileFirefox(Exception):
    def __str__(self):
        return "Profile Firefox Not Found"


class DetectCloudflare(Exception):
    def __str__(self):
        return "Detect Cloudflare"


class InvalidCallback(Exception):
    def __str__(self):
        return "Invalid Callback"


class NotFoundTab(Exception):
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return "Not Found Tab is uri: {uri}".format(uri=self.url)


class ErrorRefresh(Exception):
    def __init__(self, error_msg: str):
        self.error_msg = error_msg

    def __str__(self):
        return "Refresh Page Error: {error_msg}".format(error_msg=self.error_msg)


class ErrorExistProfile(Exception):
    def __init__(self, profile: str):
        self.profile = profile

    def __str__(self):
        return "Exist profile: {profile}".format(profile=self.profile)


class NotFoundBinaryFileFirefox(Exception):
    def __str__(self):
        return "Not Found Binary File Firefox"


class NotFoundAddon(Exception):
    def __str__(self):
        return "Not Found Addon"
