import pathlib
import re


def load_regexes(regex_file: pathlib.Path):
    """Load regular expressions from file of label \t regex"""
    regexes = []
    with open(regex_file) as fh:
        for line in fh:
            if not line.strip():
                continue
            label, regex = line.split('\t')
            regexes.append((
                label,
                re.compile(r'\W*'.join(regex.split()), re.IGNORECASE),
            ))
    return regexes
