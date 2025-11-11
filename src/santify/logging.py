# ruff: noqa: D100 D101 D102 D107
from enum import StrEnum

from rich.console import Console
from rich.prompt import Confirm


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class SantifyConsole:
    def __init__(self) -> None:
        self.console = Console()

    def log(self, level: LogLevel, message: str) -> None:
        match level:
            case LogLevel.DEBUG:
                style = "[blue]"
            case LogLevel.INFO:
                style = ""
            case LogLevel.WARNING:
                style = "[yellow]"
            case LogLevel.ERROR:
                style = "[red]"
            case LogLevel.SUCCESS:
                style = "[green]"
        self.console.log(f"{style}{message}")

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        self.log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)

    def success(self, message: str) -> None:
        self.log(LogLevel.SUCCESS, message)

    def confirm(self, message: str) -> bool:
        return Confirm.ask(message)


console = SantifyConsole()
