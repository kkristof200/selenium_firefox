# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Local
from .xpath_condition import XPathCondition
from .enums import XPathConditionType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------- class: XPathConditionContains ---------------------------------------------------- #

class XPathConditionContains(XPathCondition):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[any] = None,
        **kwargs
    ):
        super().__init__(
            name=name,
            value=value,
            condition_type=XPathConditionType.CONTAINS,
            **kwargs
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #