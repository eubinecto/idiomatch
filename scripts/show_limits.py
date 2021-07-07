"""
What we cannot do yet.
"""
from identify_idioms.service import build_iip


def main():
    iip = build_iip()
    sents = [
        # a modification case for "grasp at straws"
        "He grasped at straws",  # TP
        "He grasped desperately at the floating straw.",  # FN
        # an open slot case for "keep someone's at arm's length"
        "They preferred to persist in the strategy of keeping them at arm's length.",  # TP
        "They preferred to persist in the strategy of keeping both Germans and Russians at arm's length.",  # FN
        # a passivisation case for "open the floodgates".
        "And with him gone, they opened the floodgates",  # TP
        "And with him gone, the floodgates were opened."  # FN
    ]
    for sent in sents:
        # tokenise the sentence with identify-idioms -pipeline.
        tokens = iip(sent)
        # tokenise and get the idioms only
        idiom = [token.lemma_ for token in tokens if token._.is_idiom]
        print("{} --> {}".format(sent, idiom))


if __name__ == '__main__':
    main()
