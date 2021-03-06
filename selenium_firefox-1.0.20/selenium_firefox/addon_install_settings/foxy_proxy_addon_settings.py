# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import time

# Pip
from selenium.webdriver.support.ui import Select

# Local
from .builtin_addon_install_settings import BuiltinAddonInstallSettings
# from ..firefox import Firefox

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------- class: FoxyProxyAddonSettings ---------------------------------------------------- #

class FoxyProxyAddonSettings(BuiltinAddonInstallSettings):

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    _name = 'foxy_proxy'


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def post_install_action(
        self,
        firefox,#: Firefox,
        addon_id: str,
        internal_addon_id: str,
        addon_base_url: str
    ) -> None:
        proxy = firefox.proxy

        if not proxy:
            return

        import time
        time.sleep(1)

        firefox.get('{}/proxy.html'.format(addon_base_url), force=True)

        time.sleep(1)

        firefox.find_by('input', id='proxyAddress').send_keys(proxy.host)
        firefox.find_by('input', id='proxyPort').send_keys(str(proxy.port))

        if proxy.needs_auth:
            firefox.find_by('input', id='proxyUsername').send_keys(proxy.username)
            firefox.find_by('input', id='proxyPassword').send_keys(proxy.password)

        firefox.find_by('button', type='submit').click()
        firefox.get('{}/options.html'.format(addon_base_url), force=True)
        time.sleep(1)

        select = Select(firefox.find_by('select', id='mode'))
        select.select_by_index(len(select.options)-1)


# ---------------------------------------------------------------------------------------------------------------------------------------- #