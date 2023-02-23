import re


def validate_email(s):
    return re.match("^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", s)


def emoji(s):
    raise NotImplemented
