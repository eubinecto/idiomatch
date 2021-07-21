
from idiomatch.builders import IdiomPatternsBuilder


def main():
    patterns = [dict(), dict(), dict()]
    inserted = IdiomPatternsBuilder.insert_slop(patterns, 3)
    print(inserted)
    print(len(inserted))


if __name__ == '__main__':
    main()

