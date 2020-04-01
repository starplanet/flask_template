import click
from flask import current_app
from flask.cli import with_appcontext


@click.command('shell', short_help='Starts an interactive shell in an app context.')
@with_appcontext
def shell_command():
    ctx = current_app.make_shell_context()
    try:
        from IPython import start_ipython
        start_ipython(argv=(), user_ns=ctx)
    except ImportError:
        from code import interact
        interact(local=ctx)
