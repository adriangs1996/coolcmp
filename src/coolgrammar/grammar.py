from grammar.grammar import Grammar,Terminal,NonTerminal,AttributeProduction
from abstract.tree import *
from lexer.tokenizer import Lexer
from lexer.regexgenerator import Regex
from abstract.semantics import Type, IntegerType, VoidType, ObjectType, BoolType, StringType, AutoType

def build_cool_grammar():
    G = Grammar()
    program = G.NonTerminal('<program>',True)
    class_list, class_def, empty_feature_list, feature_list, meod_def = G.NonTerminals('<class_list> <class_def> <empty_feature_list> <feature_list> <meod_def>')
    attr_def, param_list, param, statement_list = G.NonTerminals('<attr_def> <param_list> <param> <statement_list>')
    statement, var_dec, func_call, args_list = G.NonTerminals('<statement> <var_dec> <func_call> <args_list>')
    exp, typex, term, factor = G.NonTerminals('<exp> <type> <term> <factor>')
    arith, atom = G.NonTerminals('<arith> <atom>')
    args_list_empty, param_list_empty = G.NonTerminals('<args_list_empty> <param_list_empty>')

    class_keyword, def_keyword, in_keyword = G.Terminals('class def in')
    coma, period, dot_comma, opar, cpar, obrack, cbrack, plus, minus, star, div, dd = G.Terminals(', . ; ( ) { } + - * / :')
    idx, let, intx,string, num, equal, true, false,boolean, objectx = G.Terminals('id let int string num = true false bool object')
    string_const, void, auto = G.Terminals('string_const void AUTO_TYPE')
    if_, then, else_,assign, new = G.Terminals('if then else assign new')
    gt, lt , ge, le, eq, not_ = G.Terminals('> < >= <= == !')
    while_, do = G.Terminals('while do')

    program %= class_list, lambda s: ProgramNode(s[1])

    class_list %= class_def, lambda s: [s[1]]
    class_list %= class_def + class_list, lambda s: [s[1]] + s[2]

    class_def %= class_keyword + idx + obrack + feature_list + cbrack, lambda s: ClassDef(s[2],s[4])
    class_def %= class_keyword + idx + dd + typex + obrack + feature_list + cbrack, lambda s: ClassDef(s[2],s[6],s[4])

    feature_list %= meod_def, lambda s: [s[1]]
    feature_list %= attr_def, lambda s: [s[1]]
    feature_list %= meod_def + feature_list, lambda s: [s[1]] + s[2]
    feature_list %= attr_def + feature_list, lambda s: [s[1]] + s[2] 
    
    meod_def %= def_keyword + idx + opar + param_list_empty + cpar + dd + typex + obrack + statement_list + cbrack, lambda s: MethodDef(s[2],s[4],s[7],s[9])
    
    attr_def %= idx + dd + typex + dot_comma, lambda s: AttributeDef(s[1],s[3])
    attr_def %= idx + dd + typex + equal + exp + dot_comma, lambda s: AttributeDef(s[1],s[3],s[5])
    
    param_list_empty %= param_list, lambda s: s[1]
    param_list_empty %= G.Epsilon, lambda s: []
    param_list %= param, lambda s: [s[1]]
    param_list %= param + coma + param_list, lambda s: [s[1]] + s[3]
    
    param %= idx + dd + typex, lambda s: Param(s[1],s[3])
    
    statement_list %= exp + dot_comma, lambda s: [s[1]]
    statement_list %= exp + dot_comma + statement_list, lambda s: [s[1]] + s[3]
    
    # var_dec %= let + idx + dd + typex + equal + exp, lambda s: VariableDeclaration(s[2],s[4],s[6])
    var_dec %= let + idx + dd + typex + assign + exp + in_keyword + obrack + statement_list + cbrack, lambda s: VariableDeclaration(s[2], s[4], s[6],s[9])
    
    exp %= arith, lambda s: s[1]
    arith %= arith + plus + term, lambda s: PlusNode(s[1],s[3])
    arith %= arith + minus + term, lambda s: DifNode(s[1],s[3])
    arith %= term, lambda s: s[1]
    term %= term + star + factor, lambda s: MulNode(s[1],s[3])
    term %= term + div + factor, lambda s: DivNode(s[1],s[3])
    term %= factor, lambda s: s[1]
    factor %= opar + arith + cpar, lambda s: s[2]
    factor %= num, lambda s: IntegerConstant(s[1])
    factor %= idx, lambda s: VariableCall(s[1])
    factor %= idx + period + idx + opar + args_list_empty + cpar, lambda s: FunCall(s[1],s[3],s[5])
    factor %= idx + opar + args_list_empty + cpar, lambda s: FunCall('self',s[1],s[3])
    exp %= var_dec, lambda s: s[1]
    exp %= true, lambda s: TrueConstant()
    exp %= false, lambda s: FalseConstant()
    exp %= string_const, lambda s: StringConstant(s[1])
    exp %= if_ + opar + exp + cpar + then + obrack + exp + cbrack + else_ + obrack + exp + cbrack, lambda s: IfThenElseNode(s[3],s[7],s[11])
    exp %= idx + assign + exp, lambda s: AssignNode(s[1],s[3])
    exp %= atom, lambda s: s[1]
    exp %= new + idx + opar + args_list_empty + cpar, lambda s: InstantiateClassNode(s[2], s[4])
    atom %= factor + gt + factor, lambda s: GreaterThanNode(s[1],s[3])
    atom %= factor + lt + factor, lambda s: LowerThanNode(s[1], s[3])
    atom %= factor + eq + factor, lambda s: EqualToNode(s[1], s[3])
    atom %= factor + ge + factor, lambda s: GreaterEqualNode(s[1], s[3])
    atom %= factor + le + factor, lambda s: LowerEqual(s[1], s[3])
    atom %= not_ + factor, lambda s: NotNode(s[2])
    
    exp %= while_ + opar + exp + cpar + do + obrack + statement_list + cbrack, lambda s: WhileBlockNode(s[3],s[7])

    typex %= intx, lambda s: 'int'
    typex %= boolean, lambda s: 'bool'
    typex %= string, lambda s: 'string'
    typex %= objectx, lambda s: 'object'
    typex %= idx, lambda s: s[1]
    typex %= auto, lambda s: 'AUTO_TYPE'
    typex %= void, lambda s: 'void'
    
    args_list_empty %= args_list, lambda s: s[1]
    args_list_empty %= G.Epsilon, lambda s: []
    args_list %= exp, lambda s : [s[1]]
    args_list %= exp + coma + args_list, lambda s: [s[1]] + s[3]
    
    table = [(class_keyword,'class'),
              (def_keyword,'def'),
              (in_keyword,'in'),
              (intx,'int'),
              (boolean,'bool'),
              (objectx,'object'),
              (string,'string'),
              (true,'true'),
              (false,'false'),
              (auto,'AUTO_TYPE'),
              (if_,'if'),
              (then,'then'),
              (else_,'else'),
              (new,'new'),
              (while_, 'while'),
              (do, 'do'),
              (coma,','),
              (period,'.'),
              (dd,':'),
              (dot_comma,';'),
              (assign,'<@-'),
              (lt,'@<'),
              (gt, '@>'),
              (ge,'>='),
              (le, '<='),
              (eq, '=='),
              (not_, '@!'),
              (equal, '='),
              (opar, '@('),
              (cpar, '@)'),
              (obrack, '@{'),
              (cbrack, '@}'),
              (plus, '@+'),
              (minus, '@-'),
              (div, '/'),
              (star, '@*'),
              (let, 'let'),
              (idx, '(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z)+'),
              (num, '0|(1|2|3|4|5|6|7|8|9)(1|2|3|4|5|6|7|8|9|0)*'),
              (string_const, "@'(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z)+@'")
              ]

    lexer = Lexer(table, G.EOF, ignore_white_space=False)
    return G, lexer


