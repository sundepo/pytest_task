import argparse
import os
import sys
from typing import Literal

__doc__ = """Tool for converting a file from binary (.bin) format to text (.txt)"""
__version__ = "1.0.0"


def byte_to_str(
    byte: bytes,
    type: Literal["bin", "hex"],
    endian: Literal["little", "big"],
    depth: int,
):
    number = int.from_bytes(byte, endian)

    if type == "bin":
        str_type = "b"
    elif type == "hex":
        str_type = "x"
        depth //= 4

    str_format = "0" + str(depth) + str_type
    string = format(number, str_format)

    return string.upper()


def main() -> int:
    class Formatter(argparse.RawDescriptionHelpFormatter): ...

    def depth_validation(depth: str) -> int:
        depth = int(depth)
        if depth % 8 == 0:
            return depth
        else:
            print("Error: Depth must be a multiple of 8!")
            raise ValueError

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=Formatter)

    parser.add_argument(
        "-b",
        "--binary",
        required=True,
        metavar="filename",
        dest="bin_file",
        help="Input binary file",
    )
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        metavar="filename",
        dest="txt_file",
        help="Output text file",
    )
    parser.add_argument(
        "-x",
        "--x",
        required=True,
        choices=["bin", "hex"],
        dest="out_type",
        help="Output data format",
    )
    parser.add_argument(
        "-e",
        "--endian",
        choices=["little", "big"],
        default="little",
        help="Endian in input file (default: little)",
    )
    parser.add_argument(
        "-d",
        "--depth",
        metavar="depth",
        type=depth_validation,
        default=32,
        help="Input data bit depth, multiple of 8 (default: 32)",
    )
    parser.add_argument(
        "-w",
        "--words",
        metavar="words",
        type=int,
        default=256,
        help="Number of lines in output file (default: 256)",
    )
    parser.add_argument(
        "-f",
        "--fill",
        choices=["0", "1"],
        default="0",
        help="Filling in missing data (default: 0)",
    )
    parser.add_argument(
        "-l",
        "--line",
        choices=["n", "r", "rn"],
        default="n",
        help="Select line ending (default: n)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )

    args = parser.parse_args()

    if os.path.isfile(args.bin_file) is False:
        print(f"Error: {args.bin_file} is not an existing regular file!")
        return 1

    if args.line == "n":
        end_line = "\n"
    elif args.line == "r":
        end_line = "\r"
    elif args.line == "rn":
        end_line = "\r\n"

    with open(args.bin_file, "rb") as bin_file:
        with open(args.txt_file, "w", newline=end_line) as txt_file:
            line_count = 0

            while True:
                bin_content = bytearray(bin_file.read(args.depth // 8))

                if 0 < len(bin_content) < (args.depth // 8):
                    if args.fill == "1":
                        bin_content = bin_content.ljust(args.depth // 8, b"\xFF")

                if not bin_content:
                    if line_count >= (args.words):
                        break
                    elif line_count < (args.words):
                        if args.fill == "1":
                            bin_content = bin_content.ljust(args.depth // 8, b"\xFF")

                line_count += 1

                string = byte_to_str(
                    bin_content, args.out_type, args.endian, args.depth
                )
                txt_file.write(f"{string}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
