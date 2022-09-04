import os
import re

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
tokens = []
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

def is_valid_string_symbol(caractere):
  return ord(caractere) in simbolos_ascii

def ignore_space(line, last_index, line_length):
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
  if line[first_index] != '"':
    raise Exception("Não há aspas nesse index")

  last_index = first_index
  line_length = len(line)
  string = ""

  while last_index < line_length:
    if(not is_valid_string_symbol(line[last_index]) and line[last_index] != '"'):
      raise Exception("Caractere inválido:", line[last_index])
    string += line[last_index]
    if last_index > first_index and line[last_index] == '"':
      break
    last_index += 1

  if string[-1] != '"':
    #NESSE PONTO ELE ACHOU UMA STRING QUE NÃO FECHOU AS ASPAS
    raise Exception("String não fechou aspas")

  return (string, last_index)

def find_number(line, first_index, number = ""):
  last_index = first_index
  line_length = len(line)
  count_dot = 0

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
      # Pode ser um possivel erro
      break
    last_index += 1

  if(count_dot == 1 and not number[-1].isnumeric()):
    raise Exception("Um ponto precisa ser seguido de outro número")
  return (number, last_index)

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

    if is_comment_block: # comentario de bloco
      (has_found_end, comment, index_character) = find_end_block_comment(line, index_character)
      is_comment_block = not has_found_end
      block_comment += comment

      if has_found_end:
        print("achou um comentário \n", block_comment)
        tokens.append((index_line, "COB", block_comment))
        block_comment = ""
        
      index_character += 1
      continue

    elif is_space(line[index_character]): # espaco
      # ...
      index_character += 1
      continue

    elif line[index_character] == '"': # cadeia de caractere
      (palavra, index_character) = find_string(line, index_character)

    elif is_delimiter(line[index_character]): # delimitador
      palavra = line[index_character]

    elif is_relational_operator(line[index_character]): # operador relacional
      palavra = line[index_character]
      if index_character + 1 < line_length and is_relational_operator(line[index_character]+line[index_character+1]):
        index_character += 1
        palavra = line[index_character]
        print('É um operador relacional: ', line[index_character-1]+line[index_character])
      else:
        print('É um operador relacional: ', line[index_character])
      
    elif line[index_character] == '-':
      palavra = line[index_character]
      index_character = ignore_space(line, index_character+1, line_length)
      if index_character < line_length and line[index_character].isnumeric():
        (palavra, index_character) = find_number(line, index_character, palavra[-1])
      else:
        index_character -= 1
        print('É um operador aritmetico: ', palavra[-1])

    elif line[index_character].isnumeric(): # numero
      (palavra, index_character) = find_number(line, index_character)

    elif line[index_character] == '/': # comentario

      if index_character + 1 < line_length and line[index_character+1] == '/':
        (comment, index_character) = line_comment(line, index_character)
        tokens.append((index_line, "COL", comment))

      elif index_character + 1 < line_length and line[index_character+1] == '*':
        is_comment_block = True
        continue # Ele agora vai seguir para o primeiro if para encontrar todos os comentários
      else:
        tokens.append((index_line, "ART", line[index_character]))

    elif(is_valid_string_symbol(line[index_character])): # identificador
      (palavra, index_character) = find_next(line, index_character)
      if reserved_regex.match(palavra):
        tokens.append((index_line, "PRE", palavra))
      else:
        tokens.append((index_line, "IDE", palavra))
    else: # Não foi possível identificar o token
      tokens.append((index_line, "CIN", line[index_character]))

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
        tokens.append((index_line, "CMF", block_comment))

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
