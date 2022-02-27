from typing import List

from pyknp import Juman


ESCAPE_MAP = {'"': '‘', '#': '’'}


class Tokenizer:
    def __init__(self) -> None:
        self.jumanpp = Juman()

    def tokenize(self, text: str) -> List[str]:
        tokens = []

        for line in text.split('\n'):
            for sentence in line.split(' '):
                for old_symbol, new_symbol in ESCAPE_MAP.items():
                    sentence = sentence.replace(old_symbol, new_symbol)

                result = self.jumanpp.analysis(sentence)

                for mrph in result.mrph_list():
                    midasi = mrph.midasi
                    for new_symbol, old_symbol in ESCAPE_MAP.items():
                        midasi = midasi.replace(old_symbol, new_symbol)

                    tokens.append(midasi)

                tokens.append(' ')

            else:
                del tokens[-1]

            tokens.append('\n')

        else:
            del tokens[-1]

        return tokens
