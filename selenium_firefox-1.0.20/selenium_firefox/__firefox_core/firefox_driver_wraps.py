# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from noraise import noraise

from selenium.webdriver.firefox.webdriver import WebDriver

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: FirefoxDriverWraps ------------------------------------------------------ #

class FirefoxDriverWraps:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    driver: WebDriver


    @property
    def window_handles(self) -> list:
        return self.driver.window_handles

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def current_window_handle(self):
        return self.driver.current_window_handle


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @noraise()
    def switch_to_window(
        self,
        window_handle
    ) -> Optional[dict]:
        return self.driver.switch_to.window(window_handle)

    def close(self) -> None:
        self.driver.close()

    def get(
        self,
        url: str,
        force: bool = False
    ) -> bool:
        if not force:
            to_remove = ['www.']

            clean_current = self.driver.current_url.split('://')[-1]
            clean_new = url.split('://')[-1]

            for _to_remove in to_remove:
                clean_current = clean_current.replace(_to_remove, '')
                clean_new = clean_new.replace(_to_remove, '')

            if clean_current.strip('/') == clean_new.strip('/'):
                return False

        self.driver.get(url)

        return True

    def refresh(self) -> None:
        self.driver.refresh()

    @noraise(default_return_value=False)
    def quit(self) -> bool:
        self.driver.quit()

        return True


# ---------------------------------------------------------------------------------------------------------------------------------------- #