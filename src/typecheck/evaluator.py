import grammar.grammar as gr

def evaluate_right_parse(parse: [], tokens):
    
    def evaluate_production(productions, production: gr.AttributeProduction, tokens):
        synteticed = [None] * (len(production.Right) + 1)
        rules = production.attributes
                
        for i,symbol in enumerate(production.Right[::-1],1):
            if symbol.IsTerminal:
                synteticed[len(synteticed) - i] = next(tokens).lex
            else:
                synteticed[len(synteticed) - i] = evaluate_production(productions, next(productions), tokens)
        
        rule = rules[0]
        return rule(synteticed) if rule else None
    
    parse = iter(parse)
    tokens = iter(tokens[::-1])
    
    return evaluate_production(parse, next(parse),tokens)