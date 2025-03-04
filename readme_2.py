import spacy
from idiomatch import Idiomatcher


def main():
    nlp = spacy.load("en_core_web_sm")
    idiomatcher = Idiomatcher.from_pretrained(nlp.vocab)  # instantiate 
    # As for a placeholder for openslot, use either: someone / something / someone's / one's 
    idioms = ["have blood on one's hands", "on one's hands"]
    idiomatcher.add_idioms(nlp, idioms)  # this will train idiomatcher to identify the given idioms
    sent = "The leaders of this war have the blood of many thousands of people on their hands."
    doc = nlp(sent)
    print(idiomatcher(doc))


if __name__ == '__main__':
    main()
