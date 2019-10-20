from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)

SIMPLE_PROGRAM = """
class A {
    def main(): SELF_TYPE {
print("Hello There")
};

    def a(n :int) : int {
     n
};
    def b (): int {
           let varj : int <- 10 in {varj};
           let varl : int in {
                               varh
                             };
           let varj :int, varu : string <- "Hello There" in {var};

           case varj of
                x : int => x + 10 ;
                x : string => "Hi  there" ;
                x : object => varj;
           esac;
           a(10)
};

};
"""

try:
    TOKS = LEXER(SIMPLE_PROGRAM)
    print(TOKS)
    parse = PARSER(TOKS)
    print(parse)
except Exception as e:
    print(e)
