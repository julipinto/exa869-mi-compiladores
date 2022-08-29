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

def isSpace(char):
  return char == " " or char == "\t"

def isDelimiter(char):
  return char in ["(", ")", ";", ",", "=", ":", ".", ">", "<", "!", "&", "|", "~", "^", "*", "/", "-", "+", " ", "\t"]

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

def handleLine(linha):
    line_length = len(linha)
    index = 0
    while index < line_length:
      palavra = ""
      if linha[index] == '"':
        (palavra, index) = findString(linha, index)
      elif isSpace(linha[index]):
        index += 1
        continue
      elif isDelimiter(linha[index]):
        palavra = linha[index]
      elif linha[index].isnumeric():
        (palavra, index) = findNumber(linha, index)
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