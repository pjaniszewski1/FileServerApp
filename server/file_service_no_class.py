import os


def change_dir(path):
	assert os.path.exists(path), 'Directory {} is not found'. format(path)
	os.chdir(path)