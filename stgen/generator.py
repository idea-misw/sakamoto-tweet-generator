import pickle
import random
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from .tokenizer import Tokenizer


BOS_TOKEN = '<bos>'
EOS_TOKEN = '<eos>'

PAIRED_SYMBOLS = [
    ('"', '"'),
    ("'", "'"),
    ('(', ')'),
    ('「', '」'),
    ('『', '』'),
    ('【', '】'),
    ('｢', '｣')
]

ERROR_MESSAGE = 'ﾀｽｹﾃｰｯｯ'

MAX_LENGTH = 280
NUM_TRIAL = 1000


@dataclass
class Chain:
    ngram_size: int = 3
    chain: Dict[Tuple[str, ...], List[str]] = field(default_factory=dict)
    learned_texts: Set[str] = field(default_factory=set)


class Generator:
    def __init__(self, ngram_size: Optional[int] = 3) -> None:
        self.tokenizer = Tokenizer()
        self.chain = Chain(ngram_size=ngram_size)

    def load_chain(self, file_path: str) -> None:
        with open(file_path, 'rb') as f:
            self.chain = pickle.load(f)

    def dump_chain(self, file_path: str) -> None:
        with open(file_path, 'wb') as f:
            pickle.dump(self.chain, f)

    def _calc_length(self, text: str) -> int:
        len_text = 0

        for char in text:
            len_char = (len(hex(ord(char))) - 1) // 2
            if len_char > 2:  # emojis
                len_char = 1

            len_text += len_char

        return len_text

    def _validate_text(self, text: str) -> bool:
        symbol_stack = []

        for char in text:
            for l_symbol, r_symbol in PAIRED_SYMBOLS:
                if char == l_symbol:
                    symbol_stack.append(l_symbol)

                elif char == r_symbol:
                    if len(symbol_stack) == 0:
                        return False

                    top_symbol = symbol_stack.pop()
                    if top_symbol != l_symbol:
                        return False

        if len(symbol_stack) > 0:
            return False

        return True

    def learn_text(self, text: str) -> None:
        ngram_size = self.chain.ngram_size

        tokens = (
            [BOS_TOKEN] * (ngram_size - 1)
            + self.tokenizer.tokenize(text)
            + [EOS_TOKEN]
        )

        for i in range(len(tokens) - ngram_size + 1):
            ngram = tuple(tokens[i:i+ngram_size-1])
            if ngram not in self.chain.chain:
                self.chain.chain[ngram] = []

            token = tokens[i+ngram_size-1]
            self.chain.chain[ngram].append(token)

        self.chain.learned_texts.add(text)

    def generate_text(self) -> str:
        ngram_size = self.chain.ngram_size
        chain = self.chain.chain
        learned_texts = self.chain.learned_texts

        if len(chain) == 0:
            return ERROR_MESSAGE

        for _ in range(NUM_TRIAL):
            ngram = (BOS_TOKEN,) * (ngram_size - 1)

            tokens = []
            while True:
                token = random.choice(chain[ngram])
                if token == EOS_TOKEN:
                    break
                
                tokens.append(token)
                ngram = ngram[1:] + (token,)

            text = ''.join(tokens)
            if self._calc_length(text) > MAX_LENGTH:
                continue
            if not self._validate_text(text):
                continue
            if text in learned_texts:
                continue

            return text
        
        return ERROR_MESSAGE
