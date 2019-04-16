import argparse
from conf import validate_args
from formatter import format_bib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", required=False, type=str)
    parser.add_argument("--input", "-i", required=True, type=str)
    parser.add_argument("--inplace", "-r", required=False, action="store_true")
    parser.add_argument("--sort", "-s", required=False, type=str, default='en',
                        help='sort by which order, valid options are: "en"(default) (entry then name), "ne" (name then entry)')
    parser.add_argument("--space", "-w", required=False, type=int, default=2)
    parser.add_argument("--merge", "-m", required=False,
                        action="store_true", help="try to merge similar entries")
    parser.add_argument("--verbose", "-v", required=False, action="store_true")

    args = parser.parse_args()
    config = validate_args(args)
    format_bib(config)


if __name__ == "__main__":
    main()
