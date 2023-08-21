"""Define all the commands interface of the cli"""
import json
import os
import re

import click
import pyperclip
import structlog

from keecli.database import KeePassDatabase

logger = structlog.get_logger()


def parse_names(name: str) -> (str, str):
    """Helper function to separate group and entry names."""
    pattern = r"^([^/]*)/?([^/]+)$"
    result = re.search(pattern, name)
    return result.group(1, 2)


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """Interface to your KeePass database."""
    ctx.ensure_object(dict)

    # Instanciate the database from the config
    filepath = os.path.abspath(os.path.expanduser(os.getenv("KEECLI_DB")))
    ctx.obj["db"] = KeePassDatabase(filepath, os.getenv("KEECLI_PASSWORD"))


@cli.command()
@click.pass_context
@click.option(
    "--password/--no-password",
    default=False,
    required=False,
    help="Show the password in plain text (default: false).",
)
@click.argument("name", type=click.STRING)
def get(ctx: click.Context, name: str, password: bool):
    """Get details for an entry.

    Group can be specify with / e.g. Email/gmail will look for the entry named
    gmail within the Email group. Note that either the group name or the entry name
    can be partial and are case insensitive, which means it could match multiple
    entries. If multiple entries are found, only the first one is returned. If it
    is the incorrect one, you will need to provide a more accurate name.
    """
    db = ctx.obj["db"]

    group_name, entry_name = parse_names(name)
    entry = db.get_entry(entry_name, group_name)

    if not entry:
        click.echo("No matching entry found")
        ctx.exit(1)

    click.echo(json.dumps(entry.to_dict(show_password=password)))
    ctx.exit()


@cli.command("pass")
@click.pass_context
@click.option(
    "--group",
    "-g",
    type=click.STRING,
    required=False,
    default=None,
    help="The group where to look for the entry.",
)
@click.option(
    "--copy/--no-copy",
    default=False,
    required=False,
    help="Copy the password to the clipboard (default: false).",
)
@click.argument("name", type=click.STRING)
def password(ctx: click.Context, name: str, group: str, copy: str):
    """Get the password for an entry.

    If multiple passwords are found, the --copy option is ignored.
    """
    db = ctx.obj["db"]
    entries = db.get_entry(name, group=group)

    if len(entries) > 1:
        click.confirm("Multiple passwords found, do you want to continue?", abort=True)

    if len(entries) == 0:
        click.echo("No mathcing entry found")
        ctx.exit(1)

    pwd = entries[0].password
    if copy:
        pyperclip.copy(pwd)
    click.echo(pwd)
