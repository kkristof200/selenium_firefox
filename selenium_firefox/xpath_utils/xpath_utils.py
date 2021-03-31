# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Dict

# Local
from .models import XPathCondition, XPathConditionEquals, XPathConditionRelation, XpathAttributeValue

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: XPathUtils ---------------------------------------------------------- #

class XPathUtils:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @staticmethod
    def generate_xpath(
        *args,
        tag: Optional[str] = None, #div, a, span, ...
        attributes: Optional[Dict[str, any]] = None,
        for_sub_element: bool = False, # selenium has a bug with xpath. If xpath does not start with '.' it will search in the whole doc
        conditions: Optional[List[XPathCondition]] = None,
        condition_relation: Optional[XPathConditionRelation] = None,
        **kwargs
    ) -> str:
        for_sub_element = for_sub_element or False

        if not tag:
            probable_tags = [a for a in args if isinstance(a, str)]

            if probable_tags:
                tag = probable_tags[-1]

        if condition_relation is None:
            probable_condition_relations = [a for a in args if isinstance(a, XPathConditionRelation)]

            if probable_condition_relations:
                condition_relation = probable_condition_relations[-1]
            else:
                condition_relation = XPathConditionRelation.AND

        conditions = conditions or []
        conditions.extend([a for a in args if isinstance(a, XPathCondition)])

        attributes = attributes or {}

        for a in [a for a in args if isinstance(a, dict)]:
            attributes.update(a)

        attributes.update(kwargs)

        if attributes:
            for k, v in attributes.items():
                conditions.append(v.condition(k) if isinstance(v, XpathAttributeValue) else XPathConditionEquals(k, v))

        return '{}//{}{}'.format(
            '.' if for_sub_element else '',
            tag or '*',
            '[{}]'.format(
                ' {} '.format(condition_relation.value).join(
                    [c.xpath_value for c in conditions]
                )
            ) if conditions else ''
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #