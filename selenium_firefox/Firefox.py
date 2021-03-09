# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, List, Tuple
import os, shutil, time

# Pip
from noraise import noraise

from selenium.webdriver import Firefox as FirefoxWebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Local
from .__firefox_core import FirefoxCookies, FirefoxDriverWraps, FirefoxFindFuncs, FirefoxProperties, FirefoxWebelementFunctions
from .models import Proxy, Capabilities, Prefs

from .addon_install_settings import BaseAddonInstallSettings, FoxyProxyAddonSettings
from .__resources import Constants
from .__utils import AddonManager, Utils

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Firefox ------------------------------------------------------------ #

class Firefox(
    FirefoxCookies,
    FirefoxDriverWraps,
    FirefoxFindFuncs,
    FirefoxProperties,
    FirefoxWebelementFunctions
):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,

        # cookies
        cookies_folder_path: Optional[str] = None,
        cookies_id: Optional[str] = None,
        pickle_cookies: bool = False,

        # proxy
        proxy: Optional[Union[Proxy, str]] = None,
        # proxy - legacy (kept for convenience)
        host: Optional[str] = None,
        port: Optional[int] = None,

        # addons
        addons_folder_path: Optional[str] = None,
        addon_settings: Optional[List[BaseAddonInstallSettings]] = None,
        # addons - legacy (kept for convenience)
        extensions_folder_path: Optional[str] = None,

        # other paths
        geckodriver_path: Optional[str] = None,
        firefox_binary_path: Optional[str] = None,
        profile_path: Optional[str] = None,

        # profile settings
        private: bool = False,
        full_screen: bool = True,
        language: str = 'en-us',
        user_agent: Optional[str] = None,
        disable_images: bool = False,

        # firefox option settings
        screen_size: Optional[Tuple[int, int]] = None, # (width, height)
        headless: bool = False,
        mute_audio: bool = False,
        home_page_url: Optional[str] = None,

        # selenium-wire support
        webdriver_class: Optional = None,

        # find function
        default_find_func_timeout: int = 2.5
    ):
        '''EITHER PROVIDE 'cookies_id' OR  'cookies_folder_path'.
           IF 'cookies_folder_path' is None, 'cokies_id', will be used to calculate 'cookies_folder_path'
           IF 'cokies_id' is None, the name of the 'profile_path' follder wil lbe used. if that is Nonne too, 'test' will be used

           webdriver_class: override class used to create webdriver (for example: seleniumwire.webdriver.Firefox), Defaults to: 'selenium.webdriver.Firefox'
        '''

        self.default_find_func_timeout = default_find_func_timeout
        self.pickle_cookies = pickle_cookies
        self.source_profile_path = profile_path

        self.cookies_folder_path = Utils.cookies_folder_path(
            cookies_folder_path=cookies_folder_path,
            cookies_id=cookies_id,
            profile_path=profile_path
        )
        os.makedirs(self.cookies_folder_path, exist_ok=True)

        self._user_agent = Utils.user_agent(
            user_agent=user_agent,
            file_path=os.path.join(self.cookies_folder_path, Constants.USER_AGENT_FILE_NAME)
        )

        self._proxy = Utils.proxy(
            proxy=proxy,
            host=host,
            port=port
        )

        self.driver = (webdriver_class or FirefoxWebDriver)(
            firefox_profile=Utils.profile(
                user_agent=self._user_agent,
                language=language,
                private=private,
                disable_images=disable_images,
                proxy=self._proxy if self._proxy and not self._proxy.needs_auth else None,
                path=profile_path
            ),
            firefox_options=Utils.options(
                screen_size=screen_size,
                headless=headless,
                mute_audio=mute_audio,
                home_page_url=home_page_url
            ),
            firefox_binary=FirefoxBinary(
                firefox_path=firefox_binary_path
            ) if firefox_binary_path and os.path.exists(firefox_binary_path) else None,
            **Utils.webdriver_init_path_kwarg(geckodriver_path)
        )

        if full_screen:
            self.driver.fullscreen_window()

        lib_addon_settings = []

        if self._proxy and self._proxy.needs_auth:
            lib_addon_settings.append(FoxyProxyAddonSettings())

        AddonManager.install_addons(
            firefox=self,
            addons_settings=Utils.addon_settings(
                addons_folder_path=addons_folder_path or extensions_folder_path,
                user_addon_settings=addon_settings,
                lib_addon_settings=lib_addon_settings
            ),
            temporary=False
        )


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @noraise(default_return_value=False)
    def backup_profile(
        self,
        target_profile_path: Optional[str] = None,
        delete_cache: bool = True,
        delete_storage: bool = True,
        max_copy_tries: int = 5
    ) -> bool:
        target_profile_path = target_profile_path or self.source_profile_path

        if os.path.exists(target_profile_path):
            shutil.rmtree(target_profile_path)

        current_copy_try = 0

        while not os.path.exists(target_profile_path) and current_copy_try < max_copy_tries:
            try:
                shutil.copytree(self.temp_profile_folder_path, target_profile_path)
            except:
                pass

            time.sleep(0.1)

        to_remove = [v for v in [
            'cache2' if delete_cache else None,
            'storage' if delete_storage else None,
            'storage.sqlite' if delete_storage else None
        ] if v]

        for v in to_remove:
            p = os.path.join(target_profile_path, v)

            if os.path.exists(p):
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

        return os.path.exists(target_profile_path)


    # --------------------------------------------------------- Destructor ----------------------------------------------------------- #

    @noraise()
    def __del__(self):
        if os.path.exists(self.driver.profile.path):
            self.quit()


# ---------------------------------------------------------------------------------------------------------------------------------------- #