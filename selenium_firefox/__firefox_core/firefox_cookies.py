# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Dict, Tuple, Union
import os, json, pickle, time

# Pip
from noraise import noraise

import tldextract

from selenium.webdriver.firefox.webdriver import WebDriver

# Local
from .utils import Cookies
from ..models import Cookie

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: FirefoxCookies -------------------------------------------------------- #

class FirefoxCookies:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    driver             : WebDriver
    pickle_cookies     : bool
    cookies_folder_path: str


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def login_via_cookies(
        self,
        url: str,
        accepted_cookie_names: Union[str, List[str]]
    ) -> bool:
        org_url = self.driver.current_url
        self.driver.get(url)
        time.sleep(0.5)

        @noraise(default_return_value=False)
        def __login_via_cookies(accepted_cookie_names: Union[str, List[str]]):
            if isinstance(accepted_cookie_names, str):
                accepted_cookie_names = [accepted_cookie_names]

            if self.has_cookies_for_current_website():
                self.load_cookies()
                time.sleep(1)
                self.driver.refresh()
                time.sleep(1)
            else:
                return False

            for cookie in self.get_cookies():
                if accepted_cookie_names and cookie.name in accepted_cookie_names and not cookie.is_session_cookie and not cookie.is_expired:
                    return True

        login_res = __login_via_cookies(accepted_cookie_names)

        self.driver.get(org_url)

        return login_res

    def save_cookies(
        self,
        url: Optional[str] = None,
        folder_path: Optional[str] = None,
        cookies: Optional[List[Union[Cookie, Dict[str, any]]]] = None
    ) -> None:
        return Cookies.save(
            url=url or self.driver.current_url,
            folder_path=folder_path or self.cookies_folder_path,
            cookies=cookies or self._get_cookies(),
            pickled=self.pickle_cookies
        )

    def load_cookies(
        self,
        folder_path: Optional[str] = None,
    ) -> bool:
        if not self.has_cookies_for_current_website():
            print('Did not find any cookies for url: \'{}\''.format(self.driver.current_url))

            return False

        cookies = Cookies.load(
            url=self.driver.current_url,
            folder_path=folder_path or self.cookies_folder_path
        )

        if not cookies:
            print('Loaded cookies are None or empty for url: \'{}\''.format(self.driver.current_url))

            return False

        @noraise(default_return_value=False)
        def add_cookie(cookie: Cookie) -> bool:
            self.driver.add_cookie(cookie.dict)

            return True

        did_add_cookie = False

        for cookie in cookies:
            # if cookie.is_session_cookie:
            #     print('Cookie named \'{}\' for domain \'{}\' was a session only cookie so won\'t be used'.format(
            #         cookie.name,
            #         cookie.domain
            #     ))

            #     continue

            # if cookie.is_expired:
            #     print('Cookie named \'{}\' for domain \'{}\' did expire'.format(cookie.name, cookie.domain))

            #     continue

            if add_cookie(cookie):
                did_add_cookie = True
            else:
                print('Error while loading cookie named \'{}\' for domain \'{}\'\nURL: \'{}\'\nCookie JSON: {}'.format(
                    cookie.name,
                    cookie.domain,
                    self.driver.current_url,
                    json.dumps(cookie, indent=4)
                ))

        return did_add_cookie

    def delete_cookies(
        self,
        folder_path: Optional[str] = None,
    ) -> bool:
        return Cookies.delete(
            url=self.driver.current_url,
            folder_path=self.cookies_folder_path
        )

    def get_cookies(self) -> List[Cookie]:
        return [Cookie(d) for d in self._get_cookies()]

    def get_usable_cookies(self) -> List[Cookie]:
        return [c for c in [Cookie(d) for d in self._get_cookies()] if not c.is_expired]

    def has_all_cookies(self, cookie_names: Union[str, List[str]]) -> bool:
        existing_cookie_names = [c.name for c in self.get_usable_cookies()]

        if isinstance(cookie_names, str):
            cookie_names = [cookie_names]

        for cookie_name in cookie_names:
            if cookie_name not in existing_cookie_names:
                return False

        return True

    def has_any_cookie(self, cookie_names: Union[str, List[str]]) -> bool:
        existing_cookie_names = [c.name for c in self.get_usable_cookies()]

        if isinstance(cookie_names, str):
            cookie_names = [cookie_names]

        for cookie_name in cookie_names:
            if cookie_name in existing_cookie_names:
                return True

        return False

    def has_cookie(self, cookie_name: str) -> bool:
        return cookie_name in [c.name for c in self.get_usable_cookies()]

    def has_saved_cookies_for_current_website(self) -> bool:
        return self.has_cookies_for_url(url=self.driver.current_url)

    # alias - kept for convenience
    has_cookies_for_current_website = has_saved_cookies_for_current_website

    def has_saved_cookies_for_url(
        self,
        url: str
    ) -> bool:
        return Cookies.has_saved_cookies(
            url=url,
            folder_path=self.cookies_folder_path
        )

    # alias - kept for convenience
    has_cookies_for_url = has_saved_cookies_for_url


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @noraise(default_return_value=[])
    def _get_cookies(self) -> List[dict]:
        return self.driver.get_cookies()


# ---------------------------------------------------------------------------------------------------------------------------------------- #