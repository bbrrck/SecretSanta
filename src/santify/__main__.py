# ruff: noqa: D100

import argparse
import sys
from pathlib import Path

from santify import generate_mapping_and_send_email
from santify.logging import logger


def main() -> None:
    """Run the main function."""
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
    parser.add_argument(
        "-y",
        "--skip-confirm",
        action="store_true",
        help="Do not prompt for confirmation",
    )

    args = parser.parse_args()

    if not args.skip_confirm:
        logger.info("Running script with the following arguments:")
        logger.info(f"-- Config file: {args.config_file}")
        logger.info(f"-- Output directory: {args.outdir}")
        logger.info(f"-- Debug mode? {args.debug}")
        logger.info(f"-- Send emails? {args.email}")
        logger.info(f"-- Encrypt output? {args.encrypt}")
        logger.info("Are you sure you want to continue? (y/n)")
        while True:
            answer = input()
            if answer.lower() in ["y", "yes"]:
                logger.info("Continue running...")
                break
            if answer.lower() in ["n", "no"]:
                logger.info("Exiting...")
                sys.exit(0)
            logger.info("Invalid input. Please enter 'y' or 'n'.")

    generate_mapping_and_send_email(
        config_file=args.config_file,
        output_dir=args.outdir,
        encrypt=args.encrypt,
        send_email=args.email,
        debug_mode=args.debug,
    )


if __name__ == "__main__":
    main()
