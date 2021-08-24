import os


def change_dir(path):
    assert os.path.exists(path), "Path provided does not exists {}".format(path)
    os.chdir(path)