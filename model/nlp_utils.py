from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def stem(text):

    L = []

    for word in text.split():

        L.append(ps.stem(word))

    return " ".join(L)


