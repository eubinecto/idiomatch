from service import build_iip


def main():
    mip = build_iip()
    # the sentences
    sent_non_comp = "The congress intends to seize power by hook or by crook."
    sent_non_comp_hyphen = "You are down to earth."
    sent_decomp = "Have you found your feet on the new job?"
    sent_decomp_alt = "To ask our members to accept a pay cut heaps insult on injury."
    sents = [sent_non_comp, sent_non_comp_hyphen, sent_decomp, sent_decomp_alt]
    print("original | tokenised & lemmatised")
    for sent in sents:
        # tokenise
        tokens = mip(sent)
        # lemmatise
        lemmas = [token.lemma_ for token in tokens]
        print(sent, "|", lemmas)


if __name__ == '__main__':
    main()
