import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("init")
def cmd_init() -> None:
    """최초 설정 + global hook 자동 설치"""
    from gittchi.commands.init import run
    run()


@app.command("hello")
def cmd_hello() -> None:
    """펫과 대화"""
    from gittchi.commands.hello import run
    run()


@app.command("status")
def cmd_status() -> None:
    """펫 상태 확인"""
    from gittchi.commands.status import run
    run()


@app.command("react", hidden=True)
def cmd_react(
    dry_run: bool = typer.Option(False, "--dry-run", help="hook 없이 반응 테스트"),
) -> None:
    from gittchi.commands.react import run
    run(dry_run=dry_run)
