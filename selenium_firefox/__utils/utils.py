# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from  typing import Optional, Dict, Tuple, Union, List
import json, os, tempfile, platform, subprocess

# Pip
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import geckodriver_autoinstaller

# Local
from ..models import Proxy
from ..__resources.constants import Constants
from ..addon_install_settings import BuiltinAddonInstallSettings, BaseAddonInstallSettings
from .addon_manager import AddonManager

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Utils ------------------------------------------------------------- #

class Utils:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def webdriver_init_path_kwarg(
        cls,
        user_passed_geckodriver_path: Optional[str] = None
    ) -> Dict[str, str]:
        firefox_kwargs = {}

        if user_passed_geckodriver_path and os.path.exists(user_passed_geckodriver_path):
            firefox_kwargs[Constants.WEBDRIVER_INIT_EXECUTABLE_PATH_KEYWORD] = user_passed_geckodriver_path
        elif not cls.is_geckodriver_installed():
            firefox_kwargs[Constants.WEBDRIVER_INIT_EXECUTABLE_PATH_KEYWORD] = geckodriver_autoinstaller.install()

        return firefox_kwargs

    @staticmethod
    def is_geckodriver_installed() -> bool:
        return subprocess.getstatusoutput('geckodriver -V')[0] == 0

    @staticmethod
    def cookies_folder_path(
        cookies_folder_path: Optional[str] = None,
        cookies_id: Optional[str] = None,
    ) -> str:
        return cookies_folder_path or os.path.join(
            '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir(),
            Constants.GENERAL_COOKIES_FOLDER_NAME,
            cookies_id or Constants.DEFAULT_COOKIES_ID
        )

    @staticmethod
    def user_agent(
        user_agent: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> Optional[str]:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read().strip()
        elif user_agent:
            user_agent = user_agent.strip()

            if file_path:
                with open(file_path, 'w') as f:
                    f.write(user_agent)

            return user_agent

    @staticmethod
    def proxy(
        proxy: Optional[Union[Proxy, str]] = None,

        # proxy - legacy (kept for convenience)
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> Optional[Proxy]:
        if not proxy:
            if not host and not port:
                return None

            proxy = Proxy(host=host, port=port)

        return proxy if isinstance(proxy, Proxy) else Proxy.from_str(proxy)

    @staticmethod
    def profile(
        user_agent: Optional[str] = None,
        language: str = 'en-us',
        private: bool = False,
        disable_images: bool = False,
        proxy: Optional[Proxy] = None,
        path: Optional[str] = None
    ) -> FirefoxProfile:
        profile = FirefoxProfile(path if path and os.path.exists(path) else None)

        if user_agent:
            profile.set_preference('general.useragent.override', user_agent)

        if language:
            profile.set_preference('intl.accept_languages', language)

        if private:
            profile.set_preference('browser.privatebrowsing.autostart', True)

        if disable_images:
            profile.set_preference('permissions.default.image', 2)
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

        if proxy:
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http', proxy.host)
            profile.set_preference('network.proxy.http_port', proxy.port)
            profile.set_preference('network.proxy.ssl', proxy.host)
            profile.set_preference('network.proxy.ssl_port', proxy.port)
            profile.set_preference('network.proxy.ftp', proxy.host)
            profile.set_preference('network.proxy.ftp_port', proxy.port)
            profile.set_preference('network.proxy.socks', proxy.host)
            profile.set_preference('network.proxy.socks_port', proxy.port)
            profile.set_preference('network.proxy.socks_version', 5)
            profile.set_preference('signon.autologin.proxy', True)

        profile.set_preference('marionatte', False)
        profile.set_preference('dom.webdriver.enabled', False)
        profile.set_preference('media.peerconnection.enabled', False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('general.warnOnAboutConfig', False)
        profile.update_preferences()

        return profile

    @staticmethod
    def options(
        screen_size: Optional[Tuple[int, int]] = None, # (width, height)
        headless: bool = False,
        mute_audio: bool = False,
        home_page_url: Optional[str] = None
    ) -> FirefoxOptions:
        options = FirefoxOptions()
        options.add_argument('--homepage \"{}\"'.format(home_page_url or 'data:,'))

        if screen_size is not None:
            options.add_argument('--width={}'.format(screen_size[0]))
            options.add_argument('--height={}'.format(screen_size[1]))

        if headless:
            options.add_argument('--headless')

        if mute_audio:
            options.add_argument('--mute-audio')

        return options

    @staticmethod
    def addon_settings(
        addons_folder_path: Optional[str] = None,
        user_addon_settings: Optional[List[BaseAddonInstallSettings]] = None,
        lib_addon_settings: Optional[List[BuiltinAddonInstallSettings]] = None
    ) -> List[BaseAddonInstallSettings]:
        addon_settings = lib_addon_settings or []

        if user_addon_settings:
            addon_settings.extend(user_addon_settings)

        if addons_folder_path and os.path.exists(addons_folder_path):
            addon_settings.extend(AddonManager.addons_from_folder(addons_folder_path))

        return addon_settings

    @staticmethod
    def parse_prefs_js(prefs_str: str) -> Dict[str, any]:
        prefs = {}

        for line in prefs_str.split('\n'):
            try:
                key = line.split('user_pref("')[1].split('"')[0]
                value = line.split('", ')[1].split(');')[0]

                try:
                    value = json.loads(value.replace('\\"', '"').strip('"'))
                except:
                    value = json.loads(value)

                prefs[key] = value
            except:
                pass

        return prefs


# ---------------------------------------------------------------------------------------------------------------------------------------- #