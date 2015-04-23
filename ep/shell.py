from __future__ import print_function
from functools import wraps
import os
import signal
import subprocess
import sys

from .compat import basestring  # NOQA


COLORED = "\033[{format}m{message}\033[0m"


class Color16:  # NOQA
    red = 31
    error = red
    green = 32
    success = green
    yellow = 33
    warning = yellow
    blue = 34
    purple = 35
    cyan = 36
    white = 37
    neutral = white


class Color256:  # NOQA
    red = 196
    error = red
    green = 40
    success = green
    yellow = 220
    warning = yellow
    blue = 27
    purple = 93
    cyan = 51
    white = 231
    neutral = white


class Style:  # NOQA
    plain = 0
    bold = 1
    italics = 3
    underlined = 4
    ansi256 = 5


def ansi_print(message, fmt):
    """
    Print a colored message
    """
    print(COLORED.format(message=message, format=fmt))


def output(message, color='neutral', style=Style.plain):
    """
    Print a colored message
    """
    if style == Style.ansi256:
        ANSI_CODE = "38;{0};{1}"
        Color = Color256
    else:
        ANSI_CODE = "{0};{1}"
        Color = Color16
    if isinstance(color, basestring):
        color = getattr(Color, color)
    ansi_code = ANSI_CODE.format(style, color)
    ansi_print(message, ansi_code)


def error(message):
    """
    Print an error message

    TODO: be able to deal with custom stdout and stderr
    """
    output(message, color='error', style=Style.bold)


def success(message):
    output(message, color='success')


def warning(message):
    output(message, color='warning')


def abort(message=None, status=1):
    """
    Generate error message and exit with an error status
    """
    error(message or "FAILED")
    exit(status)


def graceful_ctrlc(fun):
    """
    Decorator to gracefully deal with CTRL-C

    Instead of a stack trace it will abort with the standard bash return code
    for CTRL-C.

    """
    CTRLC_RETURN_CODE = 128 + signal.SIGINT

    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except KeyboardInterrupt:
            abort("<Ctrl-C> Aborting...", status=CTRLC_RETURN_CODE)
    return wrapper


class _AttributeString(str):
    """
    Simple string subclass to allow arbitrary attribute access.
    """
    @property
    def stdout(self):
        return str(self)


def run(command, capture=False, shell=None):
    """
    Run a command on the local system.

    A convenient wrapper around subprocess.Popen, borrowed from Fabric's
    `local` (http://www.fabfile.org/) and simplified a bit.

    ``shell`` is passed directly to `subprocess.Popen
    <http://docs.python.org/library/subprocess.html#subprocess.Popen>`_'s
    ``execute`` argument (which determines the local shell to use.)  As per the
    linked documentation, on Unix the default behavior is to use ``/bin/sh``,
    so this option is useful for setting that value to e.g.  ``/bin/bash``.

    `run` is not currently capable of simultaneously printing and capturing
    output. The ``capture`` kwarg allows you to switch between printing and
    capturing as necessary, and defaults to ``False``.

    When ``capture=False``, the local subprocess' stdout and stderr streams are
    hooked up directly to your terminal.

    When ``capture=True``, you will not see any output from the subprocess in
    your terminal, but the return value will contain the captured
    stdout/stderr.

    In either case, this return value exhibits the ``return_code``,
    ``stderr``, ``failed``, ``succeeded`` and ``command`` attributes.

    """
    dev_null = None
    if capture:
        out_stream = subprocess.PIPE
        err_stream = subprocess.PIPE
    else:
        dev_null = open(os.devnull, 'w+')
        # Non-captured, hidden streams are discarded.
        out_stream = sys.stdout
        err_stream = sys.stderr
    try:
        cmd_arg = [command]
        p = subprocess.Popen(cmd_arg, shell=True, stdout=out_stream,
                             stderr=err_stream, executable=shell,
                             close_fds=True)
        (stdout, stderr) = p.communicate()
    finally:
        if dev_null is not None:
            dev_null.close()

    # Handle error condition (deal with stdout being None, too)
    out = _AttributeString(stdout.strip() if stdout else "")
    err = _AttributeString(stderr.strip() if stderr else "")
    out.command = command
    out.failed = False
    out.return_code = p.returncode
    out.stderr = err
    if p.returncode != 0:
        out.failed = True
        msg = "Error (return code {0}) while executing '{1}'".format(
            p.returncode, command)
        error(message=msg)  # , stdout=out, stderr=err)
    out.succeeded = not out.failed
    return out
