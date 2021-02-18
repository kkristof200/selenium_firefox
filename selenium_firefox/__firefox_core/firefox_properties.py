# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import os, json

# Pip
from noraise import noraise

from selenium.webdriver.firefox.webdriver import WebDriver

# Local
from ..models import Capabilities, Proxy, Prefs
from ..__resources import Constants
from ..__utils import Utils

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: FirefoxProperties ------------------------------------------------------- #

class FirefoxProperties:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    driver: WebDriver


    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def proxy(self) -> Optional[Proxy]:
        return self._proxy

    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(self.driver.capabilities)

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


    # ------------------------------------------------------ Private properties ------------------------------------------------------ #

    _user_agent: Optional[str]
    _proxy     : Optional[Proxy]


# ---------------------------------------------------------------------------------------------------------------------------------------- #