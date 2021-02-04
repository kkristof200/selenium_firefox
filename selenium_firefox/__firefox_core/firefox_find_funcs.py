# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union, Dict, Callable
import json

# Pip
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: FirefoxFindFuncs ------------------------------------------------------- #

class FirefoxFindFuncs:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    driver                   : WebDriver
    default_find_func_timeout: float


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

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


# ---------------------------------------------------------------------------------------------------------------------------------------- #