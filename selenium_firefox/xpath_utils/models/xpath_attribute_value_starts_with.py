# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .xpath_attribute_value import XpathAttributeValue
from .enums import XPathConditionType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------- class: XpathAttributeValueStartsWith ------------------------------------------------- #

class XpathAttributeValueStartsWith(XpathAttributeValue):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        value: any
    ):
        super().__init__(
            value,
            XPathConditionType.STARTS_WITH
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #