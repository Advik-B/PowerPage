from dataclasses import dataclass
from ..errors import CacheLibNotFound, NotFoundError
from requests import get
from urllib.parse import urljoin

DEFAULT_QUERY = {
    "fields": "text_url,group(id,title,description,isPaywalled,url,cover,user(name,username,avatar),lastPublishedPart,"
              "parts(id,title,text_url),tag)"

}

@dataclass
class Wattpad:
    base_url: str = "https://www.wattpad.com"
    use_cache: bool = True
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )

    def __post_init__(self) -> None:
        if self.use_cache:
            try:
                from diskcache import Cache
                self.cache_obj = Cache("capacitor")
            except (ImportError, ModuleNotFoundError) as e:
                print("😂🫵🏻", flush=False)
                raise CacheLibNotFound(
                    "diskcache not found in the current python interpreter\n"
                    "either install it using pip or set use_cache=False"
                ) from e

    def _fetch(self, path: str, query: dict, jayson=True) -> dict | str:
        response = get(
            urljoin(self.base_url, path),
            verify=True,
            headers={"User-Agent": self.user_agent},
            params=query
        )
        # print(urljoin(self.base_url, path))
        if jayson:
            return response.json()
        else:
            return response.text

    def fetch(self, path: str, query: dict = None, expect_json=True) -> dict | str:
        if path.startswith('/'):
            path = path.removeprefix('/')

        if query is None:
            query = {}
        
        def handle_response(response: dict | str) -> dict:
            if type(response) != dict: # Don't fuck with other stuff    
                return response
            if response.get('error_code', None) == 1017:
                raise NotFoundError(response)
            return response
        
        if not self.use_cache:
            response = self._fetch(path, query, jayson=expect_json)
            return handle_response(response)
        response: dict  # for type checking
        if response := self.cache_obj.get(path):
            return handle_response(response)

        response = self._fetch(path, query, jayson=expect_json)
        self.cache_obj[path] = response
        return handle_response(response)
