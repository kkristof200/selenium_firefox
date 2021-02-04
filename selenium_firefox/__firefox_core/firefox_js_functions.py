# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import inspect, json

# Pip
from noraise import noraise

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: FirefoxJSFunctions ------------------------------------------------------ #

class FirefoxJSFunctions:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    driver: WebDriver


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def js_get_attribute(
        self,
        element: WebElement,
        key: str
    ) -> Optional:
        attrs = self.js_get_attributes(element)

        return attrs.get(key) if attrs else None

    @noraise()
    def js_get_attributes(
        self,
        element: WebElement
    ) -> Optional:
        return json.loads(
            self.execute_script_on_element(
                'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return JSON.stringify(items);',
                element
            )
        )
    # alias - kept for convenience
    get_attributes = js_get_attributes

    def js_click(
        self,
        element: WebElement
    ) -> bool:
        return self.execute_script_on_element('arguments[0].click();', element)

    def js_scroll_into_view(
        self,
        element: WebElement
    ) -> bool:
        return self.execute_script_on_element('arguments[0].scrollIntoView();', element)


    def js_get_user_agent(self) -> str:
        return self.execute_script("return navigator.userAgent;")


    def current_page_offset_y(self) -> float:
        return self.execute_script('return window.pageYOffset;')

    def scroll(
        self,
        amount: int
    ) -> None:
        self.scroll_to(self.current_page_offset_y()+amount)

    def scroll_to(
        self,
        position: int
    ) -> None:
        self.execute_script('window.scrollTo(0,{});'.format(position))


    def open_new_tab(
        self,
        url: Optional[str] = None
    ) -> bool:
        if url is None:
            url = ''

        if not self.execute_script('window.open("{}","_blank");'.format(url)):
            return False

        self.driver.switch_to.window(self.driver.window_handles[-1])

        return True


    def execute_script_on_element(
        self,
        script: str,
        element: WebElement
    ) -> bool:
        caller_name = inspect.stack()[2][3]

        if not element:
            print('{}: passed element is None'.format(caller_name))

            return False

        return self.execute_script(script, element)

    @noraise(default_return_value=False)
    def execute_script(
        self,
        script: str,
        element: Optional[WebElement] = None
    ) -> Optional[any]:
        res = self.driver.execute_script(script, element) if element else self.driver.execute_script(script)

        return res or True


# ---------------------------------------------------------------------------------------------------------------------------------------- #