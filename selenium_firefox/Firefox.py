# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional, Union, List, Tuple
import os, shutil, time

# Pip
from noraise import noraise
from selenium_browser import Browser, AddonInstallSettings, Utils as BrowserUtils
from kproxy import Proxy

from selenium.webdriver import Firefox as FirefoxWebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import geckodriver_autoinstaller

# Local
from .firefox_addons import AddonManager, FoxyProxyAddonSettings

from .__firefox_properties import FirefoxProperties
from .__constants import Constants
from .__utils import Utils

# -------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: Firefox -------------------------------------------------------- #

class Firefox(
    Browser,
    FirefoxProperties
):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,

        # profile
        profile_path: Optional[str] = None,
        profile_id: Optional[str] = None,

        # cookies
        pickle_cookies: bool = False,

        # proxy
        proxy: Optional[Union[Proxy, str]] = None,

        # addons
        addons_folder_path: Optional[str] = None,
        addon_settings: Optional[List[AddonInstallSettings]] = None,
        # addons - legacy (kept for convenience)
        extensions_folder_path: Optional[str] = None,

        # other paths
        geckodriver_path: Optional[str] = None,
        firefox_binary_path: Optional[str] = None,

        # profile settings
        private: bool = False,
        full_screen: bool = True,
        language: str = 'en-us',
        user_agent: Optional[str] = None,
        disable_images: bool = False,
        mute_audio: bool = False,

        # firefox option settings
        screen_size: Optional[Tuple[int, int]] = None, # (width, height)
        headless: bool = False,
        home_page_url: Optional[str] = None,

        # selenium-wire support
        webdriver_class: Optional = None,

        # find function
        default_find_func_timeout: int = 2.5
    ):
        '''EITHER PROVIDE 'profile_id' OR  'profile_path'.
           webdriver_class: override class used to create webdriver (for example: seleniumwire.webdriver.Firefox), Defaults to: 'selenium.webdriver.Firefox'
        '''

        proxy = BrowserUtils.proxy(proxy)
        profile_path, cookies_folder_path, user_agent_file_path = BrowserUtils.get_cache_paths(profile_path, profile_id)
        os.makedirs(cookies_folder_path, exist_ok=True)

        self.source_profile_path = profile_path

        addon_settings = addon_settings or []

        if proxy and proxy.needs_auth:
            addon_settings.append(FoxyProxyAddonSettings())

        super().__init__(
            webdriver_class or FirefoxWebDriver,
            cookies_folder_path=cookies_folder_path,
            pickle_cookies=pickle_cookies,
            proxy=proxy,
            default_find_func_timeout=default_find_func_timeout,
            webdriver_executable_path=Utils.get_geckodriver_path(geckodriver_path),
            firefox_profile=Utils.profile(
                user_agent=BrowserUtils.user_agent(
                    user_agent=user_agent,
                    file_path=user_agent_file_path
                ),
                language=language,
                private=private,
                disable_images=disable_images,
                mute_audio=mute_audio,
                proxy=proxy if proxy and not proxy.needs_auth else None,
                path=profile_path
            ),
            firefox_options=Utils.options(
                screen_size=screen_size,
                headless=headless,
                home_page_url=home_page_url
            ),
            firefox_binary=Utils.get_firefox_binary(firefox_binary_path)
        )

        if full_screen:
            self.driver.fullscreen_window()

        am = AddonManager(self)

        am.install_addons(
            addons_settings=am.get_all_addon_settings(
                addons_folder_path=addons_folder_path,
                user_addon_settings=addon_settings
            ),
            temporary=False
        )


    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

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


# -------------------------------------------------------------------------------------------------------------------------------- #