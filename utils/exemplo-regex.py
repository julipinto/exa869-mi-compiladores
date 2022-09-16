import re
# Depois da regex gerada tem que adicionar $ no final
pattern = "(?:boolean|const|e(?:lse|xtends)|f(?:alse|unction)|i(?:nt|f)|pr(?:int|ocedure)|re(?:a[dl]|turn)|st(?:art|r(?:ing|uct))|t(?:hen|rue)|var|while)$"
reserved_regex = re.compile(pattern)
print(reserved_regex.match("var"))
print(reserved_regex.match("boleeano"))
print(reserved_regex.match("els e"))
print(reserved_regex.match("extends"))