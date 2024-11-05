# Santify: Secret Santa Mapping Generator

Santa gift exchange organizer that automatically assigns givers and recipients while respecting exclusion rules.

## Installation

Using [uv](https://github.com/astral-sh/uv):

```sh
uv venv
source .venv/bin/activate
uv sync
```

## Usage

Run as command line script:

```sh
python -m santify config.json
```

Additional command line arguments:

```sh
usage: santify [-h] [-o OUTDIR] [-d] [-m] [-e] config_file

positional arguments:
  config_file           Path to the config file

options:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir OUTDIR
                        Output directory
  -d, --debug           Enable debug mode
  -m, --email           Enable sending emails
  -e, --encrypt         Encrypt the output
```
