from typing import Self, List
from stringzilla import Str, File, SplitIterator
from collections import defaultdict
from random import choice
from textwrap import fill


class MarkovChainGenerator:
    def __init__(
        self: Self, input_file_name: str, output_file_name: str, number_of_words: int
    ) -> None:
        self.input_file_name: str = input_file_name
        self.output_file_name: str = output_file_name
        self.number_of_words = number_of_words
        self.word1: str = ""
        self.word2: str = ""
        self.possibles: defaultdict = defaultdict(list)

    def generate_text(self: Self, overwrite_file: bool = False) -> None:
        self._generate_dict()
        print(self.possibles)

        self.word1, self.word2 = choice(
            [k for k in self.possibles if k[0][:1].isupper()]
        )
        output: List[str] = [self.word1, self.word2]
        for _ in range(self.number_of_words):
            word = choice(self.possibles[(self.word1, self.word2)])
            output.append(word)
            self.word1, self.word2 = self.word2, word

        with open(self.output_file_name, "w" if overwrite_file else "a") as f:
            f.write(fill(" ".join(output)))

    def _generate_dict(self: Self) -> None:
        words: SplitIterator[Str] = Str(File(self.input_file_name)).split_charset_iter(
            separator="\n\t\r "
        )

        for word in words:
            if not word:
                continue

            word = str(word)
            self.possibles[(self.word1, self.word2)].append(word)
            self.word1, self.word2 = self.word2, word

        self.possibles[self.word1, self.word2].append("")
        self.possibles[self.word2, ""].append("")
