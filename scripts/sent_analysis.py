from service import build_mip


def main():
    mip = build_mip()
    sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."

    for token in mip(sent_1):
        print(token.sentiment)


if __name__ == '__main__':
    main()
