# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union
import traceback

# Pip
import noraise

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Proxy ------------------------------------------------------------- #

class Proxy:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        host: str,
        port: Union[int, str],
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.host = host
        self.port = int(port) if isinstance(port, str) else port

        if not username or not password:
            username, password = None, None

        self.username = username
        self.password = password


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def string(self) -> str:
        proxy = '{}:{}'.format(self.host, self.port)

        if self.username and self.password:
            proxy = '{}:{}@{}'.format(self.username, self.password, proxy)

        return proxy

    @property
    def needs_auth(self) -> bool:
        return self.username and True


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_str(cls, proxy_str: str) -> Optional:
        try:
            comps = proxy_str.split('@')
            host, port = comps[-1].split(':')

            if len(comps) == 2:
                username, password = comps[0].split(':')
            else:
                username, password = None, None

            return cls(host, port, username, password)
        except:
            traceback.print_exc()

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #