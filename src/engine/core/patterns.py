import re
from core.composer import Composer
from map.symbols import *


com = Composer()

patterns = {
    'integral': com.new(com.fn("int"), com.base(), com.exponent(), com.match_all(), com.differential()),
    'sum_prod': com.new(com.fns(["sum", "prod"]), com.base(), com.exponent(), com.fn_body()),
    'fns': com.new(
        com.fns(["floor", "ceil", "sign", "round", "int", "sin", "cos", "tan", "csc", "sec", "cot",
                 "arcsin", "arccos", "arctan", "arccsc", "arcsec", "arccot", "exp", "ln"]),
        com.opt_exponent(), com.fn_pre_arg(), com.fn_body()
    ),
    'log':   com.new(com.fn("log"),   com.opt_base(),     com.fn_pre_arg(), com.fn_body()),
    'lg':    com.new(com.fn("lg"),    com.opt_exponent(), com.fn_pre_arg(), com.fn_body()),
    'sqrt':  com.new(com.fn("sqrt"),  com.cgroup()),
    'nthrt': com.new(com.fn("sqrt"),  com.ogroup(),       com.cgroup()),
    'frac':  com.new(com.fn("frac"),  com.cgroup(),       com.cgroup()),
    'binom': com.new(com.fn("binom"), com.cgroup(),       com.cgroup()),
    'perm':  com.new(com.pgroup(),    com.base()),
    'cases': com.new(com.begin("cases"),   com.match_all(), com.end("cases")),
    'mat':   com.new(com.begin("matrix"),  com.match_all(), com.end("matrix")),
}

def compile_patterns() -> dict[re.Pattern]:
    compiles = {}
    for name, pattern in patterns.items():
       compiles[name] = re.compile(pattern)

    compiles['greek'] = re.compile(r'|'.join(re.escape(key) for key in greek))
    compiles['sym'] = re.compile(r'|'.join(re.escape(key) for key in sym))
    compiles['arrows'] = re.compile(r'|'.join(re.escape(key) for key in arrows))


    return compiles


# esim ln f(x) saa jos kattoo mil alkaa

# ja lisää juttuja loppuun mitkä tarkistaa merkinnät esim korkeamman asteen derivaatta f^(4)x