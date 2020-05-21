from typing import Optional, Dict

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as by
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from fake_useragent import UserAgent
import tldextract

By = by
Keys = Keys

import pickle, os, time

RANDOM_USERAGENT = 'random'

class Firefox:
    def __init__(
        self,
        cookies_folder_path: str,
        extensions_folder_path: str,
        host: str = None,
        port: int = None,
        private: bool = False,
        full_screen: bool = True,
        headless: bool = False,
        language: str = 'en-us',
        manual_set_timezone: bool = False,
        user_agent: str = None,
        load_proxy_checker_website: bool = False
    ):
        self.cookies_folder_path = cookies_folder_path
        profile = webdriver.FirefoxProfile()

        if user_agent is not None:
            if user_agent == RANDOM_USERAGENT:
                user_agent_path = os.path.join(cookies_folder_path, 'user_agent.txt')

                if os.path.exists(user_agent_path):
                    with open(user_agent_path, 'r') as file:
                        user_agent = file.read().strip()
                else:
                    user_agent = self.__random_firefox_user_agent(min_version=60.0)
                    
                    with open(user_agent_path, 'w') as file:
                        file.write(user_agent)

            profile.set_preference("general.useragent.override", user_agent)
        
        if language is not None:
            profile.set_preference('intl.accept_languages', language)

        if private:
            profile.set_preference("browser.privatebrowsing.autostart", True)
        
        if host is not None and port is not None:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", host)
            profile.set_preference("network.proxy.http_port", port)
            profile.set_preference("network.proxy.ssl", host)
            profile.set_preference("network.proxy.ssl_port", port)
            profile.set_preference("network.proxy.ftp", host)
            profile.set_preference("network.proxy.ftp_port", port)
            profile.set_preference("network.proxy.socks", host)
            profile.set_preference("network.proxy.socks_port", port)
            profile.set_preference("network.proxy.socks_version", 5)
            profile.set_preference("signon.autologin.proxy", True)
        
        profile.set_preference("marionatte", False)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("media.peerconnection.enabled", False)
        profile.set_preference('useAutomationExtension', False)

        profile.set_preference("general.warnOnAboutConfig", False)

        profile.update_preferences()

        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options)

        if full_screen:
            self.driver.fullscreen_window()
        
        try:
            change_timezone_id = None
            for (dirpath, _, filenames) in os.walk(extensions_folder_path):
                for filename in filenames:
                    if filename.endswith('.xpi') or filename.endswith('.zip'):
                        addon_id = self.driver.install_addon(os.path.join(dirpath, filename), temporary=False)

                        if 'change_timezone' in filename:
                            change_timezone_id = addon_id

            # self.driver.get("about:addons")
            # self.driver.find_element_by_id("category-extension").click()
            # self.driver.execute_script("""
            #     let hb = document.getElementById("html-view-browser");
            #     let al = hb.contentWindow.window.document.getElementsByTagName("addon-list")[0];
            #     let cards = al.getElementsByTagName("addon-card");
            #     for(let card of cards){
            #         card.addon.disable();
            #         card.addon.enable();
            #     }
            # """)

            while len(self.driver.window_handles) > 1:
                time.sleep(0.5)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()
            
            self.driver.switch_to.window(self.driver.window_handles[0])

            if change_timezone_id is not None and manual_set_timezone:
                if host is not None and port is not None:
                    self.open_new_tab('https://whatismyipaddress.com/')
                    time.sleep(0.25)

                self.open_new_tab('https://www.google.com/search?client=firefox-b-d&q=my+timezone')
                time.sleep(0.25)

                self.driver.switch_to.window(self.driver.window_handles[0])
                
                input('\n\n\nSet timezone.\n\nPress ENTER, when finished. ')
            
                while len(self.driver.window_handles) > 1:
                    time.sleep(0.5)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.close()
                
                self.driver.switch_to.window(self.driver.window_handles[0])
            elif load_proxy_checker_website and host is not None and port is not None:
                self.driver.get('https://whatismyipaddress.com/')
        except:
            while len(self.driver.window_handles) > 1:
                time.sleep(0.5)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()

    def get(
        self,
        url: str
    ) -> bool:
        clean_current = self.driver.current_url.replace('https://', '').replace('www.', '').strip('/')
        clean_new = url.replace('https://', '').replace('www.', '').strip('/')

        if clean_current == clean_new:
            return False
        
        self.driver.get(url)

        return True

    def refresh(self) -> None:
        self.driver.refresh()

    def find(
        self,
        by: By,
        key: str,
        element: Optional = None,
        timeout: int = 15
    ) -> Optional:
        if element is None:
            element = self.driver
        
        try:
            e = WebDriverWait(element, timeout).until(
                EC.presence_of_element_located((by, key))
            )

            return e
        except:        
            return None

    def find_all(
        self,
        by: By,
        key: str,
        element: Optional = None,
        timeout: int = 15
    ) -> Optional:
        if element is None:
            element = self.driver

        try:
            es = WebDriverWait(element, timeout).until(
                EC.presence_of_all_elements_located((by, key))
            )

            return es
        except:
            return None
    
    def get_attribute(self, element, key: str) -> Optional[str]:
        try:
            return element.get_attribute(key)
        except:
            return None

    def get_attributes(self, element) -> Optional[Dict[str, str]]:
        try:
            return json.loads(
                self.browser.driver.execute_script(
                    'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return JSON.stringify(items);',
                    element
                )
            )
        except:
            return None

    def save_cookies(self) -> None:
        pickle.dump(
            self.driver.get_cookies(),
            open(self.__cookies_path(), "wb")
        )

    def load_cookies(self) -> None:
        if not self.has_cookies_for_current_website():
            self.save_cookies()

            return

        cookies = pickle.load(open(self.__cookies_path(), "rb"))

        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def has_cookies_for_current_website(self, create_folder_if_not_exists: bool = True) -> bool:
        return os.path.exists(
            self.__cookies_path(
                create_folder_if_not_exists=create_folder_if_not_exists
            )
        )

    def send_keys_delay_random(
        self,
        element: object,
        keys: str,
        min_delay: float = 0.025,
        max_delay: float = 0.25
    ) -> None:
        import random

        for key in keys:
            element.send_keys(key)
            time.sleep(random.uniform(min_delay,max_delay))

    def scroll(self, amount: int) -> None:
        self.driver.execute_script("window.scrollTo(0,"+str(self.current_page_offset_y()+amount)+");")

    def current_page_offset_y(self) -> float:
        return self.driver.execute_script("return window.pageYOffset;")

    def open_new_tab(self, url: str) -> None:
        if url is None:
            url = ""

        cmd = 'window.open("'+url+'","_blank");'
        self.driver.execute_script(cmd)
        self.driver.switch_to.window(self.driver.window_handles[-1])



    # LEGACY
    def scroll_to_bottom(self) -> None:
        MAX_TRIES = 25
        SCROLL_PAUSE_TIME = 0.5
        SCROLL_STEP_PIXELS = 5000
        current_tries = 1

        while True:
            last_height = self.current_page_offset_y()
            self.scroll(last_height+SCROLL_STEP_PIXELS)
            time.sleep(SCROLL_PAUSE_TIME)
            current_height = self.current_page_offset_y()

            if last_height == current_height:
                current_tries += 1

                if current_tries == MAX_TRIES:
                    break
            else:
                current_tries = 1



    # PRIVATE
    def __random_firefox_user_agent(self, min_version: float = 60.0) -> str:
        while True:
            agent = UserAgent().firefox

            try:
                version_str_comps = agent.split('/')[-1].strip().split('.', 1)
                version = float(version_str_comps[0] + '.' + version_str_comps[1].replace('.', ''))

                if version >= min_version:
                    return agent
            except:
                pass

    def __cookies_path(self, create_folder_if_not_exists: bool = True) -> str:
        url_comps = tldextract.extract(self.driver.current_url)
        formatted_url = url_comps.domain + '.' + url_comps.suffix

        return os.path.join(
            self.cookies_folder_path,
            formatted_url + '.pkl'
        )