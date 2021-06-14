# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional
import os, json

# Pip
from selenium_browser import BrowserProperties
from noraise import noraise

from selenium.webdriver.firefox.webdriver import WebDriver

# Local
from .models import FirefoxCapabilities, Prefs
from .__constants import Constants
from .__utils import Utils

# -------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------- class: FirefoxProperties --------------------------------------------------- #

class FirefoxProperties(BrowserProperties):

    # --------------------------------------------------- Public properties -------------------------------------------------- #

    driver: WebDriver

    @property
    def capabilities(self) -> FirefoxCapabilities:
        return FirefoxCapabilities(self.driver.capabilities)

    @property
    def prefs(self) -> Optional[Prefs]:
        @noraise()
        def _prefs() -> Optional[Prefs]:
            return Prefs(Utils.parse_prefs_js(open(os.path.join(self.capabilities.moz_profile, Constants.PREFS_JS_NAME), 'r').read()))

        return _prefs()

    @property
    def temp_profile_folder_path(self) -> Optional[str]:
        @noraise(print_exc=False)
        def _temp_profile_folder_path() -> Optional[str]:
            return self.capabilities.moz_profile

        return _temp_profile_folder_path()


# -------------------------------------------------------------------------------------------------------------------------------- #