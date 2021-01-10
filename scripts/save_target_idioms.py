from loaders import IdiomsLoader
from config import TARGET_IDIOMS_TXT_PATH, SLIDE_TSV_PATH


def main():
    target_idioms = IdiomsLoader(SLIDE_TSV_PATH).load(target_only=True)
    with open(TARGET_IDIOMS_TXT_PATH, 'w') as fh:
        for idiom in target_idioms:
            fh.write(idiom.lower() + "\n")


if __name__ == '__main__':
    main()
