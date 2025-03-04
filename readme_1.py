import spacy
from idiomatch import Idiomatcher


def main():
    sent = "The floodgates will remain opened for a host of new lawsuits."  # a usecase of *open the floodgates*
    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline; Currently supports en_core_web_sm only.
    idiomatcher = Idiomatcher.from_pretrained(nlp.vocab)  # this will take approx 50 seconds.
    doc = nlp(sent)  # process the sentence with an nlp pipeline
    print(idiomatcher(doc))  # identify the idiom in the sentence


if __name__ == '__main__':
    main()
