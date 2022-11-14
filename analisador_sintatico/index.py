import sys
import os

#sys.path.append('C:\\Users\\adlla\\Documents\\GitHub\\exa869-mi-compiladores')
sys.path.append(os.path.abspath('.'))
# run with $ python .\analisador_sintatico\index.py

from analisador_lexico.index import AcronymsEnum, run_lexical
ACR_CCA = AcronymsEnum.CHARACTER_CHAIN.value
ACR_IDE = AcronymsEnum.IDENTIFIER.value
ACR_NUM = AcronymsEnum.NUMBER.value

tokens = run_lexical()

def is_type(token):
  return token in ['int', 'real', 'boolean', 'string']

def validate_printable(index_token):
  [line, acronym, lexeme] = tokens[index_token]

  if(acronym == ACR_CCA or acronym == ACR_NUM):
    return index_token, lexeme

  if(acronym == ACR_IDE):
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(next_lexeme == ')'):
      return index_token, lexeme
    elif(next_lexeme == '.'):
      return validate_compound_type(index_token)
    elif(next_lexeme == '['):
      return validate_matrix(index_token)
    else:
      print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
      return index_token, lexeme

  return index_token, False

def is_read(acronym):
  return acronym == AcronymsEnum.IDENTIFIER.value

def red_painting(word): 
  return '\033[1;31m' + word + '\033[0;0m'

def validate_grammar_print(index_token):
  expecting = create_stack(['print', '(', '<printable>', ')', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, _, lexeme] = tokens[index_token]
    next_expect = expecting[-1]
    if(next_expect == '<printable>'):
      (index_token, accum) = validate_printable(index_token)
      if(accum != False):
        expecting.pop()
        acc += accum
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme
    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    index_token += 1


  if(len(expecting) > 0):
    expecting.reverse()
    print('Error: missing tokens ' + str(expecting))
  
  print(acc)
  return index_token, acc

'''
  Valida a gramática do READ.
'''
# def validate_grammar_read(index_init):
#   correct_grammar = False
#   if(tokens[index_init][2] == 'read'):
#     index_init = index_init + 1
#     if(tokens[index_init][2] == '('):
#       index_init = index_init + 1
#       if(is_read(tokens[index_init][1])):
#         index_init = index_init + 1
#         if(tokens[index_init][2] == ')'):
#           index_init = index_init + 1
#           if(tokens[index_init][2] == ';'):
#             index_init = index_init + 1
#             correct_grammar = True
#   return correct_grammar, index_init

def validate_readeble(index_token):
  [line, acronym, lexeme] = tokens[index_token]

  if(acronym == ACR_IDE):
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(next_lexeme == ')'):
      return index_token, lexeme
    elif(next_lexeme == '.'):
      return validate_compound_type(index_token)
    elif(next_lexeme == '['):
      return validate_matrix(index_token)
    else:
      print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
      return index_token, lexeme

  return index_token, False

def validate_grammar_read(index_token):
  expecting = create_stack(['read', '(', '<readeble>', ')', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, _, lexeme] = tokens[index_token]
    next_expect = expecting[-1]
    if(next_expect == '<readeble>'):
      (index_token, accum) = validate_readeble(index_token)
      if(accum != False):
        expecting.pop()
        acc += accum
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme
    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    index_token += 1


  if(len(expecting) > 0):
    expecting.reverse()
    print('Error: missing tokens ' + str(expecting))
  
  print(acc)
  return index_token, acc




# def validate_matrix(index_token):
#   finsh = False

#   if(tokens[index_token][1] != ACR_IDE):
#     print('Error: Identifier expected')
#     return index_token

#   acc = tokens[index_token][2]
#   brackets_stack = []
#   waiting_index = False

#   while not finsh and index_token + 1 < len(tokens):
#     [line, next_acronym, next_lexeme] = tokens[index_token + 1]
#     no_bracket_left = len(brackets_stack) == 0
#     if(next_lexeme == '['):
#       waiting_index = True
#       brackets_stack.append(next_lexeme)

#     elif(next_lexeme == ']'):
#       if(no_bracket_left):
#         finsh = True
#         continue
#       if(waiting_index): 
#         print('Missing index in matrix on line ' + str(line + 1))
#       brackets_stack.pop()

#     elif(next_acronym == ACR_IDE or next_acronym == ACR_NUM):
#       if(no_bracket_left):
#         finsh = True
#         continue
#       if(waiting_index): 
#         waiting_index = False
#       else: 
#         print("Unexpected token '" + next_lexeme + "'")

#     else:
#       if(no_bracket_left):
#         finsh = True
#         continue
#       if(waiting_index): 
#         print("Unexpected token '" + next_lexeme + "'")
#     acc += next_lexeme
#     index_token += 1
  
#   if(len(brackets_stack) > 0):
#     if(waiting_index):
#       print('Missing index in matrix ' + acc)
#     print('Missing closing bracket in matrix ' + acc)
  
#   return index_token, acc

def validate_matrix(index_token):
  finsh = False

  if(tokens[index_token][1] != ACR_IDE):
    print('Error: Identifier expected')
    return index_token
  acc = tokens[index_token][2]
  
  expecting = create_stack(['[', '<index>', ']'])

  while not finsh and index_token + 1 < len(tokens):
    [line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(len(expecting) == 0):
      if(next_lexeme == '['):
        expecting = create_stack(['<index>', ']'])
        acc += next_lexeme
      else:
        finsh = True
        continue
    else: 
      next_expect = expecting[-1]
      if(next_expect == '<index>'):
        if(next_acronym == ACR_IDE or next_acronym == ACR_NUM):
          expecting.pop()
          acc += next_lexeme
        else:
          print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(line + 1))
          acc += red_painting(next_lexeme)
      elif(next_lexeme == next_expect):
        expecting.pop()
        acc += next_lexeme
      else:
        print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(line + 1))
        acc += red_painting(next_lexeme)
    
    index_token += 1
  
  return index_token, acc

def validate_compound_type(index_token): 
  finsh = False
  ACR_IDE = AcronymsEnum.IDENTIFIER.value

  if(tokens[index_token][1] != ACR_IDE):
    print('Error: Identifier expected')
    return index_token
  
  acc = tokens[index_token][2]
  while not finsh and index_token + 1 < len(tokens):
    [line0, acronym0, lexeme0] = tokens[index_token + 1]

    if(lexeme0 != '.'):
      finsh = True
      continue

    acc += lexeme0

    # End of line before get the identifier
    if(index_token + 2 >= len(tokens)):
      index_token += 1
      print('Error: Identifier expected at line ' + str(line0 + 1))
      continue

    [line1, acronym1, lexeme1] = tokens[index_token + 2]

    if(lexeme1 == '.'):
      print('Identifier is missing at line ' + str(line1 + 1))
      index_token += 1
      continue    

    if(acronym1 != ACR_IDE):
      print('Unexpected token ' + lexeme1 + ' at line ' + str(line1 + 1))
      index_token += 1

    acc += lexeme1
    index_token += 2

  return index_token, acc

def is_sum_or_sub(index_token):
  [_, _, lexeme] = tokens[index_token]
  return lexeme == '+' or lexeme == '-'

def is_mult_or_div(index_token):
  [_, _, lexeme] = tokens[index_token]
  return lexeme == '*' or lexeme == '/'

def is_operable(index_token):
  [_, acronym, _] = tokens[index_token]
  return acronym == AcronymsEnum.IDENTIFIER.value or acronym == AcronymsEnum.NUMBER.value

def validate_grammar_while(index_token):
  pass

def validate_grammar_if(index_token):
  pass

def create_stack(arr):
  arr.reverse()
  return arr

def validate_grammar_variable_declaration(index_token):
  if(not is_type(tokens[index_token][2])):
    print('Error: Type expected')
    return index_token
  acc = tokens[index_token][2] + ' '

  index_token += 1
  expecting = create_stack(['IDE', '<may_have_more>', ';'])

  while(len(expecting) > 0 and index_token + 1 <= len(tokens)):
    next_expect = expecting[-1]
    [_, acronym, lexeme] = tokens[index_token]

    if(next_expect == '<may_have_more>'):
      if(lexeme == ','):
        expecting = create_stack(['IDE', '<may_have_more>', ';'])
        acc += lexeme + ' '
      else:
        expecting.pop()
        continue
    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme + ' '
    else:
      print('Error: Unexpected token ' + lexeme)
      acc += red_painting(lexeme) + ' '

    index_token += 1
    
  if(len(expecting) > 0):
    print('Error: Missing ' + expecting[-1])

  return index_token, acc

def run_sintatic():
  index_token = 0
  len_tokens = len(tokens)

  while index_token < len_tokens:
    [line, acronym, lexeme] = tokens[index_token]

    if(lexeme == 'print'): 
      (index_token, word) = validate_grammar_print(index_token)

    elif (lexeme == 'read'):
      (index_token, word) = validate_grammar_read(index_token)

    elif (lexeme == 'while'):
      (index_token, word) = validate_grammar_while(index_token)

    elif (lexeme == 'if'):
      (index_token, word) = validate_grammar_if(index_token)
    
    elif (lexeme == 'struct'):
      pass

    elif(is_type(lexeme)):
      (index_token, word) = validate_grammar_variable_declaration(index_token)

    elif (acronym == ACR_IDE): 
      [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]

      if(next_lexeme == '['):
        (index_token, word) = validate_matrix(index_token)
      elif(next_lexeme == '.'):
        (index_token, word) = validate_compound_type(index_token)
      elif(next_lexeme == '('):
        #chamada de função
        pass
      elif(next_lexeme == 'extends'):
        #extensão de classe
        pass

    
    index_token += 1

if __name__ == '__main__':
  run_sintatic()
