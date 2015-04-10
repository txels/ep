import semver


def match(version, spec_string):
    """
    Match a version to a specification string.

    :param spec_string:
        A comma-separated list of semver matchers, e.g. ">=2.7.0,<3.0.0"

    """
    specs = map(str.strip, spec_string.split(','))
    return all(map(lambda s: semver.match(version, s), specs))
