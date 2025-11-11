# ruff: noqa: D100

import argparse
from pathlib import Path

from santify import generate_mapping_and_send_email
from santify.logging import console


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

    console.info("Running script with the following arguments:")
    console.info(f"• Config file     : [blue]{args.config_file}")
    console.info(f"• Output directory: [blue]{args.outdir}")
    console.info(f"• Debug mode?       {args.debug}")
    console.info(f"• Send emails?      {args.email}")
    console.info(f"• Encrypt output?   {args.encrypt}")

    confirm = console.confirm("Continue?") or args.skip_confirm
    if not confirm:
        console.info("Aborting script.")
        return

    generate_mapping_and_send_email(
        config_file=args.config_file,
        output_dir=args.outdir,
        encrypt=args.encrypt,
        send_email=args.email,
        debug_mode=args.debug,
    )


if __name__ == "__main__":
    main()
