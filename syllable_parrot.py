from random import choices
from typing import Dict, List, Optional

from pyphen import Pyphen
from tweepy_parrot import JSONParrot


class HaikuException(Exception):
    pass


class SyllableParrot(JSONParrot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.word_dict = Pyphen(lang='en')

    def _build_line(
        self,
        syllable_limit: int,
        markov_chain: Dict[str, Dict[str, int]],
        start_word: Optional[str] = None,
    ) -> str:
        line = ''
        current_keys = {}
        top_level = False

        if start_word:
            current_keys = markov_chain.get(start_word, {})

        if not current_keys:
            top_level = True
            current_keys = {
                key: 1
                for key in markov_chain.keys()
            }

        while syllable_limit > 0:
            syllable_map = {}
            for key, weight in current_keys.items():
                if key == '!':
                    continue
                syllable_count = len(self.word_dict.inserted(key).split('-'))
                if syllable_count > syllable_limit:
                    continue
                syllable_map[key] = weight

            if not syllable_map and not top_level:
                top_level = True
                current_keys = {
                    key: 1
                    for key in markov_chain.keys()
                }
                continue
            elif not syllable_map:
                break

            population, weights = zip(*syllable_map.items())
            next_word = choices(population=population, weights=weights)[0]
            syllable_limit -= len(
                self.word_dict.inserted(next_word).split('-')
            )
            line += ' ' + next_word
            current_keys = markov_chain.get(next_word, {})

        return line.title()

    def squawk(
        self,
        character_limit: int = 280,
        syllable_counts: Optional[List[int]] = None
    ) -> str:
        syllable_counts = syllable_counts or [5, 7, 5]
        markov_chain = self.read_data().markov_chain
        lines = []
        start_word = None
        for count in syllable_counts:
            next_line = self._build_line(count, markov_chain, start_word)
            parts = next_line.rsplit(maxsplit=1)
            if len(parts) > 1:
                __, start_word = parts
                start_word = start_word.lower()
            lines.append(next_line)

        if not all(lines):
            raise HaikuException('Not enough data')
        return '\n'.join(lines)
