def tokenise_line(code):
    code = code.removeprefix("(")
    code = code.removesuffix(")")
    code = code.strip()

    # removes excessive whitespace
    i = 0
    bracket_cntr = 0
    token = []
    newtoken = []
    while (i + 1) <= len(code):
        if code[i] == " " and bracket_cntr == 0:
            if not newtoken:
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        if code[i] == "(":
            bracket_cntr += 1
            if bracket_cntr > 1:
                newtoken.append(code[i])
                i += 1
                continue
            if not newtoken:
                newtoken.append(code[i])
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            newtoken.append(code[i])
            i += 1
        if code[i] == ")":
            bracket_cntr -= 1
            if bracket_cntr > 0:
                newtoken.append(code[i])
                i += 1
                continue
            newtoken.append(code[i])
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        newtoken.append(code[i])

        """if (i + 1) == len(code):
            if not newtoken:
                break
            #newtoken.append(code[i])
            token.append("".join(newtoken))
            break"""

        i += 1
    if newtoken:
        token.append("".join(newtoken))
    return token


print(tokenise_line("(lambda () (+ x 1))"))
