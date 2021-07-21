import spacy


def main():
    nlp = spacy.load("en_core_web_sm")
    nlp.tokenizer.add_special_case("one's", [{"ORTH": "one's"}])
    for token in nlp("ahead of one's time"):
        print(token.text)


if __name__ == '__main__':
    main()
