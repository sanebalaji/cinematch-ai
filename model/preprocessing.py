from ast import literal_eval 

def convert(text):
    L=[]
    text = literal_eval(text)
    for i in text:
        L.append(i['name'])
    return L


def convert3(text):
    L=[]
    text = literal_eval(text)
    counter = 0
    for i in text:
        if (counter !=3):
            L.append(i['name'])
            counter+=1
        else:
            break
    return L          


def fetch_director(text):
    L = []

    text = literal_eval(text)

    for i in text:

        if i["job"] == "Director":

            L.append(i["name"])

            break

    return L









