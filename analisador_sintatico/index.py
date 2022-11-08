import sys

sys.path.append('C:\\Users\\adlla\\Documents\\GitHub\\exa869-mi-compiladores')

from analisador_lexico.index import AcronymsEnum, run_lexical

# import ./analisador_lexico/index.py
#from index import run_lexical

tokens = run_lexical()

def is_type(token):
  return token == 'int' | token == 'real' | token == 'boolean' | token == 'string'

def is_printable(acronym, lexeme):
  return acronym == AcronymsEnum.IDENTIFIER.value or acronym == AcronymsEnum.CHARACTER_CHAIN.value

def is_read(acronym):
  return acronym == AcronymsEnum.IDENTIFIER.value

def validate_grammar_print(index_init):
  is_print = tokens[index_init][2] == 'print'
  is_open = tokens[index_init + 1][2] == '('

  ## MODIFICAR O PRINTÁVEL PARA ACEITAR MAIS DE UM TOKEN EX.: MATRIZ
  [_,content_acronym, content_lexeme] = tokens[index_init + 2]
  is_print = is_printable(content_acronym, content_lexeme)

  is_close = tokens[index_init + 3][2] == ')'

  ## O 3 É ARBITRÁRIO, MODIFICAR COM O CONTEÚDO DO PRINT
  return is_print and is_open and is_print and is_close, index_init + 3

'''
  Valida a gramática do READ.
'''
def validate_grammar_read(index_init):
  correct_grammar = False
  if(tokens[index_init][2] == 'read'):
    index_init = index_init + 1
    if(tokens[index_init][2] == '('):
      index_init = index_init + 1
      if(is_read(tokens[index_init][1])):
        index_init = index_init + 1
        if(tokens[index_init][2] == ')'):
          index_init = index_init + 1
          if(tokens[index_init][2] == ';'):
            index_init = index_init + 1
            correct_grammar = True
  return correct_grammar, index_init

def run_sintatic():
  index_token = 0
  len_tokens = len(tokens)

  while index_token < len_tokens:
    [line, acronym, lexeme] = tokens[index_token]

    if(lexeme == 'print'): 
      (is_valid_print, index_token) = validate_grammar_print(index_token)
      if(is_valid_print):
        print('Print is valid')
      else:
        print('Print is invalid')
        break
    elif (lexeme == 'read'):
      (is_valid_read, index_token) = validate_grammar_read(index_token)
      if(is_valid_read):
        print('Read is valid')
      else:
        print('Read is invalid')
        break
    index_token += 1

if __name__ == '__main__':
    run_sintatic()
