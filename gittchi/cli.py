import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("init")
def cmd_init() -> None:
    """최초 설정 + global hook 자동 설치"""
    from gittchi.commands.init import run
    run()


@app.command("hello")
def cmd_hello(
    message: str = typer.Argument(None, help="바로 전달할 메시지 (없으면 대화 모드 진입)"),
) -> None:
    """펫과 대화. 메시지를 인수로 주면 단발 응답, 없으면 대화 모드"""
    from gittchi.commands.hello import run
    run(message=message)


@app.command("status")
def cmd_status() -> None:
    """펫 상태 확인"""
    from gittchi.commands.status import run
    run()


@app.command("petinfo")
def cmd_petinfo() -> None:
    """내 개발자 프로필 + 포트폴리오 자동 생성"""
    from gittchi.commands.petinfo import run
    run()


@app.command("config")
def cmd_config(
    model: str = typer.Option(None, "--model", help="모델 변경 (예: gpt-4o-mini)"),
    api_key: str = typer.Option(None, "--api-key", help="API 키 변경"),
    pet_type: str = typer.Option(None, "--pet-type", help="펫 종류 변경 (dog|cat|rabbit|bear)"),
) -> None:
    """현재 설정 확인 또는 모델/API 키/펫 종류 변경"""
    from gittchi.commands.config_cmd import run
    run(model=model, api_key=api_key, pet_type=pet_type)


@app.command("sync")
def cmd_sync() -> None:
    """내 레벨·XP를 글로벌 랭킹에 등록 (opt-in)"""
    from gittchi.commands.sync import run
    run()


@app.command("rank")
def cmd_rank() -> None:
    """글로벌 랭킹 확인"""
    from gittchi.commands.rank import run
    run()


@app.command("attach")
def cmd_attach() -> None:
    """현재 레포에 추가로 hook 설치 (global hook 미적용 환경용)"""
    from gittchi.commands.attach import run
    run()


@app.command("uninstall")
def cmd_uninstall() -> None:
    """작별 인사 후 Gittchi 삭제"""
    from gittchi.commands.uninstall import run
    run()


@app.command("react", hidden=True)
def cmd_react(
    dry_run: bool = typer.Option(False, "--dry-run", help="hook 없이 반응 테스트"),
) -> None:
    from gittchi.commands.react import run
    run(dry_run=dry_run)
