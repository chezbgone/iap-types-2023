from __future__ import annotations
from typing import Callable, Generic, TypeVar
from dataclasses import dataclass

###########
## Types ##
###########

A = TypeVar('A')
B = TypeVar('B')

@dataclass
class ParseResult(Generic[A]):
    result: A
    remaining: str

@dataclass
class Parser(Generic[A]):
    # can raise ParserError
    parse: Callable[[str], ParseResult[A]]

    def map(self, map_f: Callable[[A], B]) -> Parser[B]:
        raise NotImplementedError

    # maybe return only the B
    def then(self, next: Parser[B]) -> Parser[B]:
        def parse(input: str) -> ParseResult[B]:
            match self.parse(input):
                case ParseResult(result=_, remaining=rest_a):
                    match next.parse(rest_a):
                        case ParseResult(result=result_b, remaining=rest_b):
                            return ParseResult(result_b, rest_b)
        return Parser(parse)
    
    # TODO define >> and << to ignore some sides
    

def seq(*parsers: Parser[A]) -> Parser[tuple[A, ...]] :
    def parse(input: str) -> ParseResult[tuple[A, ...]]:
        result_accumulator = ()
        remaining_input = input
        for parser in parsers:
            match parser.parse(remaining_input):
                case ParseResult(result=result, remaining=rest):
                    result_accumulator += (result,)
                    remaining_input = rest
        return ParseResult(result_accumulator, remaining_input)
    return Parser(parse)



############
## Errors ##
############

class ParserError(Exception):
    pass

class UnexpectedEOF(ParserError):
    def __init__(self):
        super().__init__(f'Unexpected EOF')

class UnexpectedChar(ParserError):
    def __init__(self, char: str):
        super().__init__(f'Unexpected {repr(char)}')

#################
## Combinators ##
#################

# Problems:
# - didn't specify which character to parse
# - deal with remaining input
# - deal with errors


def char_parser(c: str) -> Parser[str]:
    # char_parser('[').parse('[A]')
    # >>> Result('[', 'A]')

    # char_parser('A').parse('[A]')
    # >>> error
    def parse(input: str) -> ParseResult[str]:
        if not input:
            raise UnexpectedEOF()
        first = input[0]
        if first == c:
            return ParseResult(first, input[1:])
        raise UnexpectedChar(first)
    return Parser(parse)

@Parser
def any_char_parser(input: str) -> ParseResult[str]:
    if not input:
        raise UnexpectedEOF()
    first = input[0]
    return ParseResult(first, input[1:])

##########
## Main ##
##########

#block_parser = char_parser('[').then(any_char_parser).then(char_parser(']'))
# block_parser = char_parser('[') >> any_char_parser << char_parser(']')
block_parser = seq(char_parser('['), any_char_parser, char_parser(']'))


@dataclass
class Block:
    ...

# parse_block.map(Block).parse('[A]')
# >> ParseResult(result=Block('A'), remaining=...)

def main():
    print(block_parser.parse('[A] [B]'))

if __name__ == '__main__':
    main()
