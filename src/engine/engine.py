import re

from core.tokenizer import tokenize
from core.patterns import compile_patterns
from map.symbols import *


class Engine:
    DEFAULT = 0
    CAS = 1
    SPEEDCRUNCH = 2

    def __init__(self):
        self.patterns = compile_patterns()

    def _replace_symbols(self, pattern: re.Pattern, text: str, symbols: dict) -> str:
        return pattern.sub(lambda match: symbols[match.group(0)], text)

    def _replace(self, matches: re.Match | None, replace_format: str):
        if matches is None:
            return replace_format

        # Find all occurrences of \digit in the replace_format
        group_indices = [int(g) for g in re.findall(r'\\(\d+)', replace_format)]
        
        for group_idx in group_indices:
            group_value = matches.group(group_idx) or ""
            replace_format = replace_format.replace(f"\\{group_idx}", group_value, 1)
            print(group_idx, "\t|", matches.group(group_idx))

        replace_format = re.sub(r"\(\((.+?)\)\)", r"(\1)", replace_format)
        return re.sub(r"(\_|\^)?\(\)", "", replace_format)  # This will remove _() and ^() 

    def sub(self, pattern: str, replace: str, string: str) -> str:
        return re.sub(pattern, lambda matches: self._replace(matches, replace), string)

    def remove_tokens(self, string: str) -> str:
        repls = {
            r"<LL\d+>": "(",
            r"<RR\d+>": ")",
            r"<LP\d+>": "(",
            r"<RP\d+>": ")",
            r"<LO\d+>": "[",
            r"<RO\d+>": "]"
        }
        for token, repl in repls.items():
            string = re.sub(token, repl, string)
        return string

    def translate_units(self, string: str, mode: int) -> str:
        match mode:
            case self.DEFAULT:
                string = re.sub(r"<TE>", "", string)
            case self.CAS:
                ...
        return string

    def translate(self, string: str) -> str:
        string = string.replace("\\ ", "").replace(" ", "")
        string = tokenize(string)
        string = self._replace_symbols(self.patterns['greek'], string, greek)
        string = self._replace_symbols(self.patterns['sym'], string, sym)
        string = self._replace_symbols(self.patterns['arrows'], string, arrows)
        string = self.translate_units(string, self.DEFAULT)

        steps = [
            (self.patterns['integral'], r"integral(\7,\9,\1\3,\4\6)"),
            (self.patterns['fns'],      r"\1(\5_(\6\10)^(\9\11)(\14\16)_(\15\17)^(\18\20))^(\2\4)"),
            (self.patterns['sqrt'],     r"sqrt(\2)"),
            (self.patterns['nthrt'],    r"root(\4,\2)"),
            (self.patterns['frac'],     r"(\2)/(\4)"),
            (self.patterns['binom'],    r"nCr(\2,\4)"),
            (self.patterns['perm'],     r"nPr(\2,\3\5)")
        ]

        for pat, rep in steps:
            string = self.sub(pat, rep, string)

        string = self.remove_tokens(string)
        return string
    

s = r'\alpha+\frac{1}{3}\left(x-1\right)^{n+1}+\left(x-1\right)_3-\binom{4}{\frac{3}{x}}'
# s = r'\int_a^bf\left(x\right)\text{d}x'
s = r"\tan^2f'\left(x\right)"

s = r"\sqrt[n]{1}-\text{kg}"

k = Engine()

result = k.translate(s)
print(result)

# jotai tämmöst pitää käyttää

    # def replace_multiplicand(match):
    #     return ")*" + match.group(1)