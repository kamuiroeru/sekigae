#
from subprocess import run

run(['rm', '-rf', 'sekigae.egg-info', 'dist', 'build'])
run(['python', 'setup.py', 'sdist', 'bdist_wheel'])
run(['twine', 'upload', '--verbose', '--repository', 'pypi', 'dist/*'])
