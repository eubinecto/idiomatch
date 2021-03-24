from service import build_iip


def main():
    mip = build_iip()
    sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."

    for token in mip(sent_1):
        print(token.sentiment)


if __name__ == '__main__':
    main()
