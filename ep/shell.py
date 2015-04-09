from fabric.api import hide, local


def run(*args, **kwargs):
    with hide('running'):
        local(*args, **kwargs)
