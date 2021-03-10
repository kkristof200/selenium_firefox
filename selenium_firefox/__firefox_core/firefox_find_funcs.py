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

# Local
from ..xpath_utils import XPathUtils, XPathCondition, XPathConditionRelation

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
        in_element: Optional[WebElement] = None,
        timeout: Optional[int] = None,
        conditions: Optional[List[XPathCondition]] = None,
        condition_relation: Optional[XPathConditionRelation] = None,
        **kwargs
    ) -> Optional[WebElement]:
        return self.find(
            By.XPATH,
            XPathUtils.generate_xpath(tag=type_, attributes=attributes, conditions=conditions, condition_relation=condition_relation, for_sub_element=in_element is not None, **kwargs),
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
        in_element: Optional[WebElement] = None,
        timeout: Optional[int] = None,
        conditions: Optional[List[XPathCondition]] = None,
        condition_relation: Optional[XPathConditionRelation] = None,
        **kwargs
    ) -> List[WebElement]:
        return self.find_all(
            By.XPATH,
            XPathUtils.generate_xpath(tag=type_, attributes=attributes, conditions=conditions, condition_relation=condition_relation, for_sub_element=in_element is not None, **kwargs),
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