from idiomatch.builders import IdiomsBuilder


def main():
    idioms = IdiomsBuilder().construct()
    with open("idioms.txt", "w") as fh:
        for idiom in idioms:
            fh.write(idiom + "\n")


if __name__ == '__main__':
    main()
