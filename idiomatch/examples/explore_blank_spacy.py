
import spacy


def main():
    # https://github.com/explosion/spaCy/discussions/5886#discussioncomment-189675
    sent = "this is my test sentence"
    nlp = spacy.blank("en")
    tokenizer = nlp.tokenizer
    for token in tokenizer(sent):
        print(token)


if __name__ == '__main__':
    main()