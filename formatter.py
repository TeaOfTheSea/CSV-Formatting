#This file is something I wroke to automation the building of selections for sql fields from a woorkbook that my boss maintains and I sometimes work out of.

data = open("text.txt").readlines()
output = open("output.txt", "a")
for i in range(len(data)):
    if i == 0:
        prefix = "\"SELECT "
    else:
        prefix = "    , "
    if i == len(data)-1:
        postfix = "\""
    else:
        postfix = "\n"
    text=data[i].strip()
    underscore = text.find("_")
    text2 = text[:underscore:] + "." + text[underscore+1::]
    output.write(prefix + text2 + " as " + text + postfix)
