![GitHub release (with filter)](https://img.shields.io/github/v/release/leoperard/keecli)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/leoperard/keecli/release.yaml)

# KeeCLI

`KeeCLI` is a command line interface to interact with KeePass databases. It takes a lot of inspiration from [`pass`](https://www.passwordstore.org/),
so if you used it in the past you will find a lot of similarities with `KeeCLI`.

## Installation

Using pip:

```bash
pip install keecli
```

From source:
```bash
git clone https://github.com/leoperard/keecli
cd keecli
pip install poetry # if not already present
poetry install
```

## Configuration

`KeeCLI` expects 2 environment variables for the database file and the password associated.

```bash
export KEECLI_DB="/path/to/my/db.kdbx"
export KEECLI_PASSWORD="higly-secured-password"
```

Note that `KeeCLI` does not store your password. It only read it from the environment variable to open the database.

## Commands

### Get an entry

Get all the details of an entry in json format. If multiple entries are found, the result will be a list of entries.
You can reduce the scope of the search by specifying a group. All names are fuzzy matched. By default, the password
will be displayed with `*` characters, you can use the `--password` option to print it in plain text.

```bash
keecli get --help
Usage: keecli get [OPTIONS] NAME

  Get details for an entry.

Options:
  -g, --group TEXT            The group where to look for the entry.
  --password / --no-password  Show the password in plain text (default:
                              false).
  --help                      Show this message and exit.
```
