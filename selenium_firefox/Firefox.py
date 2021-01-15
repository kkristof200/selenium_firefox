# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, List, Dict, Callable, Tuple
import pickle, os, time, json, inspect

# Pip
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as by
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from fake_useragent import UserAgent
import tldextract

By = by
Keys = Keys

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------------- Defines ---------------------------------------------------------------- #

RANDOM_USERAGENT = 'random'

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Firefox ------------------------------------------------------------ #

class Firefox:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        cookies_folder_path: Optional[str] = None,
        extensions_folder_path: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        cookies_id: Optional[str] = None,
        firefox_binary_path: Optional[str] = None,
        # proxy: Optional[str] = None,
        profile_path: Optional[str] = None,
        private: bool = False,
        screen_size: Optional[Tuple[int, int]] = None, # (width, height)
        full_screen: bool = True,
        headless: bool = False,
        language: str = 'en-us',
        manual_set_timezone: bool = False,
        user_agent: Optional[str] = None,
        load_proxy_checker_website: bool = False,
        disable_images: bool = False,
        default_find_func_timeout: int = 2.5
    ):
        '''EITHER PROVIDE 'cookies_id' OR  'cookies_folder_path'.
           IF 'cookies_folder_path' is None, 'cokies_id', will be used to calculate 'cookies_folder_path'
           IF 'cokies_id' is None, it will become 'test'
        '''

        self.default_find_func_timeout = default_find_func_timeout

        if cookies_folder_path is None:
            cookies_id = cookies_id or 'test'

            current_folder_path = os.path.dirname(os.path.abspath(__file__))
            general_cookies_folder_path = os.path.join(current_folder_path, 'cookies')
            os.makedirs(general_cookies_folder_path, exist_ok=True)

            cookies_folder_path = os.path.join(general_cookies_folder_path, cookies_id)

        self.cookies_folder_path = cookies_folder_path
        os.makedirs(self.cookies_folder_path, exist_ok=True)

        user_agent_file_path = os.path.join(cookies_folder_path, 'ua.txt')

        if user_agent:
            user_agent = user_agent.strip()

            if not os.path.exists(user_agent_file_path):
                with open(user_agent_file_path, 'w') as f:
                    f.write(user_agent)
        else:
            if os.path.exists(user_agent_file_path):
                with open(user_agent_file_path, 'r') as f:
                    user_agent = f.read()

        profile = webdriver.FirefoxProfile(profile_path if profile_path and os.path.exists(profile_path) else None)

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

            profile.set_preference('general.useragent.override', user_agent)

        self.__user_agent = user_agent
        self.__proxy_port = port
        self.__proxy_host = host

        if language is not None:
            profile.set_preference('intl.accept_languages', language)

        if private:
            profile.set_preference('browser.privatebrowsing.autostart', True)
        
        if disable_images:
            profile.set_preference('permissions.default.image', 2)
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        
        if host is not None and port is not None:
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http', host)
            profile.set_preference('network.proxy.http_port', port)
            profile.set_preference('network.proxy.ssl', host)
            profile.set_preference('network.proxy.ssl_port', port)
            profile.set_preference('network.proxy.ftp', host)
            profile.set_preference('network.proxy.ftp_port', port)
            profile.set_preference('network.proxy.socks', host)
            profile.set_preference('network.proxy.socks_port', port)
            profile.set_preference('network.proxy.socks_version', 5)
            profile.set_preference('signon.autologin.proxy', True)
        
        profile.set_preference('marionatte', False)
        profile.set_preference('dom.webdriver.enabled', False)
        profile.set_preference('media.peerconnection.enabled', False)
        profile.set_preference('useAutomationExtension', False)

        profile.set_preference('general.warnOnAboutConfig', False)
        profile.update_preferences()
        options = FirefoxOptions()

        if screen_size is not None:
            options.add_argument('--width={}'.format(screen_size[0]))
            options.add_argument('--height={}'.format(screen_size[1]))

        if headless:
            options.add_argument('--headless')

        # seleniumwire_options = {
        #     'suppress_connection_errors': True
        # }

        # if proxy:
        #     if type(proxy) == str:
        #         proxy = proxy.strip().lstrip('https://').lstrip('http://').lstrip('ftp://')

        #         seleniumwire_options['proxy'] = {
        #             'https': 'https://{}'.format(proxy),
        #             'http': 'http://{}'.format(proxy),
        #             'ftp': 'ftp://{}'.format(proxy)
        #         }
        # else:
        #     seleniumwire_options = None

        ff_binary = FirefoxBinary(firefox_path=firefox_binary_path) if firefox_binary_path and os.path.exists(firefox_binary_path) else None

        self.driver = webdriver.Firefox(
            firefox_profile=profile,
            firefox_options=options,
            # seleniumwire_options=seleniumwire_options,
            firefox_binary=ff_binary
        )

        if full_screen:
            self.driver.fullscreen_window()

        if extensions_folder_path is not None:
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


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def user_agent(self) -> str:
        self.__user_agent = self.__user_agent or self.js_get_user_agent()

        return self.__user_agent


    # proxy

    @property
    def proxy_host(self) -> Optional[str]:
        return self.__proxy_host

    @property
    def proxy_port(self) -> Optional[int]:
        return self.__proxy_port

    @property
    def proxy_str(self) -> Optional[str]:
        return '{}:{}'.format(self.proxy_host, self.proxy_port) if self.proxy_host and self.proxy_port is not None else None


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def login_via_cookies(self, url: str, needed_cookie_name: Optional[str] = None) -> bool:
        org_url = self.driver.current_url
        self.get(url)
        time.sleep(0.5)

        try:
            if self.has_cookies_for_current_website():
                self.load_cookies()
                time.sleep(1)
                self.refresh()
                time.sleep(1)
            else:
                self.get(org_url)

                return False

            for cookie in self.driver.get_cookies():
                if needed_cookie_name is not None:
                    if 'name' in cookie and cookie['name'] == needed_cookie_name:
                        self.get(org_url)

                        return True
                else:
                    for k, v in cookie.items():
                        if k == 'expiry':
                            if v - int(time.time()) < 0:
                                self.get(org_url)

                                return False
        except Exception as e:
            print(e)
            self.get(org_url)

            return False

        self.get(org_url)

        return needed_cookie_name is None

    def has_cookie(self, cookie_name: str) -> bool:
        for cookie in self.driver.get_cookies():
            if 'name' in cookie and cookie['name'] == cookie_name:
                return True

        return False

    def get(
        self,
        url: str,
        force: bool = False
    ) -> bool:
        if not force:
            to_remove = ['http://', 'https://', 'www.']

            clean_current = self.driver.current_url
            clean_new = url

            for _to_remove in to_remove:
                clean_current = clean_current.replace(_to_remove, '')
                clean_new = clean_new.replace(_to_remove, '')

            if clean_current.strip('/') == clean_new.strip('/'):
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
        timeout: Optional[int] = None
    ) -> Union[Optional[WebElement], List[WebElement]]:
        return self.__find(
            by,
            EC.presence_of_element_located,
            key,
            element=element,
            timeout=timeout
        )

    def find_by(
        self,
        type_: Optional[str] = None, #div, a, span, ...
        attributes: Optional[Dict[str, str]] = None,
        id_: Optional[str] = None,
        class_: Optional[str] = None,
        in_element: Optional[WebElement] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Optional[WebElement]:
        return self.find(
            By.XPATH,
            self.generate_xpath(type_=type_, attributes=attributes, id_=id_, class_=class_, for_sub_element=in_element is not None, **kwargs),
            element=in_element,
            timeout=timeout
        )

    # aliases
    bsfind = find_by
    find_ = find_by

    def reload_element(
        self,
        element,
        timeout: Optional[int] = None
    ) -> Optional[WebElement]:
        return self.find(
            By.XPATH,
            key=element.get_xpath(),
            timeout=timeout
        )

    def find_all(
        self,
        by: By,
        key: str,
        element: Optional = None,
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        return self.__find(
            by,
            EC.presence_of_all_elements_located,
            key,
            element=element,
            timeout=timeout
        )

    def find_all_by(
        self,
        type_: Optional[str] = None, #div, a, span, ...
        attributes: Optional[Dict[str, str]] = None,
        id_: Optional[str] = None,
        class_: Optional[str] = None,
        in_element: Optional[WebElement] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> List[WebElement]:
        return self.find_all(
            By.XPATH,
            self.generate_xpath(type_=type_, attributes=attributes, id_=id_, class_=class_, for_sub_element=in_element is not None, **kwargs),
            element=in_element,
            timeout=timeout
        )

    # aliases
    bsfind_all = find_all_by
    find_all_ = find_all_by

    def get_attribute(self, element, key: str) -> Optional[str]:
        try:
            return element.get_attribute(key)
        except:
            return None

    def get_attributes(self, element) -> Optional[Dict[str, str]]:
        try:
            return json.loads(
                self.driver.execute_script(
                    'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return JSON.stringify(items);',
                    element
                )
            )
        except:
            return None

    def save_cookies(self, cookies: Optional[List[Dict]] = None) -> None:
        cookies_path = self.__cookies_path()

        try:
            os.remove(cookies_path)
        except:
            pass

        pickle.dump(
            cookies or self.driver.get_cookies(),
            open(self.__cookies_path(), 'wb')
        )

    def load_cookies(self) -> None:
        if not self.has_cookies_for_current_website():
            self.save_cookies()

            return

        cookies = pickle.load(open(self.__cookies_path(), 'rb'))
        should_save = False
        cookies_to_save = []

        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
                cookies_to_save.append(cookie)
            except Exception as e:
                should_save = True
                print('Error while loading cookie:', e)
                print(json.dumps(cookie, indent=4))
        
        if should_save:
            self.save_cookies(cookies_to_save)

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
        self.scroll_to(self.current_page_offset_y()+amount)
    
    def scroll_to(self, position: int) -> None:
        try:
            self.driver.execute_script('window.scrollTo(0,'+str(position)+');')
        except:
            pass

    def scroll_to_element(self, element, header_element=None):
        try:
            header_h = 0

            if header_element is not None:
                _, _, _, header_h, _, _ = self.get_element_coordinates(header_element)

            _, element_y, _, _, _, _ = self.get_element_coordinates(element)

            self.scroll_to(element_y-header_h)
        except Exception as e:
            print('scroll_to_element', e)
    
    def move_to_element(self, element: Optional[WebElement]) -> bool:
        if not element:
            print('move_to_element: None element passed')

            return False

        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            return True
        except Exception as e:
            print('move_to_element', e)

            return False

    def switch_to_frame(self, iframe: Optional[WebElement]) -> bool:
        if not iframe:
            print('switch_to_frame: None frame passed')

            return False

        try:
            self.driver.switch_to.frame(iframe)

            return True
        except Exception as e:
            print('switch_to_frame', e)

            return False

    # returns x, y, w, h, max_x, max_y
    def get_element_coordinates(self, element) -> Tuple[int, int, int, int, int, int]:
        location = element.location
        size = element.size

        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']

        return x, y, w, h, x+w, y+h

    def current_page_offset_y(self) -> float:
        return self.driver.execute_script('return window.pageYOffset;')

    def open_new_tab(self, url: str) -> None:
        if url is None:
            url = ''

        cmd = 'window.open("'+url+'","_blank");'
        self.driver.execute_script(cmd)
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    @staticmethod
    def generate_xpath(
        type_: Optional[str] = None, #div, a, span, ...
        attributes: Optional[Dict[str, str]] = None,
        id_: Optional[str] = None,
        class_: Optional[str] = None,
        for_sub_element: bool = False, # selenium has a bug with xpath. If xpath does not start with '.' it will search in the whole doc
        **kwargs
    ) -> str:
        attributes = attributes or {}

        if class_ is not None:
            attributes['class'] = class_

        if id_ is not None:
            attributes['id'] = id_

        attributes.update({k:(v if type(v) == str else json.dumps(v)) for k, v in kwargs.items()})
        type_ = type_ or '*'
        xpath_query = ''

        for key, value in attributes.items():
            if len(xpath_query) > 0:
                xpath_query += ' and '

            xpath_query += '@' + key + '=\'' + value + '\''

        return ('.' if for_sub_element else '') + '//' + type_ + (('[' + xpath_query + ']') if len(xpath_query) > 0 else '')


    # JS
    def js_click(self, element: WebElement) -> bool:
        return self.execute_script_on_element('arguments[0].click();', element)

    def js_scroll_into_view(self, element: WebElement) -> bool:
        return self.execute_script_on_element('arguments[0].scrollIntoView();', element)

    def js_get_user_agent(self) -> str:
        return self.execute_script("return navigator.userAgent;")

    def execute_script_on_element(self, script: str, element: WebElement) -> bool:
        caller_name = inspect.stack()[2][3]

        if not element:
            print('{}: passed element is None'.format(caller_name))

            return False

        return self.execute_script(script, element)

    def execute_script(self, script: str, element: Optional[WebElement] = None) -> bool:
        try:
            self.driver.execute_script(script, element) if element else self.driver.execute_script(script)

            return True
        except Exception as e:
            print('{}: {} - {}'.format(inspect.stack()[2][3], script, e))

            return False

    def quit(self) -> bool:
        try:
            self.driver.quit()

            return True
        except Exception as e:
            print('Error - Firefox: quit() - ', e)

            return False

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


    # --------------------------------------------------------- Destructor ----------------------------------------------------------- #

    def __del__(self):
        try:
            self.quit()
        except Exception as e:
            print('Error - Firefox: __del__() - ', e)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __find(
        self,
        by: By,
        find_func: Callable,
        key: str,
        element: Optional = None,
        timeout: Optional[int] = None
    ) -> Union[Optional[WebElement], List[WebElement]]:
        timeout = timeout if timeout is not None else self.default_find_func_timeout

        if element is None:
            element = self.driver
        elif by == By.XPATH and not key.startswith('.'):
            # selenium has a bug with xpath. If xpath does not start with '.' it will search in the whole doc
            key = '.' + key

        try:
            es = WebDriverWait(element, timeout).until(
                find_func((by, key))
            )

            return es
        except:
            return None

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


# ---------------------------------------------------------------------------------------------------------------------------------------- #