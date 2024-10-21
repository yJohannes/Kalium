import re

from core.tokenizer import tokenize
from core.patterns import compile_patterns
from symbols.symbols import sym, greek


class Engine:
    def __init__(self):
        self.patterns = compile_patterns()

    def _replace(self, matches: re.Match | None, replace_format: str, order: list[int]):
        if matches is None:
            return replace_format

        for group_idx in order:
            group_value = matches.group(group_idx) or ""
            replace_format = replace_format.replace(f"\\{group_idx}", group_value, 1)
            print(group_idx, "\t|", matches.group(group_idx))

        replace_format = re.sub(r"\(\((.+?)\)\)", r"(\1)", replace_format)
        return re.sub(r"(\_|\^)?\(\)", "", replace_format)  # This will remove _() and ^() 

    def sub(self, pattern: str, replace: str, order: list[int], string: str) -> str:
        return re.sub(pattern, lambda matches: self._replace(matches, replace, order=order), string)

    def remove_tokens(self, string: str) -> str:
        repls = {
            r"<LL\d+>": "(",
            r"<RR\d+>": ")",
            r"<LP\d+>": "(",
            r"<RP\d+>": ")"
        }
        for token, repl in repls.items():
            string = re.sub(token, repl, string)
        return string

    def translate(self, string: str) -> str:
        string = tokenize(string)

        steps = [
            (
                self.patterns['fns'],
                r"\1((\5\7)_(\8\10)^(\11\13))^(\2\4)",
                [1, 5, 7, 8, 10, 11, 13, 2, 4]
            ),
            (
                self.patterns['sqrt'],
                r"sqrt(\2)",
                [2]
            ),
            (
                self.patterns['frac'],
                r"(\2)/(\4)",
                [2, 4]),
            (
                self.patterns['binom'],
                r"nCr(\2,\4)",
                [2, 4]
            ),
            (
                self.patterns['perm'],
                r"nPr(\2,\3\5)",
                [2, 3, 5]
            ),
        ]

        for pat, rep, order in steps:
            string = self.sub(pat, rep, order, string)

        string = self.remove_tokens(string)
        return string

s = r'\frac{1}{3}\left(x-1\right)^{n+1}+\left(x-1\right)_3-\binom{4}{\frac{3}{x}}'
s = r'\sqrt{1}'

k = Engine()

result = k.translate(s)
print(result)
# jotai tämmöst pitää käyttää

    # def replace_multiplicand(match):
    #     return ")*" + match.group(1)