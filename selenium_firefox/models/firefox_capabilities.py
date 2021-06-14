# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Dict

# Pip
from selenium_browser import Capabilities

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: Capabilities ----------------------------------------------------- #

class FirefoxCapabilities(Capabilities):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        d: Dict[str, any]
    ):
        super().__init__(d)

        self.moz_accessibility_checks                  = d.get('moz:accessibilityChecks')
        self.moz_build_id                              = d.get('moz:buildID')
        self.moz_geckodriver_version                   = d.get('moz:geckodriverVersion')
        self.moz_headless                              = d.get('moz:headless')
        self.moz_process_id                            = d.get('moz:processID')
        self.moz_profile                               = d.get('moz:profile')
        self.moz_shutdown_timeout                      = d.get('moz:shutdownTimeout')
        self.moz_use_non_spec_compliant_pointer_origin = d.get('moz:useNonSpecCompliantPointerOrigin')
        self.moz_webdriver_click                       = d.get('moz:webdriverClick')


# -------------------------------------------------------------------------------------------------------------------------------- #