from identify_idioms.builders import IdiomsBuilder
from identify_idioms.paths import IDIOMS_TXT


def main():
    idioms = IdiomsBuilder().construct()
    with open(IDIOMS_TXT, 'w') as fh:
        for idiom in idioms:
            fh.write(idiom + "\n")


if __name__ == '__main__':
    main()
