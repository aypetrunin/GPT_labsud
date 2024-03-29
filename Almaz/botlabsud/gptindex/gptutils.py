import tiktoken

def num_tokens_from_string( string: str) -> int:
    """Возвращает количество токенов в строке"""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens
