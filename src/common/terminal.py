import logging

# ANSI SGR color codes used when running interactively in a terminal.
ANSI_RESET = "\033[0m"
ANSI_COLOR_BY_LEVEL = {
    logging.DEBUG: "\033[2m",     # dim
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",    # red
    logging.CRITICAL: "\033[31m", # red
}


class TerminalColorLogFormatter(logging.Formatter):
    """Colors log lines using ANSI escape codes, for a nicer experience when running interactively in a
    terminal. Intended to be used only when output is attached to an actual terminal (e.g. based on
    sys.stdout.isatty()), so that piped/redirected output is not polluted with escape codes.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003 - logging.Formatter protocol method
        message = super().format(record)

        color = ANSI_COLOR_BY_LEVEL.get(record.levelno)
        if not color:
            return message

        return f"{color}{message}{ANSI_RESET}"
