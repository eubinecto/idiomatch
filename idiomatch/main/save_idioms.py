from idiomatch.builders import IdiomsBuilder
from idiomatch.paths import IDIOMS_TXT


def main():
    idioms = IdiomsBuilder().construct()
    with open(IDIOMS_TXT, 'w') as fh:
        for idiom in idioms:
            fh.write(idiom + "\n")


if __name__ == '__main__':
    main()
