from dataclasses import dataclass
from .errors import CacheLibNotFound
from requests import get
from urllib.parse import urljoin

DEFAULT_QUERY = {
    "fields": "text_url,group(id,title,description,isPaywalled,url,cover,user(name,username,avatar),lastPublishedPart,"
              "parts(id,title,text_url),tags)"

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

    def _fetch(self, path: str, query: dict) -> dict:
        response = get(
            urljoin(self.base_url, path),
            verify=True,
            headers={"User-Agent": self.user_agent},
            params=query
        )
        print(urljoin(self.base_url, path))
        return response.json()

    def fetch(self, path: str, query: dict = None) -> dict:
        if query is None:
            query = DEFAULT_QUERY
        if not self.use_cache:
            return self._fetch(path, query)
        response: dict  # for type checking
        if response := self.cache_obj.get(path) is not None:
            return response

        response = self._fetch(path, query)
        self.cache_obj[path] = response
        return response


def main():
    wpad = Wattpad(use_cache=False)
    url = "https://www.wattpad.com"
    print(urljoin(url, "v4/parts"))

    print(wpad.fetch("v4/parts/1321853334"))


if __name__ == "__main__":
    main()
