from __future__ import print_function
import os
import subprocess
import sys


def error(message, stdout, stderr):
    """
    Print an error message

    TODO: properly deal with stdout and stderr, and apply formatting/colors
    """
    print(message)


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
        msg = "run error (return code {0}) while executing '{1}'".format(
            p.returncode, command)
        error(message=msg, stdout=out, stderr=err)
    out.succeeded = not out.failed
    return out
