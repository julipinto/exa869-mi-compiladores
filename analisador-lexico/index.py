import re
root = "./files/"
demo = root + "demofile.txt"

operadores_aritmeticos = ["+", "-", "*", "/", "++", "--"] 
operadores_relacionais = ["!=", "==", "<", ">", "<=", ">=", "="]
operadores_logicos = ["&&", "||", "!"]
deliminadores = [";", ",", "(", ")", "[", "]", "{", "}", ".", " ", "\t"]
reservadas = ["var", "const", "struct", "extends", "procedure",
              "function", "start", "return", "if", "else", "then",
              "while", "read", "print", "int", "real", "boolean",
              "string", "true", "false"]

"""
  Dado uma linha e um index, ele verifica se a linha nesse index
  são aspas, e a partir daí ele vai concatenando os caracteres
  até encontrar o fechamento das aspas.
"""
def acharString(linha, index_aspas):
  if linha[index_aspas] != '"':
    raise Exception("Não há aspas nesse index")

  final_string = index_aspas
  line_length = len(linha)
  string = ""

  while final_string < line_length:
    string += linha[final_string]
    if final_string > index_aspas and linha[final_string] == '"':
      break
    final_string += 1

  return (string, final_string)

def isSpace(char):
  return char == " " or char == "\t"

def isDelimiter(char):
  return char in ["(", ")", ";", ",", "=", ":", ".", ">", "<", "!", "&", "|", "~", "^", "*", "/", "-", "+", " ", "\t"]

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

def tratarLinha(linha):
    line_length = len(linha)
    index = 0
    while index < line_length:
      palavra = ""
      if linha[index] == '"':
        (palavra, index) = acharString(linha, index)
      elif isSpace(linha[index]):
        index += 1
        continue
      elif isDelimiter(linha[index]):
        palavra = linha[index]
      else:
        (palavra, index) = findNext(linha, index)
        if palavra in reservadas:
          print('palavra reservada', palavra)
          continue
      
      print("palavra\t",palavra)

      # next index
      index += 1

    return linha

f = open(demo, "r")
for x in f:
  x = x.strip()
  tratarLinha(x)
  
f.close()