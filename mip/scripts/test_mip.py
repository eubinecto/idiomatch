from loaders import MIPLoader
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mip_pkl_path", type=str,
                        help="path to the pickle binary of idiom_matcher")
    args = parser.parse_args()
    mip_pkl_path = args.mip_pkl_path
    mip_loader = MIPLoader(path=mip_pkl_path)
    mip = mip_loader.load()
    doc = mip("It's not the end of the world, is it?")

    for token in doc:
        print(token.lemma_)


if __name__ == '__main__':
    main()
