import nox

nox.options.default_venv_backend = "uv"


@nox.session
def typing(session: nox.Session) -> None:
    session.install("nbqa", "mypy", "globus-sdk >= 4, < 5")
    session.run("nbqa", "mypy", "Platform_Introduction.ipynb")
