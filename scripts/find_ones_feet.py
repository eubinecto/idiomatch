from service import build_mip


def main():
    sent = "Have you found your feet on the new job?"
    mip = build_mip()
    tokens = mip(sent)
    lemmas = [token.lemma_ for token in tokens]
    print("original:", sent)
    print("tokenised & lemmatised:", lemmas)


if __name__ == '__main__':
    main()
