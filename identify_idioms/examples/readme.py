import spacy
from identify_idioms import IdiomMatcher


def main():

    sentences = [
        "He called my blatant bluff",  # modification
        "This will keep all of us posted",  # openslot
        "That was one balls-out street race!",  # hyphenated
        "That was one balls out street race!",  # hyphen omitted
        "the floodgates are finally opened",  # passivisation with modification
        "my bluff was embarrassingly called by her",   # passivisation with openslot
        "If she dies, you wil have her blood on your hands!"  # inclusion
    ]

    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline. Currently supports en_core_web_sm only.
    idiom_matcher = IdiomMatcher.from_pretrained(nlp)  # this will take approx 40 seconds.

    sent = sentences[0]
    print("### modification ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[1]
    print("### openslot ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[2]
    print("### hyphenated ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[3]
    print("### hyphen omitted ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[4]
    print("### passivisation (modification) ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[5]
    print("### passivisation (openslot) ###\n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[6]
    print("### inclusion ### \n: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))


if __name__ == '__main__':
    main()
