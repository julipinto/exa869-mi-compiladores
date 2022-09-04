from asyncio.windows_events import NULL
from logging.config import IDENTIFIER
import os
import re
from enum import Enum

"""
os da professora: 
PRE palavra reservada
IDE identificador
NRO numero
DEL delimitador 
REL operador relacional
LOG operador logico
ART operador aritmetico
CMF cadeia mal formada
CoMF comentário mal formado
CIN	caracter inválido

os da gente: 
COB comentário de bloco
COL comentário de linha
"""

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
  return char == " " or char == "\t"

def is_delimiter(char):
  # return char in ["(", ")", ";", ",", "=", ":", ".", ">", "<", "!", "&", "|", "~", "^", "*", "-", "+", " ", "\t"]
  return char in deliminadores

def is_relational_operator(char):
  return char in operadores_relacionais

def is_logical_operator(char):
  return char in operadores_logicos

def is_arithmetic_operator(char):
  return char in operadores_aritmeticos

def helper_logical_operator(char):
  return char in helper_operador_logico

def is_valid_string_symbol(caractere):
  return ord(caractere) in simbolos_ascii

def ignore_space(line, last_index):
  line_length = len(line)
  while last_index < line_length:
    if(not is_space(line[last_index])):
      break
    last_index += 1
  return last_index

def find_string(line, first_index):
  """
    Dado uma linha e um index, ele verifica se a linha nesse index
    são aspas, e a partir daí ele vai concatenando os caracteres
    até encontrar o fechamento das aspas.
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
      # raise Exception("Caractere inválido:", line[last_index])
    string += line[last_index]
    if last_index > first_index and line[last_index] == '"':
      break
    last_index += 1

  if string[-1] != '"':
      acronym = AcronymsEnum.UNCLOSED_CHARACTER_CHAIN.value
    #NESSE PONTO ELE ACHOU UMA STRING QUE NÃO FECHOU AS ASPAS
    # raise Exception("String não fechou aspas")

  return (acronym, string, last_index)

def find_number(line, first_index):
  last_index = first_index
  line_length = len(line)
  count_dot = 0
  number = ""
  acronym = AcronymsEnum.NUMBER.value

  while last_index < line_length:
    if(line[last_index] == '.'):
      if(count_dot == 0):
        count_dot = 1
        number += line[last_index]
      else:
        break
    elif(line[last_index].isnumeric()):
      number += line[last_index]
    else:
      acronym = AcronymsEnum.UNFORMED_NUMBER.value
      break
    last_index += 1

  if(count_dot == 1 and not number[-1].isnumeric()):
    acronym = AcronymsEnum.UNFORMED_NUMBER.value
  return (acronym, number, last_index)

"""
Essa função vai achar o próximo conjunto de caracteres
"""
def find_next(linha, index):
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
-- Corrigir comentário de bloco fechando ao encontrar /*/ [CORRIGIDO AGORA TEM QUE TESTAR]
-- Implementar erro, bloco não fechou o comentário
"""

def find_end_block_comment(line, index_start):
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

""" TODO
-- verificar operadores logicos
-- comentar todas as funcoes
-- padronizar identificacao
-- salvar identificao em um arquivo
-- melhorar funcao de delimitador ?
-- verificar numero negativo
-- verificar se ele nao atende nenhum padrao e identificar como erro
-- refatorar
"""
def handle_line(index_line, line):
  global block_comment, is_comment_block
  line_length = len(line)
  index_character = 0

  while index_character < line_length:
    palavra = ""

    current_caracter = line[index_character]
    next_character = None
    if(index_character + 1 < line_length):
      next_character = line[index_character + 1]

    if is_comment_block: # comentario de bloco
      (has_found_end, comment, index_character) = find_end_block_comment(line, index_character)
      is_comment_block = not has_found_end
      block_comment += comment

      if has_found_end:
        print("achou um comentário \n", block_comment)
        tokens.append((index_line, AcronymsEnum.BLOCK_COMMENT.value, block_comment))
        block_comment = ""
        
      index_character += 1
      continue

    elif is_space(current_caracter): # espaco
      # ...
      index_character += 1
      continue

    elif current_caracter == '"': # cadeia de caractere
      (acronym, palavra, index_character) = find_string(line, index_character)
      tokens.append((index_line, acronym, palavra))

    elif is_delimiter(current_caracter): # delimitador
      tokens.append((index_line, AcronymsEnum.DELIMITER.value, current_caracter))

    elif(current_caracter == '!'):
      palavra = current_caracter
      if index_character + 1 < line_length and is_relational_operator(current_caracter+line[index_character+1]):
        index_character += 1
        palavra = current_caracter
        print('É um operador relacional: ', line[index_character-1]+current_caracter)
      else:
        print('É um operador lógico: ', current_caracter)

    elif is_relational_operator(current_caracter): # operador relacional
      palavra = current_caracter
      if index_character + 1 < line_length and is_relational_operator(current_caracter+line[index_character+1]):
        index_character += 1
        palavra = current_caracter
        print('É um operador relacional: ', line[index_character-1]+current_caracter)
      else:
        print('É um operador relacional: ', current_caracter)
    
    elif helper_logical_operator(current_caracter): # operador relacional
      if index_character + 1 < line_length and is_logical_operator(current_caracter+line[index_character+1]):
        index_character += 1
        palavra = line[index_character-1]
        palavra = current_caracter
        print('É um operador lógico: ', line[index_character-1]+current_caracter)
      else:
        raise Exception("Operador lógico não encontrado: "+current_caracter)

    elif current_caracter == '-':
      palavra = current_caracter
      acronym = AcronymsEnum.ARITHMETIC_OPERATOR.value
      next_character = ignore_space(line, index_character+1)
      if next_character < line_length and line[next_character].isnumeric():
        (acronym, number, index_character) = find_number(line, next_character)
        palavra += number
      tokens.append((index_line, acronym, palavra))

    elif current_caracter.isnumeric(): # numero
      (acronym, number, index_character) = find_number(line, index_character)
      tokens.append((index_line, acronym, number))

    elif current_caracter == '/': # comentario
      if next_character == '/':
        (comment, index_character) = line_comment(line, index_character)
        tokens.append((index_line, AcronymsEnum.LINE_COMMENT.value, comment))

      elif next_character == '*':
        is_comment_block = True
        continue # Ele agora vai seguir para o primeiro if para encontrar todos os comentários
      else:
        tokens.append((index_line, AcronymsEnum.ARITHMETIC_OPERATOR.value, current_caracter))

    elif(is_valid_string_symbol(current_caracter)): # identificador
      (palavra, index_character) = find_next(line, index_character)
      if reserved_regex.match(palavra):
        tokens.append((index_line, AcronymsEnum.RESERVED_WORD.value, palavra))
      else:
        tokens.append((index_line, AcronymsEnum.IDENTIFIER.value, palavra))
    else: # Não foi possível identificar o token
      tokens.append((index_line, AcronymsEnum.INVALID_CHARACTER.value, current_caracter))

    print("palavra\t",palavra)

    # next index
    index_character += 1

  return line

def remove_line_garbage(line):
  return line.strip()

def print_console_header(path_name):
  print("**********************************************")
  print("Analisando o arquivo: ", path_name)
  print("**********************************************")

root = "./files"
directory_files = [
  root+'/'+file_name
  for file_name in os.listdir(root) if os.path.isfile(root+'/'+file_name)
]

if __name__ == "__main__":
  for relative_path_name in directory_files:
    print_console_header(relative_path_name) 
    with open(relative_path_name, encoding = 'utf-8') as file:
      for index_line, line in enumerate(file):
        line = remove_line_garbage(line)
        handle_line(index_line, line)
      if is_comment_block:
        print("Bloco de comentário não foi fechado")
        tokens.append((index_line, AcronymsEnum.UNFORMED_COMMENT.value , block_comment))

print(tokens)

# IA ACABAR FICANDO ASSIM MAS EU REFATOREI PRA O QUE TA AI EM CIMA PRA DIMINUIR
# if __name__ == "__main__":
#   for _, _, directory_files in os.walk(root):
#     for file_name in directory_files:
#       relative_path_name = root+'/'+file_name
#       with open(relative_path_name, encoding = 'utf-8') as file:
#         print_header(relative_path_name) 
#         for index_line, line in enumerate(file):
#           line = remove_garbage_from_line(line)
#           handle_line(index_line, line)
      # if is_comment_block:
      #   print("Bloco de comentário não foi fechado")
      #   tokens.append((index_line, "CMF", block_comment))
