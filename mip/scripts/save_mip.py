from config import MIP_PATH, IDIOM_MATCHER_PKL_CURR_PATH
from mip.builders import MIPBuilder


def main():
    # build the pipeline and save it to disk.
    mip_builder = MIPBuilder()
    mip_builder.construct(IDIOM_MATCHER_PKL_CURR_PATH)
    mip_builder.mip.to_disk(MIP_PATH)


if __name__ == '__main__':
    main()
