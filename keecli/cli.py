"""Define all the commands interface of the cli"""
import json
import os

import click
import pyperclip
import structlog

from keecli.database import KeePassDatabase

logger = structlog.get_logger()


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
    "--group",
    "-g",
    type=click.STRING,
    required=False,
    default=None,
    help="The group where to look for the entry.",
)
@click.option(
    "--password/--no-password",
    default=False,
    required=False,
    help="Show the password in plain text (default: false).",
)
@click.argument("name", type=click.STRING)
def get(ctx: click.Context, name: str, group: str, password: bool):
    """Get details for an entry."""
    db = ctx.obj["db"]
    entries = db.get_entry(name, group=group)

    if len(entries) == 0:
        click.echo("No matching entry found")
        ctx.exit(1)

    if len(entries) == 1:
        click.echo(json.dumps(entries[0].to_dict(show_password=password)))
        ctx.exit()

    click.echo(json.dumps([entry.to_dict(show_password=password) for entry in entries]))
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
