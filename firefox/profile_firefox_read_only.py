import configparser
from os import getenv
from os.path import dirname
from webdriver.other.common import WINDOWS, LINUX


class ProfileFirefoxConfig:

    def __init__(self, index: int, name: str, path: str, path_ini_file: str = None):
        if name == "" or path == "":
            raise Exception("Name or Path empty")

        self.index = index
        self.name = name
        self.path = path
        if path_ini_file is not None:
            self.full_path = dirname(path_ini_file) + "/" + self.path

    def __str__(self):
        return "Index: {0}\nName: {1}\nPath: {2}\n".format(self.index, self.name, self.path)

    def __eq__(self, other):
        if (self.index == other.index
            and self.name == other.name
                and self.path == other.path):
            return True
        else:
            return False


if WINDOWS:
    FIREFOX_WORK_DIR = getenv('APPDATA') + "/Mozilla/Firefox/"
    FIREFOX_PROFILE_INI = FIREFOX_WORK_DIR + "profiles.ini"

if LINUX:
    FIREFOX_WORK_DIR = getenv('HOME') + "/.mozilla/firefox/"
    FIREFOX_PROFILE_INI = FIREFOX_WORK_DIR + "profiles.ini"


class FileProfileFirefoxReadOnly:

    def __init__(self):
        self.work_folder = FIREFOX_WORK_DIR
        self.path_ini_file = FIREFOX_PROFILE_INI
        self.profiles_ini = configparser.ConfigParser()
        self.profiles_ini.read(self.path_ini_file)
        self._list_prof = []
        self._visible_list_prof = self._list_prof
        self._read_list_prof()
        self.text_filling = ""

    def _read_list_prof(self):
        index_prof = 0
        self._list_prof = []
        while ("Profile" + str(index_prof)) in self.profiles_ini.sections():
            self._list_prof.append(ProfileFirefoxConfig(
                index_prof,
                self.profiles_ini.get("Profile" + str(index_prof), 'Name'),
                self.profiles_ini.get("Profile" + str(index_prof), 'Path'),
                self.path_ini_file
            ))
            index_prof += 1

    def filling(self, text: str):
        self.text_filling = text

    def _filling(self):
        self._visible_list_prof = []
        for prof in self._list_prof:
            if len(self.text_filling):
                if self.text_filling.lower() in prof.name.lower():
                    self._visible_list_prof.append(prof)
            else:
                self._visible_list_prof.append(prof)

    def __str__(self):
        self._filling()
        # print(self._list_prof[0])
        # return str([str(x)for x in self._list_prof])
        return "\n".join([str(x)for x in self._visible_list_prof])

    def __getitem__(self, item):
        self._filling()
        return self._visible_list_prof[item]

    def __setitem__(self, key, value):
        for num, prof in enumerate(list(self._list_prof)):
            if prof == self._visible_list_prof[key]:
                self._list_prof[num] = value
                self._visible_list_prof[key] = self._list_prof[num]

        # self._filling()

    def __delitem__(self, key):
        for num, prof in enumerate(list(self._list_prof)):
            if prof == self._visible_list_prof[key]:
                self._list_prof.pop(num)
        self._filling()

    def pop(self, index):
        del self[index]

    def __len__(self):
        self._filling()
        return len(self._visible_list_prof)


if __name__ == "__main__":
    print(WINDOWS)
    fp = FileProfileFirefoxReadOnly()
    print(str(fp))
    fp.filling("test")
    print(123)
    print(str(fp[1]))

