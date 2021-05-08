
from identify_idioms.service import build_iip


def main():
    iip = build_iip()
    sents = [
        # modification
        "grasp at straws",
        "Vologsky grasped desperately at the floating straw.",
        # open slot
        "Now you get frightened and keep me at arm's length!",
        "They preferred to persist in Piłsudski's strategy of keeping both Germans and Russians at arm's length.",
        # passivisation
        "The case could open the floodgates for thousands of similar claims worldwide.",
        "And with Wright gone, the floodgates were opened."
    ]
    for sent in sents:
        tokens = iip(sent)
        # filter idioms
        idiom = [
            token.text
            for token in tokens
            if token._.is_idiom
        ]
        print(idiom)


if __name__ == '__main__':
    main()
