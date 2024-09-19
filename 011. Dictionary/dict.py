import json
from difflib import get_close_matches

data = json.load(open("data.json"))


def translate(comb: str):
    comb = comb.lower()
    if comb in data:
        return data[comb]
    elif comb.title() in data:
        return data[comb.title()]
    elif comb.upper() in data:
        return data[comb.upper()]
    elif len(get_close_matches(comb, data.keys())) > 0:
        a = len(get_close_matches(comb, data.keys()))
        print(a, get_close_matches(comb, data.keys()))
        b = 0
        resolved = True
        while resolved:
            resolved = False
            answer = 'n'
            while answer == 'n':
                print("Did you mean %s instead of" % get_close_matches(comb, data.keys())[b])
                answer = (input("Enter 'Y' for yes, 'N' for No: ")).lower()
                b += 1
            return print(data[get_close_matches(comb, data.keys())[b - 1]])
    else:
        print("You have entered non-existing word!\nTry again!")


word = (input("Enter word for search: "))
output = translate(word)
#  print(output)

if type(output) == list:
    x = 1
    for item in output:
        print("Meaning {}: {}".format(x, item))
        x += 1
else:
    print(output)
