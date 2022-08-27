import re

"""
This is a regex generator for the lexical analyzer.
It generates a regex that matches all passed the keywords.

Based oh the question on StackOverflow: https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3
"""

class Trie():
    """Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())

# makeTrie = Trie()

# makeTrie.add("var")
# makeTrie.add("const")
# makeTrie.add("struct")
# makeTrie.add("extends")
# makeTrie.add("procedure")
# makeTrie.add("function")
# makeTrie.add("start")
# makeTrie.add("return")
# makeTrie.add("if")
# makeTrie.add("else")
# makeTrie.add("then")
# makeTrie.add("while")
# makeTrie.add("read")
# makeTrie.add("print")
# makeTrie.add("int")
# makeTrie.add("real")
# makeTrie.add("boolean")
# makeTrie.add("string")
# makeTrie.add("true")
# makeTrie.add("false")

