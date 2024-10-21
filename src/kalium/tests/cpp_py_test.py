import ctypes

lib = ctypes.CDLL('./libpair.dll')
lib.pair.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.pair.restype = ctypes.c_char_p

def pair(s: str, left: str, right: str, left_to: str, right_to: str) -> str:
    result = lib.pair(s.encode('utf-8'), left.encode('utf-8'), right.encode('utf-8'), left_to.encode('utf-8'), right_to.encode('utf-8'))
    return result.decode('utf-8')

s = "(wow(Cat)(greg))(fly)"
left = "("
right = ")"
left_to = "L"
right_to = "R"
print(pair(s, left, right, left_to, right_to))
