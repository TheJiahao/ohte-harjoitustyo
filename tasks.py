from invoke import task


@task
def start(ctx):
    pass


@task
def test(ctx):
    ctx.run("cd ./src && pytest . && cd ..", pty=True)


@task
def coverage_report(ctx):
    ctx.run("cd ./src && coverage run --branch -m pytest . && cd ..", pty=True)
    ctx.run("coverage html", pty=True)
