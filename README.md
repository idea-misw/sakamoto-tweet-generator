# Sakamoto Tweet Generator

Sakamoto Tweet Generator (サカモトツイートジェネレータ) generates a sentence that reminds us of [Sakamoto](https://twitter.com/sksk_sskn).

```python
>>> from skgen import Generator

>>> generator = Generator()
>>> generator.load_chain('chain.pickle')

>>> generator.generate_text()
'ざむちゃんが1000人'
```

Actually, this is a _primitive_ sentence generator based on morphological analysis and Markov chains. Under the two concepts, it generates a Sakamoto-like sentence by

- analyzing a number of Sakamoto's tweets into sequences of morphemes and
- building a Markov model (trigram-based by default) with the analyzed tweets.

**Note:** For morphological analysis, the generator uses [Juman++](https://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN%2B%2B) via [PyKNP](https://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP).
