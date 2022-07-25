import os

from webdriver.other.common import *
from webdriver.firefox.exceptions import NotFoundBinaryFileFirefox


if WINDOWS:
    PATH_GECKODRIVER = "geckodriver.exe"
    t_pf_path = os.getenv('PROGRAMFILES')
    t_pfx86_path = os.getenv('PROGRAMFILES(x86)')
    t_path_binary = "\\Mozilla Firefox\\firefox.exe"

    if os.getenv("FIREFOX_BINARY", default=None) is not None:
        FIREFOX_BINARY_FULL_PATH = os.getenv("FIREFOX_BINARY")
    elif os.path.isfile(t_pf_path + t_path_binary):
        FIREFOX_BINARY_FULL_PATH = (t_pf_path + t_path_binary)
    elif os.path.isfile(t_pfx86_path + t_path_binary):
        FIREFOX_BINARY_FULL_PATH = (t_pfx86_path + t_path_binary)
    else:
        raise NotFoundBinaryFileFirefox
elif LINUX:
    PATH_GECKODRIVER = "/usr/bin/geckodriver"

    if os.getenv("FIREFOX_BINARY", default=None) is not None:
        FIREFOX_BINARY_FULL_PATH = os.getenv("FIREFOX_BINARY")
    elif os.path.isfile("/usr/bin/firefox-esr"):
        FIREFOX_BINARY_FULL_PATH = "/usr/bin/firefox-esr"
    elif os.path.isfile("/usr/bin/firefox"):
        FIREFOX_BINARY_FULL_PATH = "/usr/bin/firefox"
    else:
        raise NotFoundBinaryFileFirefox
