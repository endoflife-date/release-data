"""Tracks subprocesses (and other killable resources, e.g. Playwright browsers) started by this
program, so that they can all be forcibly terminated in one go, e.g. when the user hits Ctrl-C
while products are being updated in parallel (see update-release-data.py).

subprocess.run() itself doesn't offer a way to know from the outside which child processes are
currently running, and once a process is killed via a plain SIGINT sent to the terminal's
foreground process group, orphaned Playwright/chromium processes have been observed to survive
because they are managed by their own driver process. Routing every subprocess invocation through
`run()` below, and registering/unregistering it for the duration of its execution, lets
`kill_all()` reliably clean everything up regardless of which thread started it.
"""
import logging
import subprocess
import threading
from typing import Callable

_lock = threading.Lock()
_killables: set[Callable[[], None]] = set()


def register(killer: Callable[[], None]) -> None:
    """Registers a callable that forcibly stops a running subprocess/resource, so that it is
    invoked by kill_all()."""
    with _lock:
        _killables.add(killer)


def unregister(killer: Callable[[], None]) -> None:
    with _lock:
        _killables.discard(killer)


def kill_all() -> None:
    """Best-effort termination of every subprocess/resource currently registered (e.g. on Ctrl-C)."""
    with _lock:
        killables = list(_killables)

    for killer in killables:
        try:
            killer()
        except Exception:
            logging.exception("failed to kill a subprocess/resource while shutting down")


def run(args: list[str], timeout: float = None, check: bool = False, capture_output: bool = False,
        **kwargs: any) -> subprocess.CompletedProcess:
    """Drop-in replacement for subprocess.run() that registers the child process while it runs,
    so that it can be killed by kill_all() (e.g. if the program is interrupted with Ctrl-C)."""
    if capture_output:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE

    process = subprocess.Popen(args, **kwargs)
    register(process.kill)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        raise
    except BaseException:
        process.kill()
        raise
    finally:
        unregister(process.kill)

    completed = subprocess.CompletedProcess(process.args, process.poll(), stdout, stderr)
    if check:
        completed.check_returncode()
    return completed
