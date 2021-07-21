
import spacy


def main():
    nlp = spacy.load("en_core_web_sm")
    for token in nlp("keep something at arm's length"):
        print(token.pos_)


if __name__ == '__main__':
    main()
