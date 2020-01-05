import os


def get_abs_path(filepath):
    if not os.path.isfile(filepath):
        raise ValueError('The file does not exist')

    return os.path.abspath(filepath)


def get_bin_directory():
    return os.path.join(os.path.expanduser('~'), '.bin')
