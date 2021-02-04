# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Capabilities --------------------------------------------------------- #

class Capabilities:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: Dict[str, any]
    ):
        self.accept_insecure_certs                     = d.get('acceptInsecureCerts')
        self.browser_name                              = d.get('browserName')
        self.browser_version                           = d.get('browserVersion')
        self.moz_accessibility_checks                  = d.get('moz:accessibilityChecks')
        self.moz_build_id                              = d.get('moz:buildID')
        self.moz_geckodriver_version                   = d.get('moz:geckodriverVersion')
        self.moz_headless                              = d.get('moz:headless')
        self.moz_process_id                            = d.get('moz:processID')
        self.moz_profile                               = d.get('moz:profile')
        self.moz_shutdown_timeout                      = d.get('moz:shutdownTimeout')
        self.moz_use_non_spec_compliant_pointer_origin = d.get('moz:useNonSpecCompliantPointerOrigin')
        self.moz_webdriver_click                       = d.get('moz:webdriverClick')
        self.page_load_strategy                        = d.get('pageLoadStrategy')
        self.platform_name                             = d.get('platformName')
        self.platform_version                          = d.get('platformVersion')
        self.rotatable                                 = d.get('rotatable')
        self.set_window_rect                           = d.get('setWindowRect')
        self.strict_file_interactability               = d.get('strictFileInteractability')
        self.timeouts                                  = d.get('timeouts')
        self.unhandled_prompt_behavior                 = d.get('unhandledPromptBehavior')


# ---------------------------------------------------------------------------------------------------------------------------------------- #