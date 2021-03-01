import re

def parseDuration(string):
    """
    Parses 'NdNhNmNs' formatted string.
    Returns integer seconds.
    """

    regex = '^(([0-9]*)d)?(([0-9]*)h)?(([0-9]*)m)?(([0-9]*)s)?$'

    result = re.findall(regex, string)

    if len(result) == 0:
        raise ValueError

    seconds = int(result[0][1] if result[0][1] != '' else 0) * 86400 + \
              int(result[0][3] if result[0][3] != '' else 0) * 3600 + \
              int(result[0][5] if result[0][5] != '' else 0) * 60 + \
              int(result[0][7] if result[0][7] != '' else 0)

    return seconds

