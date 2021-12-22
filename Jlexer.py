from constants import *

JSON_QUOTE = '"'
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')

##c.id.event.on | whey we are in trouble
def lex_words(words):
    json_words = ''

    if words[0] == JSON_QUOTE:
        words = words[1:]
    else:
        return None, words

    for c in words:
        if c == JSON_QUOTE:
            return json_words, words[len(json_words)+1:]
        else:
            json_words += c

    raise Exception('Expected end-of-words quote')


def lex_number(words):
    json_number = ''

    number_characters = [str(d) for d in range(0, 10)] + ['-', 'e', '.']

    for c in words:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = words[len(json_number):]

    if not len(json_number):
        return None, words

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def lex_bool(words):
    words_len = len(words)

    if words_len >= TRUE_LEN and \
         words[:TRUE_LEN] == 'true':
        return True, words[TRUE_LEN:]
    elif words_len >= FALSE_LEN and \
         words[:FALSE_LEN] == 'false':
        return False, words[FALSE_LEN:]

    return None, words


def lex_null(words):
    words_len = len(words)

    if words_len >= NULL_LEN and \
         words[:NULL_LEN] == 'null':
        return True, words[NULL_LEN]

    return None, words


def lex(words):
    tokens = []

    while len(words):
        json_words, words = lex_words(words)
        if json_words is not None:
            tokens.append("string")
            continue

        json_number, words = lex_number(words)
        if json_number is not None:
            tokens.append("number")
            continue

        json_bool, words = lex_bool(words)
        if json_bool is not None:
            if json_bool :
                tokens.append("True")
            else :
                tokens.append("False")
            continue

        json_null, words = lex_null(words)
        if json_null is not None:
            tokens.append("null")
            continue

        c = words[0]

        if c in JSON_WHITESPACE:
            # Ignore whitespace
            words = words[1:]
        elif c in JSON_SYNTAX:
            tokens.append(c)
            words = words[1:]
        else:
            raise Exception('Unexpected character: {}'.format(c))
    tokens.append('$')

    return tokens
