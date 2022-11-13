import sys
import os

#sys.path.append('C:\\Users\\adlla\\Documents\\GitHub\\exa869-mi-compiladores')
sys.path.append(os.path.abspath('.'))
# run with $ python .\analisador_sintatico\index.py

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




def validate_matrix(index_token):
  finsh = False
  ACR_IDE = AcronymsEnum.IDENTIFIER.value
  ACR_NUM = AcronymsEnum.NUMBER.value

  if(tokens[index_token][1] != ACR_IDE):
    print('Error: Identifier expected')
    return index_token

  acc = tokens[index_token][2]
  brackets_stack = []
  waiting_index = False

  while not finsh and index_token + 1 < len(tokens):
    [line, next_acronym, next_lexeme] = tokens[index_token + 1]
    no_bracket_left = len(brackets_stack) == 0
    if(next_lexeme == '['):
      acc += next_lexeme
      waiting_index = True
      brackets_stack.append(next_lexeme)

    elif(next_lexeme == ']'):
      if(no_bracket_left):
        finsh = True
        continue
      if(waiting_index): 
        print('Missing index in matrix on line ' + str(line + 1))
      acc += next_lexeme
      brackets_stack.pop()

    elif(next_acronym == ACR_IDE or next_acronym == ACR_NUM):
      if(no_bracket_left):
        finsh = True
        continue
      if(waiting_index): 
        waiting_index = False
      else: 
        print("Unexpected token '" + next_lexeme + "'")
      acc += str(next_lexeme)

    else:
      if(no_bracket_left):
        finsh = True
        continue
      if(waiting_index): 
        print("Unexpected token '" + next_lexeme + "'")
      acc += next_lexeme
    index_token += 1
  
  if(len(brackets_stack) > 0):
    if(waiting_index):
      print('Missing index in matrix ' + acc)
    print('Missing closing bracket in matrix ' + acc)
  
  print(acc)
  return index_token

def check_compound_type(index_token):
  pass

def check_identifier(index_token):
  pass

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
    else: 
      (index_token) = validate_matrix(index_token)

    
    index_token += 1

if __name__ == '__main__':
  run_sintatic()
