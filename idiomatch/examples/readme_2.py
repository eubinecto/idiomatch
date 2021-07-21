import spacy
from idiomatch import IdiomMatcher


def main():

    nlp = spacy.load("en_core_web_sm")
    idiom_matcher = IdiomMatcher(nlp)
    idioms = ["have blood on one's hands", "on one's hands"]
    idiom_matcher.add_idioms(idioms)
    sent = "The leaders of this war have the blood of many thousands of people on their hands."
    doc = nlp(sent)
    print(idiom_matcher.identify(doc))


if __name__ == '__main__':
    main()

