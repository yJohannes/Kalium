tokens = {
    "\\left(":              "LP",
    "\\right)":             "RP",
    "\\left[":              "LS",
    "\\right]":             "RS",
    "\\left{":              "LC",
    "\\right}":             "RC",
    
    "{":                    "LL",
    "}":                    "RR",

    "\\begin{cases}":       "BC",
    "\\end{cases}":         "EC",
    "\\begin{matrix}":      "BM",
    "\\end{matrix}":        "EM",

    "\\int":                "IN",

    "\\text":               "TE",
    "\\mathrm":             "TE"
}

# Make process all at once
def pair(s: str, left, right, left_to, right_to) -> str:
    result = []
    stack = []
    num_pairs = 0
    i = 0

    while i < len(s):
        if s[i:i+len(left)] == left:
            num_pairs += 1
            stack.append(num_pairs)
            result.append(f"<{left_to}{num_pairs}>")
            i += len(left)
        elif s[i:i+len(right)] == right:
            # if stack:
                current_number = stack.pop()
                result.append(f"<{right_to}{current_number}>")
            # else:
                # raise Exception(f"Warning: Unmatched closing '{right}' found at index {i}")
                i += len(right)
        else:
            result.append(s[i])
            i += 1
    
    # if stack:
        # raise Exception(f"Warning: Incomplete Pairing of '{left}' and '{right}'")

    return ''.join(result)

def tokenize(s: str):

    s = pair(s, "\\left(", "\\right)", "LP", "RP")
    s = pair(s, "\\left[", "\\right]", "LS", "RS")
    s = pair(s, "\\left{", "\\right}", "LC", "RC")

    s = pair(s, "\\begin{cases}", "\\end{cases}", "BC", "EC")
    s = pair(s, "\\begin{matrix}", "\\end{matrix}", "BM", "EM")

    s = pair(s, "{", "}", "LL", "RR")

    # "\\int":                "IN",

    s = s.replace("\\text", "<TE>")
    s = s.replace("\\mathrm", "<TE>")

    return s

if __name__ == '__main__':
    
    s = "{{hello{world}{test}}{end}"
    try:
        tokenize(s)
    except Exception as e:
        print(e)