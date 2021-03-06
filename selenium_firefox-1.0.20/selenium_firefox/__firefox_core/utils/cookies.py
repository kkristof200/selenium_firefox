# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Dict, Tuple, Union
import os, pickle, json

# Pip
import tldextract

# Local
from ...models import Cookie

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Cookies ------------------------------------------------------------ #

class Cookies:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def load(
        cls,
        url: str,
        folder_path: str
    ) -> Optional[List[Cookie]]:
        saved_cookies_path = cls.saved_cookies_path(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=False,
            delete_old_if_both_exists=False
        )

        if not saved_cookies_path:
            return None

        cookies = pickle.load(open(saved_cookies_path, 'rb')) if saved_cookies_path.endswith('.pkl') else json.load(open(saved_cookies_path, 'rb'))

        return [Cookie(cookie_dict) for cookie_dict in cookies]

    @classmethod
    def save(
        cls,
        url: str,
        folder_path: str,
        cookies: List[Union[Cookie, Dict[str, any]]],
        pickled: bool
    ) -> bool:
        if not cookies:
            print('Value passed for \'cookies\' is None or empty so will not save it. Use \'.delete_cookies\' to delete it.')

            return False

        cookies_path = cls.cookies_path(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=True,
            pickled=pickled,
            delete_old_if_both_exists=True
        )

        if os.path.exists(cookies_path):
            os.remove(cookies_path)

        _cookies = [c.dict if isinstance(c, Cookie) else c for c in cookies]

        pickle.dump(
            _cookies,
            open(cookies_path, 'wb')
        ) if pickled else json.dump(
            _cookies,
            open(cookies_path, 'w')
        )

        return True

    @classmethod
    def delete(
        cls,
        url: str,
        folder_path: str
    ) -> bool:
        did_remove_any_cookies = False

        for p in cls.possible_saved_cookies_paths(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=False,
            delete_old_if_both_exists=False
        ):
            if os.path.exists(p):
                did_remove_any_cookies = True
                os.remove(p)

        if not did_remove_any_cookies:
            print('No cookies found to delete for url \'{}\''.format(url))

        return did_remove_any_cookies

    @classmethod
    def has_saved_cookies(
        cls,
        url: str,
        folder_path: str
    ) -> bool:
        path = cls.saved_cookies_path(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=False,
            delete_old_if_both_exists=False
        )

        return path and os.path.exists(path)

    @classmethod
    def saved_cookies_path(
        cls,
        url: str,
        folder_path: str,
        create_folder_if_not_exists: bool,
        delete_old_if_both_exists: bool
    ) -> Optional[str]:
        p_pickled, p_json = cls.possible_saved_cookies_paths(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=create_folder_if_not_exists,
            delete_old_if_both_exists=delete_old_if_both_exists
        )

        pickled_exists = os.path.exists(p_pickled)
        json_exists = os.path.exists(p_json)

        if not delete_old_if_both_exists and pickled_exists and json_exists:
            return p_pickled if os.path.getmtime(p_pickled) > os.path.getmtime(p_json) else p_json

        return p_pickled if pickled_exists else p_json if json_exists else None

    @classmethod
    def cookies_path(
        cls,
        url: str,
        folder_path: str,
        create_folder_if_not_exists: bool,
        pickled: bool,
        delete_old_if_both_exists: bool
    ) -> str:
        return cls.possible_saved_cookies_paths(
            url=url,
            folder_path=folder_path,
            create_folder_if_not_exists=create_folder_if_not_exists,
            delete_old_if_both_exists=delete_old_if_both_exists
        )[0 if pickled else 1]

    @staticmethod
    def possible_saved_cookies_paths(
        url: str,
        folder_path: str,
        create_folder_if_not_exists: bool,
        delete_old_if_both_exists: bool
    ) -> Tuple[str, str]:
        url_comps = tldextract.extract(url)

        if create_folder_if_not_exists and not os.path.exists(folder_path):
            os.makedirs(folder_path)

        base_path = os.path.join(
            folder_path,
            '{}.{}'.format(
                url_comps.domain,
                url_comps.suffix,
            )
        )

        p_picked, p_json = '{}.pkl'.format(base_path), '{}.json'.format(base_path)

        if delete_old_if_both_exists and os.path.exists(p_picked) and os.path.exists(p_json):
            os.remove(p_json if os.path.getmtime(p_picked) > os.path.getmtime(p_json) else p_picked)

        return p_picked, p_json


# ---------------------------------------------------------------------------------------------------------------------------------------- #