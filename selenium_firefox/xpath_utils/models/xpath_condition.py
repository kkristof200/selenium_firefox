# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import json

# Local
from .enums import XPathConditionType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: XPathCondition -------------------------------------------------------- #

class XPathCondition:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[any] = None,
        condition_type: XPathConditionType = XPathConditionType.EQUALS,
        **kwargs
    ):
        if name and value:
            kwargs = {name: value}

        k = list(kwargs.keys())[0]
        v = kwargs[k]

        if not isinstance(v, str):
            v = json.dumps(v)

        if k != 'class' and k.strip('_') == 'class':
            k = 'class'
        elif k != 'id' and k.strip('_') == 'id':
            k = 'id'

        self.__name = k
        self.__value = v

        k = '@{}'.format(k)

        if condition_type == XPathConditionType.CONTAINS:
            self.__xpath_value = 'contains({}, \'{}\')'.format(k, v)
        elif condition_type == XPathConditionType.STARTS_WITH:
            self.__xpath_value = 'starts-with({}, \'{}\')'.format(k, v)
        else:
            self.__xpath_value = '{}=\'{}\''.format(k, v)


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> str:
        return self.__value

    @property
    def xpath_value(self) -> str:
        return self.__xpath_value


# ---------------------------------------------------------------------------------------------------------------------------------------- #