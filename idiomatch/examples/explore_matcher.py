import spacy
from spacy.matcher import Matcher


def main():
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    pattern_1 = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    pattern_2 = [{"LOWER": "hello"}, {"LOWER": "world"}]
    matcher.add("HelloWorld", [pattern_1, pattern_2])  # this is how you do logical-or join. Just pass it
    # a list of list of dict.

    doc = nlp("Hello, world! Hello world!")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)


if __name__ == '__main__':
    main()
