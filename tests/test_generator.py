import os

from stgen.generator import ERROR_MESSAGE, Generator


TEXTS = [
    'サカモトなんていないのにね……',
    'みんなサカモト'
]
EXPECTED_TEXTS = [
    'サカモト',
    'みんなサカモトなんていないのにね……',
    ERROR_MESSAGE
]


def test_generator():
    generator = Generator(ngram_size=2)
    for text in TEXTS:
        generator.learn_text(text)

    generated_text = generator.generate_text()
    assert generated_text in EXPECTED_TEXTS


def test_generator_not_learn():
    generator = Generator(ngram_size=2)

    generated_text = generator.generate_text()
    assert generated_text == ERROR_MESSAGE


def test_generator_dump_load():
    generator = Generator(ngram_size=2)
    for text in TEXTS:
        generator.learn_text(text)

    file_path = os.path.join(os.path.dirname(__file__), 'test_dump.pickle')
    generator.dump_chain(file_path)

    generator = Generator(ngram_size=2)
    generator.load_chain(file_path)
    os.remove(file_path)

    generated_text = generator.generate_text()
    assert generated_text in EXPECTED_TEXTS
