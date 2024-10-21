import re
from core.composer import Composer

com = Composer()

com.new()
integral = com.fn("int") + com.base() + com.exponent() + com.match_all() + com.delimiter("d")

com.new()
sum_prod = com.fns(["sum", "prod"]) + com.base() + com.exponent() + com.fn_body()

# com.new()
# lim

com.new()
fns = com.fns([
        "floor", "ceil", "sign", "round", "int",
        "sin", "cos", "tan", "csc", "sec", "cot",
        "arcsin", "arccos", "arctan",
        "arccsc", "arcsec", "arccot",
        "exp", "ln"]) + com.opt_exponent() + com.fn_body()

com.new()
log = com.fn("log") + com.opt_base() + com.fn_body()

com.new()
lg = com.fn("lg") + com.opt_exponent() + com.fn_body()

com.new()
sqrt = com.fn("sqrt") + com.cgroup()

com.new()
nthrt = com.fn("sqrt") + com.sgroup() + com.cgroup()

com.new()
frac = com.fn("frac") + com.cgroup() + com.cgroup()

com.new()
binom = com.fn("binom") + com.cgroup() + com.cgroup()

com.new()
perm = com.pgroup() + com.base()

com.new()
cases = com.begin("cases") + com.match_all() + com.end("cases")

com.new()
mat = com.begin("matrix") + com.match_all() + com.end("matrix")

com.new()
t = com.fn("log") + com.opt_base() + com.fn_pre_arg() + com.fn_body()


# patterns = [integral, sum_prod, fns, log, lg, sqrt, nthrt, frac, comb, perm, cases, mat]
patterns = {
    'integral': integral,
    'sum_prod': sum_prod,
    'fns': fns,
    'log': log,
    'lg': lg,
    'sqrt': sqrt,
    'nthrt': nthrt,
    'frac': frac,
    'binom': binom,
    'perm': perm,
    'cases': cases,
    'mat': mat
}
def compile_patterns() -> dict[re.Pattern]:
    compiles = {}
    for name, pattern in patterns.items():
       compiles[name] = re.compile(pattern)
    return compiles

# lisää patternien teko symboleil

# esim ln f(x) saa jos kattoo mil alkaa

# ja lisää juttuja loppuun mitkä tarkistaa merkinnät esim korkeamman asteen derivaatta f^(4)x