from stgen.tokenizer import Tokenizer


def test_tokenizer():
    tokenizer = Tokenizer()
    
    text = '"サカ モト"なんて\nいないのに#ね……'
    tokenized_text = tokenizer.tokenize(text)
    assert tokenized_text == [
        '"', 'サカ', ' ', 'モト', '"', 'なんて', '\n',
        'い', 'ない', 'のに', '#', 'ね', '……'
    ]
