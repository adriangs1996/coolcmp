from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)

SIMPLE_PROGRAM = """
class A{
    def main(): SELF_TYPE {
print('Hello There');
}

    def a(n :int) : int {
     n;
}
    def b (): int {
       a(10);
}

}

"""

TOKS = LEXER(SIMPLE_PROGRAM)
print(TOKS)
parse = PARSER(TOKS)
print(parse)
