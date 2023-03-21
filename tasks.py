from invoke import task


@task
def start(ctx):
    pass


@task
def test(ctx):
    ctx.run("cd ./src && pytest . && cd ..", pty=True)


@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)
