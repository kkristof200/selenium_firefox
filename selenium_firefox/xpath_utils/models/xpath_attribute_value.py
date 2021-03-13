# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .xpath_condition import XPathCondition
from .enums import XPathConditionType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: XpathAttributeValue ------------------------------------------------------ #

class XpathAttributeValue:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        value: any,
        condition_type: XPathConditionType
    ):
        self.value = value
        self.condition_type = condition_type


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def condition(
        self,
        attr_name: str
    ) -> XPathCondition:
        return XPathCondition(
            name=attr_name,
            value=self.value,
            condition_type=self.condition_type
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #