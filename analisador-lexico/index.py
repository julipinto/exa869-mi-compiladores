import re

root = "./files/"
demo = root + "demofile.txt"

operadores_aritmeticos = {"+", "-", "*", "/", "++", "--"} 
operadores_relacionais = {"!=", "==", "<", ">", "<=", ">=", "="}
operadores_logicos = {"&&", "||", "!"}
deliminadores = {";", ",", "(", ")", "[", "]", "{", "}", ".", " ", "\t"}
reserved_regex = re.compile("(?:boolean|const|e(?:lse|xtends)|f(?:alse|unction)|i(?:nt|f)|pr(?:int|ocedure)|re(?:a[dl]|turn)|st(?:art|r(?:ing|uct))|t(?:hen|rue)|var|while)$")

"""
  Dado uma linha e um index, ele verifica se a linha nesse index
  são aspas, e a partir daí ele vai concatenando os caracteres
  até encontrar o fechamento das aspas.
"""
def findString(line, first_index):
  if line[first_index] != '"':
    raise Exception("Não há aspas nesse index")

  last_index = first_index
  line_length = len(line)
  string = ""

  while last_index < line_length:
    string += line[last_index]
    if last_index > first_index and line[last_index] == '"':
      break
    last_index += 1

  if string[-1] != '"':
    #NESSE PONTO ELE ACHOU UMA STRING QUE NÃO FECHOU AS ASPAS
    raise Exception("String não fechou aspas")

  return (string, last_index)

def findNumber(line, first_index):
  last_index = first_index
  line_length = len(line)
  number = ""
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

def isComment(line, first_index):
  last_index = first_index
  line_length = len(line)
  comment = ""

  while last_index < line_length:
    if(line[last_index] == '*'):
      comment += line[last_index]
      if(line[last_index+1] == '/'):
        comment += line[last_index+1]
        last_index += 2
        break
    last_index += 1

  if(comment[last_index-1] != '*' and comment[-1] != '/'):
    raise Exception("Um ponto precisa ser seguido de outro número")
  return (comment, last_index)

def isSpace(char):
  return char == " " or char == "\t"

def isDelimiter(char):
  return char in ["(", ")", ";", ",", "=", ":", ".", ">", "<", "!", "&", "|", "~", "^", "*", "-", "+", " ", "\t"]

"""
Essa função vai achar o próximo conjunto de caracteres
"""
def findNext(linha, index):
  final_string = index
  line_length = len(linha)
  string = ""

  while final_string < line_length:
    if final_string >= index and linha[final_string] in deliminadores:
      break
    string += linha[final_string]
    final_string += 1

  return (string, final_string)

def lineComment(line, index):
  if line[index] != '/' and line[index+1] != '/':
    raise Exception("Não é um comentário de linha")

  line_length = len(line)
  index_end = index
  comment = ""

  while index_end < line_length:
    comment += line[index_end]
    index_end += 1

  return (comment, index_end)

def findEndBlock(line, index_start):
  line_length = len(line)
  index_end = index_start
  comment = ""

  while index_end < line_length:
    comment += line[index_end]
    if len(comment) > 1 and  comment[-2] == '*' and comment[-1] == '/':
      return (True, comment, index_end)
    index_end += 1
  
  return (False, comment, index_end)

block_comment = ""
is_comment_block = False

def handleLine(linha):
    global block_comment, is_comment_block
    line_length = len(linha)
    index = 0
    while index < line_length:
      palavra = ""
      if is_comment_block:
        (achou, comment, index) = findEndBlock(linha, index)
        is_comment_block = not achou
        block_comment += comment
        if achou:
          block_comment = ""
          print("achou o comentário \n", block_comment)
        index += 1
        continue
      elif linha[index] == '"':
        (palavra, index) = findString(linha, index)
      elif isSpace(linha[index]):
        index += 1
        continue
      elif isDelimiter(linha[index]):
        palavra = linha[index]
      elif linha[index].isnumeric():
        (palavra, index) = findNumber(linha, index)
      elif linha[index] == '/':
        if linha[index+1] == '/':
          (comment, index) = lineComment(linha, index)
        elif linha[index+1] == '*':
          is_comment_block = True
          continue
        #  (achou, comment, index) = findEndBlock(linha, index)
        #  is_comment_block = not achou
        #  block_comment += comment
        #if achou:
        #  print("achou o comentário \n", block_comment)
        else:
          palavra = linha[index] # vai ser um operador

      else:
        (palavra, index) = findNext(linha, index)
        if reserved_regex.match(palavra):
          print('palavra reservada', palavra)
          continue

      print("palavra\t",palavra)

      # next index
      index += 1

    return linha


if __name__ == "__main__":
  with open(demo, encoding = 'utf-8') as f:
    for x in f:
      x = x.strip()
      handleLine(x)
