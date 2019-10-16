#%%
from automatons.state import State
from lexer.regexgenerator import Regex
from lexer.tokens import Token
#%%
class Lexer:

    """
    El generador de lexer se basa en un conjunto de expresiones regulares. 
    Cada una de ellas está asociada a un tipo de token. 
    El lexer termina siendo un autómata finito determinista con ciertas peculiaridades:
    - Resulta de transformar el autómata unión entre todas las expresiones regulares del lenguaje, 
      y convertirlo a determinista.
    - Cada estado final almacena los tipos de tokens que se reconocen al alcanzarlo. 
      Se establece una prioridad entre ellos para poder desambiaguar.
    - Para tokenizar, la cadena de entrada viaja repetidas veces por el autómata.
    - Cada vez, se comienza por el estado inicial, pero se continúa a partir de la última sección de la 
      cadena que fue reconocida.
    - Cuando el autómata se "traba" durante el reconocimiento de una cadena, se reporta la ocurrencia de un token. 
      Su lexema está formado por la concatenación de los símbolos que fueron consumidos desde el inicio y hasta pasar 
      por el último estado final antes de trabarse. Su tipo de token es el de mayor relevancia entre los anotados en el 
      estado final.
    - Al finalizar de consumir toda la cadena, se reporta el token de fin de cadena.
    """
    def __init__(self, table, eof,ignore_white_space=False):
        self.eof = eof
        self.regexs = self._build_regexs(table, ignore_white_space)
        self.automaton = self._build_automaton()
        self.ignore_white_space = ignore_white_space

    def _build_regexs(self, table, ignore_white_space):
        regexs = []
        for n, (token_type, regex) in enumerate(table):

            regex = Regex(regex, ignore_white_space)

            start = State.from_nfa(regex.automaton)

            for state in start:
                if state.final:
                    state.tag = (n,token_type)
            regexs.append(start)
 
        return regexs

    def _build_automaton(self):
        start = State('start')

        for regex in self.regexs:
            start.add_epsilon_transition(regex)
        return start.to_deterministic()


    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        lex = ''
        suffix = ''

        for symbol in string:
            next_state = state.transitions.get(symbol,None)
            if next_state:
                suffix+= symbol
                state = next_state[0]
                if state.final:
                    lex+= suffix
                    suffix =''
                    final = state
            else:
                break

        return final, lex

    def _tokenize(self, text):
        while text:
            string = text.pop(0)
            final,lex = self._walk(string)
            if lex == '':
                print(text)
                raise SyntaxError(f'Invalid token in {text[0]}')
            if final:
                n = 2**64
                token_type = None
                for state in final.state:
                    try:
                        priority, tt = state.tag
                        if priority < n:
                            n = priority
                            token_type = tt
                    except TypeError:
                        pass      
                yield lex, token_type
                if string != lex:
                    text.insert(0,string[len(lex):])
            else:
                raise SyntaxError(f'Invalid token in {text}')

        yield '$', self.eof

    def __call__(self, text:str):
        if self.ignore_white_space:
            text = text.replace('\n',' ')
            text = text.split()
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]


