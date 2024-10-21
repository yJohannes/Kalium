import re

from core.tokenizer import tokenize
from core.patterns import compile_patterns
from symbols.symbols import sym, greek

s = r'\frac{1}{3}\left(x-1\right)^{n+1}'

s = tokenize(s)

class Kalium:
    def __init__(self):
        self.patterns = compile_patterns()

    def translate(self, s):
        def repl(matches):
            g = matches.groups()

            r_fns = r"\1((\5\7)_(\8\10)^(\11\13))^(\2\4)"

            r = f"{g[0]}("

            r += f"({g[4]}{g[6]})"
            
            if g[8-1] or g[10-1]:
                r += f"_({g[7]}{g[9]})"

            if g[11-1] or g[13-1]:
                r += f"^({g[10]}{g[12]})"
            
            r += ")"

            if g[2-1] or g[4-1]:
                r += f"^({g[1]}{g[3]})"
            print(r)
            return r


        s = re.sub(self.patterns['fns'], repl, s)
        return(s)

k = Kalium()

result = k.translate("\\sinx")
print(result)
# jotai tämmöst pitää käyttää

    # def replace_multiplicand(match):
    #     return ")*" + match.group(1)