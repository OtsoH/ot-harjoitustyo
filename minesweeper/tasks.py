import sys
import webbrowser
from pathlib import Path
from invoke import task

@task
def start(ctx):
    pty = sys.platform != "win32"
    python_command = "py" if sys.platform == "win32" else "python3"
    ctx.run(f"{python_command} main.py", pty=pty)

@task
def coverage(ctx):
    pty = sys.platform != "win32"
    ctx.run(
        "coverage run --branch --include='board.py,piece.py' --omit='tests/*,__init__.py,tasks.py,game.py,main.py' -m pytest tests/",
        pty=pty
    )

@task()
def coverage_report(ctx):
    pty = sys.platform != "win32"
    ctx.run("coverage html", pty=pty)

    htmlcov = Path('htmlcov').absolute()
    index_file = htmlcov / 'index.html'
    webbrowser.open(f'file://{index_file}')

@task()
def test(ctx):
    pty = sys.platform != "win32"
    ctx.run("pytest tests/", pty=pty)

@task()
def lint(ctx):
    pty = sys.platform != "win32"
    ctx.run("pylint board.py game.py main.py piece.py", pty=pty)

@task()
def coverage_check(ctx):
    coverage(ctx)
    coverage_report(ctx)