import functools


@functools.cache
def handle_character(current: int, character: str, modulus: int) -> int:
    return (((current + ord(character)) % modulus) * 17) % modulus


@functools.cache
def elf_hash_function(initialization_step: str, modulus: int) -> int:
    _result = 0

    for character in initialization_step:
        _result = handle_character(current=_result, character=character, modulus=modulus)

    return _result
