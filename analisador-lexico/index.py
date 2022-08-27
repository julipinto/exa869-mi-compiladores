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
def acharString(linha, index_primeira_aspas):
  if linha[index_primeira_aspas] != '"':
    raise Exception("Não há aspas nesse index")

  index_final_string = index_primeira_aspas
  tamanho_linha = len(linha)
  string = ""

  while index_final_string < tamanho_linha:
    string += linha[index_final_string]
    if index_final_string > index_primeira_aspas and linha[index_final_string] == '"':
      break
    index_final_string += 1

  if string[-1] != '"':
    #NESSE PONTO ELE ACHOU UMA STRING QUE NÃO FECHOU AS ASPAS
    raise Exception("String não fechou aspas")
    pass

  return (string, index_final_string)

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
      elif linha[index].isnumeric():
        #aquela parte que acha o número
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
      tratarLinha(x)