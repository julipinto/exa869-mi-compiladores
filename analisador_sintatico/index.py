import os
import sys

#sys.path.append('C:\\Users\\adlla\\Documents\\GitHub\\exa869-mi-compiladores')
sys.path.append(os.path.abspath('.'))
# run with $ python .\analisador_sintatico\index.py

from inspect import currentframe, getframeinfo

from analisador_lexico.index import AcronymsEnum, run_lexical

tokens = run_lexical()

############################################### ACRONYMS CONSTANTS ###############################################
ACR_CCA = AcronymsEnum.CHARACTER_CHAIN.value
ACR_IDE = AcronymsEnum.IDENTIFIER.value
ACR_NUM = AcronymsEnum.NUMBER.value
ACR_REL = AcronymsEnum.RELATIONAL_OPERATOR.value
ACR_LOG = AcronymsEnum.LOGICAL_OPERATOR.value
ACR_ART = AcronymsEnum.ARITHMETIC_OPERATOR.value

############################################### AUXILIAR FUNCTIONS ###############################################

def is_type(token):
  return token in ['int', 'real', 'boolean', 'string']

def is_logical(token):
  return token in ['&&', '||']

def is_boolean(token):
  return token in ['true', 'false']

def red_painting(word): 
  #painting a word in red on terminal
  return '\033[1;31m' + str(word) + '\033[0;0m'

def blue_painting(word): 
  #painting a word in blue on terminal
  return '\033[1;34m' + str(word) + '\033[0;0m'


def print_if_missing_expecting(expecting_stack):
  if(len(expecting_stack) > 0):
    expecting_stack.reverse()
    print('Error: missing tokens ' + str(expecting_stack))

def create_stack(arr):
  arr.reverse()
  return arr

IDE_PRODUCTIONS = ['IDE', 'MATRIX', 'COMPOUND_TYPE']

## PODE SER QUE TENHA QUE MELHORAR ISSO AQUI
# FUNÇÃO GENÉRICA QUE VALIDA ARGUMENTOS DE FUNÇÕES, EXEMPLO PRINT E READ
def validate_arg(valid_args_list, index_token, function_arg = False, end_ide = ')'):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]

  if(ACR_CCA in valid_args_list and acronym == ACR_CCA):
    return index_token, lexeme

  elif(ACR_NUM in valid_args_list and acronym == ACR_NUM):
    return index_token, lexeme

  elif('BOOLEAN' in valid_args_list and is_boolean(lexeme)):
    return index_token, lexeme

  elif(ACR_IDE in valid_args_list and acronym == ACR_IDE and function_arg):
    if(tokens[index_token+1][2] == '('):
      [index_token, lexeme] = validate_grammar_function_return(index_token)
      return index_token, lexeme
    elif(tokens[index_token+1][2] == ','):
      return index_token, lexeme

  # check if there is a production derivated from IDE
  if((set(IDE_PRODUCTIONS) & set(valid_args_list)) and acronym == ACR_IDE):
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]

    if('IDE' in valid_args_list and end_ide in [f"_{next_acronym}", next_lexeme]): return index_token, lexeme

    elif('COMPOUND_TYPE' in valid_args_list and next_lexeme == '.'): return validate_compound_type(index_token)

    elif('MATRIX' in valid_args_list and next_lexeme == '['): return validate_matrix(index_token)

    else:
      print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
      return index_token, lexeme
  else: 
    # DA ERRO AQUI
    #print('Error: Unexpected token ' + lexeme + ' on line ' + str(next_line + 1))
    pass

  return index_token, False

############################################### PRINT FUNCTIONS ###############################################

def validate_grammar_print(index_token):
  expecting = create_stack(['print', '(', '<printable>', ')', ';'])
  # delimiters = create_stack(['(', ')', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, _, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<printable>'):
      valid_args = [ACR_CCA, ACR_NUM]
      valid_args.extend(IDE_PRODUCTIONS)
      (index_token, accum) = validate_arg(valid_args, index_token)
      if(accum != False):
        expecting.pop()
        acc += accum
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect == lexeme):
      # if(delimiters[-1] == next_expect): delimiters.pop()
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc

############################################### READ ###############################################

def validate_grammar_read(index_token):
  expecting = create_stack(['read', '(', '<readeble>', ')', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, _, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<readeble>'):
      valid_args = IDE_PRODUCTIONS
      (index_token, accum) = validate_arg(valid_args , index_token)

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
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


############################################### MATRIX ###############################################

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
    
    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)

  return index_token, acc

############################################### COMPOUND TYPE ###############################################
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

  print(blue_painting(getframeinfo(currentframe()).lineno), acc)

  return index_token, acc

###############################################  ###############################################

# def is_sum_or_sub(index_token):
#   lexeme = tokens[index_token][2]
#   return lexeme == '+' or lexeme == '-'

def is_sum_or_sub_or_mult_or_div(lexeme):
  return lexeme in ('+', '-', '*', '/')

# def is_mult_or_div(index_token):
#   lexeme = tokens[index_token][2]
#   return lexeme == '*' or lexeme == '/'

def is_operable(index_token):
  acronym = tokens[index_token][1]
  return acronym == AcronymsEnum.IDENTIFIER.value or acronym == AcronymsEnum.NUMBER.value

###############################################  ###############################################
#TODO: validar as expressões
#TODO: validar o block
def validate_grammar_while(index_token):
  expecting = create_stack(['while', '(', '<exp>', ')', '<block>'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<exp>'):
      expecting.pop()
      acc += lexeme

    elif(next_expect == '<block>'):
      expecting.pop()
      acc += lexeme

    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc

###############################################  ###############################################
# TODO: else
def validate_grammar_if(index_token):
  expecting = create_stack(['if', '(', '<exp>', ')', 'then', '<block>'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<exp>'):
      expecting.pop()
      acc += lexeme

    elif(next_expect == '<block>'):
      (index_token, accum) = validate_grammar_block(index_token)
      if(accum != False):
        acc += accum
        expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc

############################################### VARIABLE DECLARATION ###############################################
#FIXME: permitir atribuir valores a variáveis (int a = 1, b = 2;)

def validate_grammar_variable_declaration(index_token):
  if(not is_type(tokens[index_token][2])):
    print('Error: Type expected')
    return index_token, tokens[index_token][2]

  acc = tokens[index_token][2] + ' '

  # May have more = , Ide <mayhavemore> | 
  index_token += 1
  expecting = create_stack(['IDE', '<may_have_more>', ';'])

  while(len(expecting) > 0 and index_token + 1 <= len(tokens)):
    [_, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]
    
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

    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)

  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  
  return index_token, acc

############################################### COMPOUND DECLARATION ###############################################
# TODO: Validar o <all_vars>

def validate_grammar_compound_declaration(index_token):
  expecting = create_stack(['struct', 'IDE', '{', '<all_vars>', '}', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<all_vars>' and index_token + 1 < len(tokens)):
      if(is_type(lexeme)):
        (index_token, accum) = validate_grammar_variable_declaration(index_token)
        acc += accum
        
        if(not (index_token + 1 < len(tokens) and is_type(tokens[index_token + 1][2]))):
          expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  
  return index_token, acc

############################################### EXTENDS ###############################################
# TODO: Validar o <all_vars>

def validate_grammar_extends(index_token):
  expecting = create_stack(['IDE', 'extends', 'IDE', '{', '<all_vars>', '}', ';'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<all_vars>' and index_token + 1 < len(tokens)):
      if(is_type(lexeme)):
        (index_token, accum) = validate_grammar_variable_declaration(index_token)
        acc += accum
        
        if(not (index_token + 1 < len(tokens) and is_type(tokens[index_token + 1][2]))):
          expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  
  return index_token, acc

############################################### GLOBAL VARIABLE ###############################################
def validate_grammar_global_variable_declaration(index_token):
  expecting = create_stack(['<init>', '{', '<all_vars>', '}'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<init>' and (lexeme == 'const' or lexeme == 'var')):
      expecting.pop()
      acc += lexeme

    elif(next_expect == '<all_vars>' and index_token + 1 < len(tokens)):
      if(is_type(lexeme)):
        (index_token, accum) = validate_grammar_variable_declaration(index_token)
        acc += accum
        
        if(not (index_token + 1 < len(tokens) and is_type(tokens[index_token + 1][2]))):
          expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    

    if(len(expecting) > 0):
      index_token += 1

  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  
  return index_token, acc


####################################### PROCEDURE DECLARATION  ###############################################
def validate_grammar_procedure_declaration(index_token):
  expecting = create_stack(['procedure', 'IDE', '(', '<list_params>', ')', '<block>'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<list_params>'):
      if(lexeme != ')'):
        (index_token, accum) = validate_parameters(index_token)
        if(accum != False):
          acc += accum
          expecting.pop()
        else:
          print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
          acc += red_painting(lexeme)
        # index_token -= 1
        # expecting.pop()
      else:
        expecting.pop()
        continue

    elif(next_expect == '<block>'):
      (index_token, accum) = validate_grammar_block(index_token)
      if(accum != False):
        acc += accum
        expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))

    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


########################################### FUNCTIONS RETURN #############################################

def validate_grammar_function_return(index_token):
  expecting = create_stack(['IDE', '(', '<optional_params>', ')'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<optional_params>'):
      if(lexeme != ')'):
        valid_args = [ACR_CCA, ACR_NUM]
        valid_args.extend(IDE_PRODUCTIONS)
        more_params = True
        params = create_stack(['<optional_params>'])
        while more_params and index_token < len(tokens)-1 and tokens[index_token][2] != ')':
          [line, acronym, lexeme] = tokens[index_token]
          
          if(len(params) == 0):
            if(lexeme == ')'):
              more_params = False
            else:
              params = create_stack([',', '<optional_params>'])
              continue
          else:
            next_expect = params[-1]
            if(next_expect == '<optional_params>'):
              (index_token, accum) = validate_arg(valid_args, index_token, function_arg = True)
              if(accum != False):
                acc += accum
              else:
                print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
                acc += red_painting(lexeme)
            elif(next_expect == lexeme):
              acc += lexeme
            else:
              print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
              acc += red_painting(lexeme)
            index_token += 1
            params.pop()
        index_token -= 1
        expecting.pop()
      else:
        expecting.pop()
        continue
      # if(lexeme != ')'):
        # valid_args = [ACR_CCA, ACR_NUM]
        # valid_args.extend(IDE_PRODUCTIONS)
      #   index_init_params = index_token

      #   while index_token < len(tokens)-1 and tokens[index_token][2] != ')':
      #     [line, acronym, lexeme] = tokens[index_token]
      #     if(index_token != index_init_params):
      #       if(lexeme == ',') and tokens[index_token+1][2] != ')':
      #         index_token += 1
      #         acc += ','
          # (index_token, accum) = validate_arg(valid_args, index_token, function_arg = True)
          # if(accum != False):
          #   acc += accum
          # else:
          #   print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
          #   acc += red_painting(lexeme)
      #     index_token += 1
      #   expecting.pop()
      #   index_token -= 1
      # else:
      #   expecting.pop()
      #   next_expect = expecting[-1]
      #   continue

    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))

    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc

def validate_arg_relational_expression(index_token, return_error = True):
  [_, acronym, lexeme] = tokens[index_token]

  if(acronym == ACR_CCA or acronym == ACR_NUM or acronym == is_boolean(lexeme)):
    return index_token, lexeme

  # else:
  #   if(index_token+1 < len(tokens)):
  #     (index, production) = validate_arg_relational_expression(index_token, return_error = False)
  #     # verifica se o acronym depois do argumento válido é um relacional
  #     # isso identifica a expressão como relacional
  #     if(index+1 < len(tokens) and tokens[index+1][1] == ACR_REL):
  #       (index_valid, production) = validate_grammar_relational_expression(index_token)
  #       # index_token = index_valid + 1 #TODO: corrigir index que está sendo necessário acrescimo
  #       return (index_valid, production)
  #   # if(return_error):
  #   #   print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
  #   if(acronym == ACR_IDE):
  #     if(index_token+1 < len(tokens) and tokens[index_token+1][2] == '('):
  #       [index_token, lexeme] = validate_grammar_function_return(index_token)
  #     return index_token, lexeme

  if(acronym == ACR_IDE):
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]

    if(next_acronym == ACR_REL): return index_token, lexeme

    elif(next_lexeme == '.'): return validate_compound_type(index_token)

    elif(next_lexeme == '['): return validate_matrix(index_token)

    else:
      if(return_error):
        print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
      return index_token, lexeme

  else:
    if(return_error):
      print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
    return index_token, lexeme

  # validar <RetornoFuncao> | '(' <ExpressaoRelacional> ')' | '(' <Expressao> ')' | '(' <ExpressaoLogica> ')


########################################### RELATIONAL EXPRESSIONS #############################################

def validate_grammar_relational_expression(index_token):
  expecting = create_stack(['<relational_value>', 'REL', '<relational_value>'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<relational_value>'):
      #valid_args = [ACR_CCA, ACR_NUM, ACR_IDE, 'MATRIX', 'COMPOUND_TYPE', 'BOOLEAN']
      #(index_token, accum) = validate_arg(valid_args, index_token, end_ide = '_REL')
      (index_token, accum) = validate_arg_relational_expression(index_token)
      if(accum != False):
        expecting.pop()
        acc += accum
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect in [acronym, lexeme]):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))

    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


def validate_arg_logical_expression(index_token, return_error = True):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]

  if(is_boolean(lexeme)):
    return index_token, lexeme
  else:
    if(index_token+1 < len(tokens)):
      (index, production) = validate_arg_relational_expression(index_token, return_error = False)
      # verifica se o acronym depois do argumento válido é um relacional
      # isso identifica a expressão como relacional
      if(index+1 < len(tokens) and tokens[index+1][1] == ACR_REL):
        (index_valid, production) = validate_grammar_relational_expression(index_token)
        # index_token = index_valid + 1 #TODO: corrigir index que está sendo necessário acrescimo
        return (index_valid, production)
    # if(return_error):
    #   print('Error: Unexpected token ' + next_lexeme + ' on line ' + str(next_line + 1))
    if(acronym == ACR_IDE):
      if(index_token+1 < len(tokens) and tokens[index_token+1][2] == '('):
        [index_token, lexeme] = validate_grammar_function_return(index_token)
      return index_token, lexeme

def validate_arg_arithmetic_expression(valid_args_list, index_token, return_error = True):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]
  has_parentheses = True

  if(not return_error):
    while(has_parentheses):
        if(lexeme == '('):
          index_token += 1
          [_, acronym, lexeme] = tokens[index_token]
        else:
          has_parentheses = False

  if(ACR_IDE in valid_args_list and acronym == ACR_IDE):
    return index_token, lexeme

  elif(ACR_NUM in valid_args_list and acronym == ACR_NUM):
    return index_token, lexeme
  return index_token, lexeme

########################################### LOGICAL EXPRESSIONS #############################################

def validate_grammar_logical_expression(index_token):
  expecting = create_stack(['<logical_value>', 'LOG', '<logical_value>'])
  acc = ""
  finsh = False

  while not finsh and index_token < len(tokens):
    [line, acronym, lexeme] = tokens[index_token]

    if(lexeme == '!'):
      index_token += 1
      [line, acronym, lexeme] = tokens[index_token]
      acc += '!'

    if(index_token + 1 >= len(tokens)):
      # print(expecting)
      finsh = True

    if(len(expecting) == 0 and not finsh):
      [line, next_acronym, next_lexeme] = tokens[index_token + 1]
      if(is_logical(next_lexeme)):
        expecting = create_stack(['<logical_value>'])
        acc += next_lexeme
        index_token += 1
      else:
        finsh = True
        # continue
    else:
      print(lexeme)
      if(len(expecting) > 0):
        next_expect = expecting[-1]

        if(next_expect == '<logical_value>'):
          (index_token, accum) = validate_arg_logical_expression(index_token)
          if(accum != False):
            expecting.pop()
            acc += accum
          else:
            print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
            acc += red_painting(lexeme)

        elif(next_expect in [acronym, lexeme] and is_logical(lexeme)):
          expecting.pop()
          acc += lexeme

        else:
          acc += red_painting(lexeme)
          print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))

    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


############################################# ARITHMETIC EXPRESSIONS #############################################

def validate_grammar_arithmetic_expression(index_token):
  expecting = create_stack(['<value>', 'ART', '<value>'])
  acc = ""
  parentheses = []
  has_parentheses = True
  finsh = False

  while not finsh and index_token < len(tokens):
    [line, acronym, lexeme] = tokens[index_token]

    # controle de parenteses na expressão
    while(has_parentheses):
      if(lexeme == '('):
        index_token += 1
        acc += '('
        parentheses.append(')')
        [line, acronym, lexeme] = tokens[index_token]
      else:
        has_parentheses = False

    if(len(expecting) == 0):
      has_parentheses = True
      # controle de parenteses na expressão
      while(index_token < len(tokens) and len(parentheses) > 0 and has_parentheses):
          if(tokens[index_token][2] == ')'):
            index_token += 1
            acc += ')'
            parentheses.pop()
          else:
            has_parentheses = False
      
      if(index_token + 1 < len(tokens) and tokens[index_token][1] == 'ART'):
        expecting = create_stack(['ART', '<value>'])
      else:
        finsh = True
        continue
    else:
      [line, acronym, lexeme] = tokens[index_token]
      next_expect = expecting[-1]

      if(next_expect == '<value>'):
        valid_args = [ACR_IDE, ACR_NUM]
        # valid_args.extend(IDE_PRODUCTIONS)
        (index_token, accum) = validate_arg_arithmetic_expression(valid_args, index_token)
        if(accum != False):
          expecting.pop()
          acc += accum
        else:
          print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
          acc += red_painting(lexeme)

      elif(next_expect == acronym and is_sum_or_sub_or_mult_or_div(lexeme)):
        expecting.pop()
        acc += lexeme

      elif(index_token-1 >= len(parentheses) and len(parentheses) > 0 and tokens[index_token][2] == ')' and (tokens[index_token-1][2] == ')' or tokens[index_token-1][1] in ['IDE', 'NRO'])):
        acc += ')'
        parentheses.pop()
        index_token += 1

      else:
        acc += red_painting(lexeme)
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))

      if(len(expecting) > 0):
        has_parentheses = True
        index_token += 1
      else:
        index_token += 1

  # # controle de parenteses na expressão
  # while(index_token < len(tokens) and len(parentheses) > 0):
  #   if(tokens[index_token][2] == ')'):
  #     index_token += 1
  #     acc += ')'
  #     parentheses.pop()
  #   else:
  #     print_if_missing_expecting(')')

  print_if_missing_expecting(parentheses)
  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


def validate_arg_function_content(index_token):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]

  if(lexeme == 'print'): 
    return validate_grammar_print(index_token)

  elif (lexeme == 'read'):
    return validate_grammar_read(index_token)

  elif (lexeme == 'while'):
    return validate_grammar_while(index_token)

  elif (lexeme == 'if'):
    return validate_grammar_if(index_token)

  elif (acronym == ACR_IDE): 
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(next_lexeme == '('):
      (index_token, production) = validate_grammar_function_return(index_token)
      index_token += 1
      if(tokens[index_token][2] == ';'):
        production += ';'
        return (index_token, production)


def validate_arg_function_return(index_token):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]
  if(acronym == ACR_NUM or acronym == ACR_CCA or acronym == ACR_IDE or is_boolean(lexeme)): 
    return (index_token, lexeme)
  return (index_token, lexeme)


def validate_parameters(index_token):
  more_params = True
  acc = ""
  params = create_stack(['<type>', 'IDE'])
  while more_params and index_token < len(tokens)-1 and tokens[index_token][2] != ')':
    [line, acronym, lexeme] = tokens[index_token]
    if(len(params) == 0):
      if(lexeme == ')'):
        more_params = False
      else:
        params = create_stack([',', '<type>', 'IDE'])
        continue
    else:
      next_expect = params[-1]
      if(next_expect == '<type>'):
        if(not is_type(lexeme)):
          print('Error: Type expected')
        else:
          acc += lexeme
      elif(next_expect in [lexeme, acronym]):
        acc += lexeme
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
      index_token += 1
      params.pop()
  index_token -= 1
  return (index_token, acc)

############################################### FUNCTIONS DECLARATION ###############################################

def validate_grammar_function_declaration(index_token):
  expecting = create_stack(['function', '<type>', 'IDE', '(', '<optional_params>', ')', '{', '<conteudo>', 'return', '<return>', ';', '}'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<optional_params>'):
      if(lexeme != ')'):
        (index_token, accum) = validate_parameters(index_token)
        if(accum != False):
          acc += accum
          expecting.pop()
        else:
          print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
          acc += red_painting(lexeme)
        # index_token -= 1
        # expecting.pop()
      else:
        expecting.pop()
        continue
    elif(next_expect == '<conteudo>'):
      (index_token, accum) = validate_content(index_token, validate_arg_function_content, 'return')
      if(accum != False):
        acc += accum
        expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
    elif(next_expect == '<return>'):
      (index_token, accum) = validate_arg_function_return(index_token)
      if(accum != False):
        expecting.pop()
        acc += accum
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
    elif(next_expect == [lexeme, acronym]):
      expecting.pop()
      acc += lexeme
    elif(next_expect == '<type>'):
      if(is_type(lexeme)):
        expecting.pop()
        acc += lexeme
      else:
        acc += red_painting(lexeme)
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc


def validate_arg_start_content(index_token):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]

  if(lexeme == 'print'): 
    return validate_grammar_print(index_token)

  elif (lexeme == 'read'):
    return validate_grammar_read(index_token)

  elif (lexeme == 'while'):
    return validate_grammar_while(index_token)

  elif (lexeme == 'if'):
    return validate_grammar_if(index_token)

  elif (acronym == ACR_IDE): 
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(next_lexeme == '('):
      (index_token, production) = validate_grammar_function_return(index_token)
      index_token += 1
      if(tokens[index_token][2] == ';'):
        production += ';'
        return (index_token, production)


############################################### START FUNCTION ###############################################

def validate_grammar_start_function(index_token):
  expecting = create_stack(['function', 'start', '(', ')', '{', '<content>', '}'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, acronym, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<content>'):
      (index_token, accum) = validate_content(index_token, validate_arg_start_content, '}')
      if(accum != False):
        acc += accum
        expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)
    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme
    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1

  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc



def validate_arg_block_content(index_token):
  # By indicating a list of acceptable tokens, this function will validate if the next token is in the list
  [_, acronym, lexeme] = tokens[index_token]

  if(lexeme == 'print'): 
    return validate_grammar_print(index_token)

  elif (lexeme == 'read'):
    return validate_grammar_read(index_token)

  elif (lexeme == 'while'):
    return validate_grammar_while(index_token)

  elif (lexeme == 'if'):
    return validate_grammar_if(index_token)

  elif (acronym == ACR_IDE): 
    [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]
    if(next_lexeme == '('):
      (index_token, production) = validate_grammar_function_return(index_token)
      index_token += 1
      if(tokens[index_token][2] == ';'):
        production += ';'
        return (index_token, production)


def validate_content(index_token, validate_function, delimiter):
  [line, _, lexeme] = tokens[index_token]
  more_content = True
  acc = ""
  while(more_content):
    (index_token, accum) = validate_function(index_token)
    if(accum != False):
      acc += accum
    else:
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
      acc += red_painting(lexeme)
    if(tokens[index_token+1][2] == delimiter):
      more_content = False
    else:
      index_token += 1
  return (index_token, acc)


############################################### BLOCK ###############################################

def validate_grammar_block(index_token):
  expecting = create_stack(['{', '<content>', '}'])
  acc = ""

  while index_token < len(tokens) and len(expecting) > 0:
    [line, _, lexeme] = tokens[index_token]
    next_expect = expecting[-1]

    if(next_expect == '<content>'):
      (index_token, accum) = validate_content(index_token, validate_arg_block_content, '}')
      if(accum != False):
        acc += accum
        expecting.pop()
      else:
        print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
        acc += red_painting(lexeme)

    elif(next_expect == lexeme):
      expecting.pop()
      acc += lexeme

    else:
      acc += red_painting(lexeme)
      print('Error: Unexpected token ' + lexeme + ' on line ' + str(line + 1))
    
    if(len(expecting) > 0):
      index_token += 1


  print_if_missing_expecting(expecting)
  
  print(blue_painting(getframeinfo(currentframe()).lineno), acc)
  return index_token, acc

############################################### MAIN ###############################################

def run_sintatic():
  index_token = 0
  len_tokens = len(tokens)

  while index_token < len_tokens:
    [line, acronym, lexeme] = tokens[index_token]

    if(lexeme == 'print'): 
      (index_token, production) = validate_grammar_print(index_token)

    elif (lexeme == 'read'):
      (index_token, production) = validate_grammar_read(index_token)

    elif (lexeme == 'while'):
      (index_token, production) = validate_grammar_while(index_token)

    elif (lexeme == 'if'):
      (index_token, production) = validate_grammar_if(index_token)
    
    elif (lexeme == 'struct'):
      (index_token, production) = validate_grammar_compound_declaration(index_token)

    elif (lexeme == 'function'):
      if(tokens[index_token+1][2] == 'start'):
        (index_token, production) = validate_grammar_start_function(index_token)
      else:
        (index_token, production) = validate_grammar_function_declaration(index_token)

    elif(lexeme == 'procedure'):
      (index_token, production) = validate_grammar_procedure_declaration(index_token)

    elif(lexeme == 'const' or lexeme == 'var'):
      (index_token, production) = validate_grammar_global_variable_declaration(index_token)

    elif(lexeme == '{'): #TODO: elif apenas para testar bloco
      (index_token, production) = validate_grammar_block(index_token)
    elif(is_type(lexeme)):
      (index_token, production) = validate_grammar_variable_declaration(index_token)
    elif (acronym == ACR_IDE and tokens[index_token + 1][2] == '('): 
      (index_token, production) = validate_grammar_function_return(index_token)
    # este else analisa as produções não identificadas anteriormente e que provavelmente são
    # alguma das expressões (relacional, aritmetica ou lógica)
    else:
      # boolean para controle de verificações a fim de evitar verificações desnecessárias
      is_expression = False

      # tenta identificar se o argumento antes do acronym é valido na expressão relacional
      (index, production) = validate_arg_relational_expression(index_token, return_error = False)
      # verifica se o acronym depois do argumento válido é um relacional
      # isso identifica a expressão como relacional
      if(index+1 < len(tokens) and tokens[index+1][1] == ACR_REL):
        (index_valid, production) = validate_grammar_relational_expression(index_token)
        is_expression = True
        index_token = index_valid + 1 #TODO: corrigir index que está sendo necessário acrescimo
      
      if(not is_expression):
        # tenta identificar se o argumento antes do acronym é valido na expressão lógica
        (index, production) = validate_arg_logical_expression(index_token, return_error = False)
        # verifica se o acronym depois do argumento válido é um lógico
        # isso identifica a expressão como relacional
        if(index+1 < len(tokens) and tokens[index+1][1] == ACR_LOG):
          (index_valid, production) = validate_grammar_logical_expression(index_token)
          is_expression = True
          index_token = index_valid

      if(not is_expression):
        # tenta identificar se o argumento antes do acronym é valido na expressão lógica
        (index, production) = validate_arg_arithmetic_expression([ACR_IDE, ACR_NUM], index_token, return_error = False)
        # verifica se o acronym depois do argumento válido é um lógico
        # isso identifica a expressão como relacional
        if(index+1 < len(tokens) and tokens[index+1][1] == ACR_ART):
          (index_valid, production) = validate_grammar_arithmetic_expression(index_token)
          is_expression = True
          index_token = index_valid

    # elif (acronym == ACR_IDE): 
    #   [next_line, next_acronym, next_lexeme] = tokens[index_token + 1]

    #   if(next_lexeme == '['):
    #     (index_token, production) = validate_matrix(index_token)
    #   elif(next_lexeme == '.'):
    #     (index_token, production) = validate_compound_type(index_token)
      # elif(next_lexeme == '('):
      #   (index_token, production) = validate_grammar_function_return(index_token)
    #   elif(next_lexeme == 'extends'):
    #     (index_token, production) = validate_grammar_extends(index_token)

    index_token += 1

if __name__ == '__main__':
  run_sintatic()
