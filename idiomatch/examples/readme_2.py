import spacy
from idiomatch import Idiomatcher


def main():

    nlp = spacy.load("en_core_web_sm")
    idiomatcher = Idiomatcher(nlp)
    idioms = ["have blood on one's hands", "on one's hands"]
    idiomatcher.add_idioms(idioms)
    sent = "The leaders of this war have the blood of many thousands of people on their hands."
    doc = nlp(sent)
    print(idiomatcher.identify(doc))


if __name__ == '__main__':
    main()

