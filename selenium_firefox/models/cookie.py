# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Dict
import time

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Cookie ------------------------------------------------------------ #

class Cookie:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: Dict[str, any]
    ):
        self.__d = d


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def name(self) -> str:
        return self.__d.get('name')

    @property
    def value(self) -> str:
        return self.__d.get('value')

    @property
    def path(self) -> str:
        return self.__d.get('path')

    @property
    def domain(self) -> str:
        return self.__d.get('domain')

    @property
    def secure(self) -> bool:
        return self.__d.get('secure')

    @property
    def expiry(self) -> Optional[int]:
        return self.__d.get('expiry')

    @property
    def dict(self) -> Dict[str, any]:
        return self.__d


    # calculated properties

    # This returns false for session cookies too, when loaded, since I couldn't determine if the session is the current one or not
    @property
    def is_expired(self) -> bool:
        seconds_till_expired = self.seconds_till_expired

        return seconds_till_expired is not None and seconds_till_expired > 0

    @property
    def seconds_till_expired(self) -> Optional[int]:
        expiry = self.expiry

        return int(time.time()) - expiry if expiry is not None else None

    @property
    def is_session_cookie(self) -> bool:
        return self.expiry is None


# ---------------------------------------------------------------------------------------------------------------------------------------- #