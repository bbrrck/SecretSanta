# ruff: noqa: D100

import argparse
from pathlib import Path

from santify import generate_mapping_and_send_email

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="santify")
    parser.add_argument("config_file", type=Path, help="Path to the config file")
    parser.add_argument("-o", "--outdir", type=Path, help="Output directory")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "-m",
        "--email",
        action="store_true",
        help="Enable sending emails",
    )
    parser.add_argument(
        "-e",
        "--encrypt",
        action="store_true",
        help="Encrypt the output",
    )
    args = parser.parse_args()

    generate_mapping_and_send_email(
        config_file=args.config_file,
        output_dir=args.outdir,
        encrypt=args.encrypt,
        send_email=args.email,
        debug_mode=args.debug,
    )
