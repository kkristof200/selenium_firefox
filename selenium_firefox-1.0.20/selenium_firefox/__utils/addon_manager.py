# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Tuple, Callable, Dict
import os

# Pip
from noraise import noraise

from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver

# Local
# from ..firefox import Firefox
from ..addon_install_settings import BaseAddonInstallSettings

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: AddonManager --------------------------------------------------------- #

class AddonManager:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def addons_from_folder(
        cls,
        folder_path: str
    ) -> List[BaseAddonInstallSettings]:
        for (dirpath, _, filenames) in os.walk(folder_path):
            return [
                BaseAddonInstallSettings(os.path.join(dirpath, f))
                for f in filenames if f.split('.')[-1] in cls.__SUPPORTED_ADDON_FILE_EXTENSIONS
            ]

    @classmethod
    def install_addons(
        cls,
        firefox,#: Firefox,
        addons_settings: List[BaseAddonInstallSettings],
        temporary: Optional[bool] = False
    ) -> List[Optional[str]]:
        return [
            cls.install_addon(firefox=firefox, addon_settings=addon_settings, temporary=temporary)
            for addon_settings in addons_settings
        ]

    @classmethod
    def install_addon(
        cls,
        firefox,#: Firefox,
        addon_settings: BaseAddonInstallSettings,
        temporary: Optional[bool] = False
    ) -> Optional[str]:
        if addon_settings.path.split('.')[-1] not in cls.__SUPPORTED_ADDON_FILE_EXTENSIONS:
            print('Will not install \'{}\'. Reason: not one of the needed formats: {}'.format(
                addon_settings.path,
                cls.__SUPPORTED_ADDON_FILE_EXTENSIONS
            ))

            return None

        org_handle = firefox.driver.current_window_handle
        addon_id = firefox.driver.install_addon(addon_settings.path, temporary=temporary)

        if not addon_id:
            print('Could not install addon with path \'{}\''.format(addon_settings.path))

        print('Did install addon with id \'{}\' and path \'{}\''.format(addon_id, addon_settings.path))

        internal_addon_id = cls.__get_addon_internal_id(firefox, addon_id)
        org_current_url = firefox.current_url

        def reset(org_handle, org_current_url):
            if len(firefox.window_handles) > 1:
                for handle in firefox.window_handles:
                    firefox.switch_to_window(handle)

                    if internal_addon_id in firefox.current_url:
                        firefox.close()

                        return reset(org_handle, org_current_url)

            if org_handle not in firefox.window_handles:
                org_handle = firefox.window_handles[0]

            firefox.switch_to_window(org_handle)
            firefox.get(org_current_url)

        reset(org_handle, org_current_url)

        addon_settings.post_install_action(
            firefox,
            addon_id,
            internal_addon_id,
            cls.__ADDON_URL.format(internal_addon_id)
        )

        reset(org_handle, org_current_url)

        return addon_id


    # ------------------------------------------------------ Private properties ------------------------------------------------------ #

    __SUPPORTED_ADDON_FILE_EXTENSIONS = ['xpi', 'zip']
    __ADDON_URL                       = 'moz-extension://{}'


    # -------------------------------------------------------- Private methods ------------------------------------------------------- #

    # @noraise()
    @staticmethod
    def __get_addon_internal_id(
        firefox,#: Firefox,
        addon_public_id: str
    ) -> Optional[str]:
        import time
        start_time = time.time()

        while not firefox.prefs.extensions_webextensions_uuids.get(addon_public_id) and time.time() - start_time < 5:
            time.sleep(0.05)

        return firefox.prefs.extensions_webextensions_uuids.get(addon_public_id)


# ---------------------------------------------------------------------------------------------------------------------------------------- #