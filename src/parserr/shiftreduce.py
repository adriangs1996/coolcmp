class ShiftReduceParser:
    """
    Clase base para los parsers SLR(1), LALR(1) y LR(1).
    No se debe instanciar directamente, en vez de eso, todo parser
    cuyo funcionamiento se base en las acciones shift reduce deben heredar
    de esta clase e implementar el metodo build_parsing_table.    
    """
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
     
        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            try:         
                action, tag = self.action[state, lookahead]
            except KeyError:
                error = w.copy()
                error[cursor] = '@'
                raise SyntaxError(f'Unexpected Token {w[cursor].lex} in position {cursor}, {error} ')
            if action == self.SHIFT:
                cursor += 1
                stack.append(tag)

            elif action == self.REDUCE:
                head, body = tag  #Separar la cabecera de la produccion, tag devuelve la produciion si la accion es Rk
                for _ in range(len(body)): stack.pop() #Consumir todos los elementos de la pila que correspondan a la produccion
                output.append(tag)
                new_state = self.goto[stack[-1],head]
                stack.append(new_state)

            elif action == self.OK:
                output.append(tag)
                return output[::-1]

            else:
                raise Exception('La cadena no pertenece al lenguaje')