from core.tokenizer import tokens
# https://regex101.com/

class Composer:
    """Call new() to start composing a new pattern"""
    w = r"a-zA-Zα-ωΑ-Ω0-9"

    def new(self) -> None:
        self.n = 0

    def chars(self) -> str:
        """
        `No capture group, returns latin and greek alphabet`
        \+0
        """
        return "a-zA-Zα-ωΑ-Ω"

    def exponent(self) -> str:
        """
        `group \\1` ... short exponent\n
        `group \\3` ... long exponent\n
        \+3
        """
        self.n += 3
        return fr"\^(?:([{self.w}])|<LL(\d+)>(.*)<RR\{self.n-1}>)"

    def base(self) -> str:
        """
        `group \\1` ... short base\n
        `group \\3` ... long base\n
        \+3
        """
        self.n += 3
        return fr"_(?:([{self.w}])|<LL(\d+)>(.*)<RR\{self.n-1}>)"

    def opt_exponent(self) -> str:
        """
        `group \\1` ... short exponent\n
        `group \\3` ... long exponent\n
        \+3
        """
        self.n += 3
        return fr"(?:\^(?:([{self.w}])|<LL(\d+)>(.*)<RR\{self.n-1}>))?"

    def opt_base(self) -> str:
        """
        `group \\1` ... short base\n
        `group \\3` ... long base\n
        \+3
        """
        self.n += 3
        return fr"(?:_(?:([{self.w}])|<LL(\d+)>(.*)<RR\{self.n-1}>))?"

    def fn(self, fn: str) -> str:
        """
        `No capture group`\n
        \+0
        """
        return fr"\\{fn}" 

    def fns(self, fns: list[str]) -> str:
        """
        `group \\1` ... function name\n
        \+1
        """
        self.n += 1
        return r"\\(" + "|".join(fns) + ")"
    
    # mitä jos sin toisen kerran?
    # ehkä vois laittaa jonku jutun tähä ettei tuu kertomerkkii funktion ja ( väli
    def fn_pre_arg(self) -> str:
        """
        `group \\1` ... possible function as arg, e.g. `f(x)`\n
        `group \\2` ... short base\n
        `group \\4` ... long base\n
        `group \\5` ... short exponent\n
        `group \\7` ... long exponent\n
        \+7
        """
        self.n += 1
        return "([a-zA-Zα-ωΑ-Ω]+)?" + self.opt_base() + self.opt_exponent()

    def fn_arg(self) -> str:
        """
        `group \\1` ... argument no parentheses\n
        `group \\3` ... argument with parentheses\n
        \+3
        """
        self.n += 3
        return fr"(?:([{self.w}.,°]+)|<LP(\d+)>(.*)<RP\{self.n-1}>)"
    
    def fn_body(self) -> str:
        """
        Combines fn_arg + opt_base + opt_exponent\n

        `group \\1` ... argument no parentheses\n
        `group \\3` ... argument with parentheses\n

        `group \\4` ... short base\n
        `group \\6` ... long base\n

        `group \\7` ... short exponent\n
        `group \\9` ... long exponent\n
        \+9
        """
        return self.fn_arg() + self.opt_base() + self.opt_exponent()

    def pgroup(self) -> str:
        """
        Parentheses enclosed group\n
        `group \\2` ... enclosed group\n
        \+2
        """
        self.n += 2
        return fr"<LP(\d+)>(.*)<RP\{self.n-1}>"

    def cgroup(self) -> str:
        """
        Curly braces enclosed group\n
        `group \\2` ... enclosed group\n
        \+2
        """
        self.n += 2
        return fr"<LL(\d+)>(.*)<RR\{self.n-1}>"
    
    def sgroup(self) -> str:
        """
        Square brackets enclosed group\n
        `group \\2` ... enclosed group\n
        \+2
        """
        self.n += 2
        return fr"<LS(\d+)>(.*)<RS\{self.n-1}>"

    def match_all(self):
        """
        `group \\1` ... matches 0 or more\n
        \+1
        """
        self.n += 1
        return r"(.*)"

    def delimiter(self, s: str) -> str:
        """
        Delimiter, e.g. `d` in `\\int_a^b x dx`\n
        \+1
        """
        self.n += 1
        return fr"(?:{s}|<TE><LL(\d+)>{s}<RR\{self.n}>)"
    
    def begin(self, name: str) -> str:
        """
        \+1
        """
        token = tokens[f"\\begin{{{name}}}"]
        self.n += 1
        return fr"<{token}(\d+)>"

    def end(self, name: str) -> str:
        token = tokens[f"\\end{{{name}}}"]
        return fr"<{token}(\{self.n})>"

"""
\begin{cases}
-x&{,}\ x>0\\
+n&{,}\ x=0\\
+x&{,}\ x<0
\end{cases}

\begin{matrix}
1&2\\
3&4\\
5&6
\end{matrix}
"""
    
# NAME GROUPS ?P<func>

# translateUnits1(expression)
# translateSum(expression)
# translateProd(expression)
# translateIntegrals(expression) # SIIRRETTY TÄHÄN
# translateCommonFunctions(expression)
# translateLimits(expression)
# translateCombinations(expression) # merkintä kai \left(n\right)_k
# translatePermutations(expression)
# translateFractions(expression)
# engine.translateLn(expression)
# translateLog(expression)
# translateLowerIndexazAZ(expression)
# translateLg(expression) # \sqrt[\sqrt{2}+1]{\sqrt{3-x}}
# translateSqrt(expression)
# translateSystem(expression)
# translateArrows(expression)
# translateVectors(expression)

# translateMatrices(expression)




# log = r"\\log(?:_(?:(\w)|<LL(\d+)>(.+)<RR\2>))?(?:([\w.,°]+)|<LP(\d+)>(.+)<RP\5>)(?:\^(?:(\w)|<LL(\d+)>(.+)<RR\8>))?"
