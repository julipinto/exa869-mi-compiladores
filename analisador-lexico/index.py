import os
import re
from enum import Enum

class AcronymsEnum(Enum):
  RESERVED_WORD = "PRE"
  IDENTIFIER = "IDE"
  NUMBER = "NRO"
  UNFORMED_NUMBER = "NMF"
  DELIMITER = "DEL"
  RELATIONAL_OPERATOR = "REL"
  LOGICAL_OPERATOR = "LOG"
  ARITHMETIC_OPERATOR = "ART"
  UNFORMED_CHAIN = "CMF"
  UNFORMED_COMMENT = "CoMF"
  INVALID_CHARACTER = "CIN"
  BLOCK_COMMENT = "COB"
  LINE_COMMENT = "COL"
  CHARACTER_CHAIN = "CCH"
  UNCLOSED_CHARACTER_CHAIN = "CCU"


tokens = []
helper_operador_logico = ('&', '|')
operadores_aritmeticos = ("+", "-", "*", "/", "++", "--")
operadores_relacionais = ("!=", "==", "<", ">", "<=", ">=", "=")
operadores_logicos = ("&&", "||", "!")
deliminadores = (";", ",", "(", ")", "[", "]", "{", "}", ".", " ", "\t")
reserved_regex = re.compile("(?:boolean|const|e(?:lse|xtends)|f(?:alse|unction)|i(?:nt|f)|pr(?:int|ocedure)|re(?:a[dl]|turn)|st(?:art|r(?:ing|uct))|t(?:hen|rue)|var|while)$")
simbolos_ascii = {i for i in range(32, 127) if i != 34}

def is_space(char):
  """ Returns true if the character is a space or tab"""
  return char == " " or char == "\t"

def is_delimiter(char):
  """ Returns true if the character is contained by the delimiter list"""
  return char in deliminadores

def is_relational_operator(char):
  """ Returns true if the character is contained by the relational operator list"""
  return char in operadores_relacionais

def is_logical_operator(char):
  """ Returns true if the character is contained by the logical operator list"""
  return char in operadores_logicos

def is_arithmetic_operator(char):
  """ Returns true if the character is contained by the arithmetic operator list"""
  return char in operadores_aritmeticos

def helper_logical_operator(char):
  """ Returns true if the character is contained by the logical operator helper list"""
  return char in helper_operador_logico

def confirm_operator(line, current_index, line_length, function):
  operator = line[current_index]
  compound_operator = False
  if current_index + 1 < line_length and function(line[current_index]+line[current_index+1]):
    current_index += 1
    operator += line[current_index]
    compound_operator = True
  return (operator, current_index, compound_operator)

def is_valid_string_symbol(caractere):
  """ Returns true if the character is a valid symbol for a string, between 32 and 127 ascii regardeless of the double quote, 34""" 
  return ord(caractere) in simbolos_ascii

def ignore_space(line, last_index):
  """With the line and the first index given, it returns the next index that is not a space"""
  line_length = len(line)
  while last_index < line_length:
    if(not is_space(line[last_index])):
      break
    last_index += 1
  return last_index

def find_string(line, first_index):
  """
    With the line and the first index given, it checks if the first character is a double quote,
    and then it returns the concatenated string if the dople quote is closed or it gets to the
    end of the line. If the double quote is not closed, it returns the acronym for an unclosed
    string.
  """
  acronym = AcronymsEnum.CHARACTER_CHAIN.value
  if line[first_index] != '"':
    raise Exception("Não há aspas nesse index")

  last_index = first_index
  line_length = len(line)
  string = ""

  while last_index < line_length:
    if(not is_valid_string_symbol(line[last_index]) and line[last_index] != '"'):
      acronym = AcronymsEnum.UNFORMED_CHAIN.value

    string += line[last_index]
    if last_index > first_index and line[last_index] == '"':
      break
    last_index += 1

  if string[-1] != '"':
      acronym = AcronymsEnum.UNCLOSED_CHARACTER_CHAIN.value
  return (acronym, string, last_index)

def find_number(line, first_index):
  """
    With the line and the first index given, it checks if the first character is a number,
    and then it returns the concatenated the following numbers and at the maximum one dot.
    """
  if not line[first_index].isnumeric():
    raise Exception("Não é um número")

  last_index = first_index
  line_length = len(line)
  count_dot = 0
  number = ""
  acronym = AcronymsEnum.NUMBER.value

  while last_index < line_length:
    current_number = line[last_index]
    if(current_number == '.'):
      if(count_dot == 0):
        count_dot = 1
        number += current_number
      else:
        break
    elif(current_number.isnumeric()):
      number += current_number
    elif(is_space(current_number)):
      break
    else:
      acronym = AcronymsEnum.UNFORMED_NUMBER.value

    last_index += 1

  if(count_dot == 1 and not number[-1].isnumeric()):
    acronym = AcronymsEnum.UNFORMED_NUMBER.value
    print("segundo")
  return (acronym, number, last_index)

def find_next(linha, index):
  """
    With the line and the first index given, it accumulates the following characters until it
    finds a delimiter, a space the end of the line.
  """
  final_string = index
  line_length = len(linha)
  string = ""

  while final_string < line_length:
    if final_string >= index and linha[final_string] in deliminadores:
      break
    string += linha[final_string]
    final_string += 1

  return (string, final_string)

def line_comment(line, index):
  if line[index] != '/' and line[index+1] != '/':
    raise Exception("Não é um comentário de linha")

  index_end = len(line)
  comment = line[index:index_end]

  return (comment, index_end)


"""
TODO
-- Implementar erro, bloco não fechou o comentário
"""

def find_end_block_comment(line, index_start):
  """given a line and the index of the start of the block comment, it accumulates the following 
   until it finds the end of the block comment or the end of the line"""
  line_length = len(line)
  index_end = index_start
  comment = ""

  current_block_length = len(block_comment)
  has_found = False

  while index_end < line_length:
    comment += line[index_end]

    if (len(comment) > 1 and
      comment[-2] == '*' and 
      comment[-1] == '/' and
      current_block_length + len(comment) >= 4):
      has_found = True
      break

    index_end += 1
  
  return (has_found, comment, index_end)

block_comment = ""
is_comment_block = False
index_block_comment = 0

""" TODO
-- comentar todas as funcoes [ainda falta algumas]
-- melhorar funcao de delimitador ?
-- refatorar [TA INDO]
"""
def handle_line(index_line, line):
  global block_comment, is_comment_block, index_block_comment
  line_length = len(line)
  index_character = 0

  while index_character < line_length:
    palavra = ""

    current_caracter = line[index_character]
    next_character = None
    if(index_character + 1 < line_length):
      next_character = line[index_character + 1]

    if is_comment_block: # reconhece comentário de bloco não finalizado
      (has_found_end, comment, index_character) = find_end_block_comment(line, index_character)
      is_comment_block = not has_found_end
      block_comment += comment

      if has_found_end:
        tokens.append((index_block_comment, AcronymsEnum.BLOCK_COMMENT.value, block_comment))
        reset_variable_comment()
        
    elif is_space(current_caracter): # reconhece espaco
      ...

    elif current_caracter == '/': # reconhece comentário de linha ou bloco
      if next_character == '/':
        (comment, index_character) = line_comment(line, index_character)
        tokens.append((index_line, AcronymsEnum.LINE_COMMENT.value, comment))

      elif next_character == '*':
        index_block_comment = index_line
        is_comment_block = True
        continue # Ele agora vai seguir para o primeiro if para encontrar todos os comentários
      else:
        tokens.append((index_line, AcronymsEnum.ARITHMETIC_OPERATOR.value, current_caracter))

    elif current_caracter == '"': # reconhece cadeia de caractere
      (acronym, palavra, index_character) = find_string(line, index_character)
      tokens.append((index_line, acronym, palavra))

    elif is_delimiter(current_caracter): # reconhece delimitador
      tokens.append((index_line, AcronymsEnum.DELIMITER.value, current_caracter))

    elif current_caracter.isnumeric(): # reconhece número com ou sem .
      (acronym, number, index_character) = find_number(line, index_character)
      tokens.append((index_line, acronym, number))

    elif current_caracter == '-': # reconhece - como operador aritmético ou representando um símbolo de número negativo
      palavra = current_caracter
      acronym = AcronymsEnum.ARITHMETIC_OPERATOR.value
      next_character = ignore_space(line, index_character+1)
      if next_character < line_length and line[next_character].isnumeric():
        (acronym, number, index_character) = find_number(line, next_character)
        palavra += number
      tokens.append((index_line, acronym, palavra))

    elif is_arithmetic_operator(current_caracter): # reconhece operador aritmético
      (palavra, index_character, compound_operator) = confirm_operator(line, index_character, line_length, is_arithmetic_operator)
      tokens.append((index_line, AcronymsEnum.ARITHMETIC_OPERATOR.value, palavra))

    elif(current_caracter == '!'): # reconhece exclamação como operador lógico ou relacional
      acronym = AcronymsEnum.LOGICAL_OPERATOR.value
      (palavra, index_character, compound_operator) = confirm_operator(line, index_character, line_length, is_relational_operator)
      if(compound_operator):
        acronym = AcronymsEnum.RELATIONAL_OPERATOR.value
      tokens.append((index_line, acronym, palavra))

    elif is_relational_operator(current_caracter): # reconhece operador relacional
      (palavra, index_character, compound_operator) = confirm_operator(line, index_character, line_length, is_relational_operator)
      tokens.append((index_line, AcronymsEnum.RELATIONAL_OPERATOR.value, palavra))
    
    elif helper_logical_operator(current_caracter): # reconhece operador lógico
      acronym = AcronymsEnum.LOGICAL_OPERATOR.value
      (palavra, index_character, compound_operator) = confirm_operator(line, index_character, line_length, is_logical_operator)
      if(not compound_operator):
        acronym = AcronymsEnum.INVALID_CHARACTER.value
      tokens.append((index_line, acronym, palavra))

    elif(is_valid_string_symbol(current_caracter)): # reconhece identificador
      (palavra, index_character) = find_next(line, index_character)
      acronym = AcronymsEnum.IDENTIFIER.value
      if reserved_regex.match(palavra):
        acronym = AcronymsEnum.RESERVED_WORD.value
      tokens.append((index_line, acronym, palavra))
      continue

    else: # Não foi possível identificar o token
      tokens.append((index_line, AcronymsEnum.INVALID_CHARACTER.value, current_caracter))

    index_character += 1 # next index

  return line

def remove_line_garbage(line):
  return line.strip()

def reset_variable_comment():
  global block_comment, is_comment_block
  is_comment_block = False
  block_comment = ""

def print_console_header(path_name):
  print("**********************************************")
  print("Analisando o arquivo: ", path_name)
  print("**********************************************")

def salvar_analise_arquivo(name_file, tokens):
  name_file = (os.path.splitext(name_file)[0]).replace('input', 'output')+'_saida.txt'
  arquivo = open(name_file, 'w+', encoding="utf-8")
  for token in tokens:
    str_token = str(token[0]) + " " + str(token[1]) + " " + str(token[2])
    arquivo.write(str_token+'\n')
  arquivo.close()

root = "./files/input"
directory_files = [
  root+'/'+file_name
  for file_name in os.listdir(root) if os.path.isfile(root+'/'+file_name)
] 

if __name__ == "__main__":
  for relative_path_name in directory_files:
    print_console_header(relative_path_name)
    reset_variable_comment()
    with open(relative_path_name, encoding = 'utf-8') as file:
      for index_line, line in enumerate(file):
        line = remove_line_garbage(line)
        handle_line(index_line, line)
      if is_comment_block:
        tokens.append((index_line, AcronymsEnum.UNFORMED_COMMENT.value , block_comment))
    salvar_analise_arquivo(relative_path_name, tokens)
    tokens = []