from requests import get, Response
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List, Self, Dict
from random import sample
from asyncio import gather


class GutenbergScraper:
    def __init__(self: Self, output_file_name: str) -> None:
        self.text_url: str = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
        self.output_file_name: str = output_file_name
        self.cache: Dict[str, int] = dict()

    def get_random_ids(
        self: Self, length: int, ignore_cache: bool = False
    ) -> List[int]:
        if ignore_cache or "max_id" not in self.cache:
            response: Response = get(
                url="https://www.gutenberg.org/ebooks/search/?sort_order=release_date"
            )
            soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
            max_id: int = int(
                soup.find(attrs={"class": "link", "accesskey": "5"})
                .get("href")  # pyright: ignore
                .split("/")[-1]  # pyright: ignore
            )
            self.cache["max_id"] = max_id

        return sample(range(1, self.cache["max_id"] + 1), k=length)

    async def save_book_texts(
        self: Self, amount: int, overwrite_file: bool = False
    ) -> None:
        if overwrite_file:
            with open(self.output_file_name, "w") as f:
                f.close()

        async with ClientSession() as session:
            tasks = [
                self._save_book_text(id, session)
                for id in self.get_random_ids(length=amount)
            ]
            await gather(*tasks)

    async def _save_book_text(
        self: Self, id: int, session: ClientSession
    ) -> None:
        url: str = self.text_url.format(id=id)

        async with session.get(url=url) as response:
            soup: BeautifulSoup = BeautifulSoup(await response.text(), "html.parser")

            with open(
                self.output_file_name, "a"
            ) as f:
                f.write(soup.get_text())
