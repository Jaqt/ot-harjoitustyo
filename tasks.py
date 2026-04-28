from invoke import task

@task
def start(ctx):
    """Käynnistää sovelluksen.
    """

    ctx.run("python3 src/index.py", pty=True)

@task
def test(ctx):
    """Käynnistää testit
    """

    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    """Käynnistää testit ja kerää testikattavuustiedot.
    """

    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    """Luo html testikattavuusraportin
    """

    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    """Tarkistaa koodin tyylivirheet pylintillä.
    """

    ctx.run("pylint src", pty=True)

@task
def format(ctx):
    """Muotoilee koodin autopep8:lla.
    """

    ctx.run("autopep8 --in-place --recursive src", pty=True)
