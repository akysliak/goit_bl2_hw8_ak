def print_result_tag(res: list) -> str:
    out = ""
    for el in res:
        out += el + "\n"
    if not out:
        out = "Nothing found."
    return out.strip()


def print_result_author(res: list) -> str:
    out = ""
    #print("res:", res)
    for el in res:
        for author, quotes in el.items():
            out += f"{author}:\n"
            for quote in quotes:
                out += f"\t{quote}\n"
    if not out:
        out = "Nothing found."
    return out.strip()
