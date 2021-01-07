from builders import MIPBuilder
from config import MIP_MODEL_PATH


def main():
    mip_builder = MIPBuilder()
    mip_builder.construct()
    mip_builder.mip.to_disk(MIP_MODEL_PATH)


if __name__ == '__main__':
    main()
