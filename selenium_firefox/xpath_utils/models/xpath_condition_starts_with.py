# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Local
from .xpath_condition import XPathCondition
from .enums import XPathConditionType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------- class: XPathConditionStartsWith --------------------------------------------------- #

class XPathConditionStartsWith(XPathCondition):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        name: str = None,
        value = None,
        **kwargs
    ):
        super().__init__(
            name=name,
            value=value,
            condition_type=XPathConditionType.STARTS_WITH,
            **kwargs
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #