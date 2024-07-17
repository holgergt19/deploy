import subprocess

with open('requirements.txt', 'w') as f:
    subprocess.call(['pip', 'freeze'], stdout=f)

with open('requirements.txt') as f:
    packages = f.readlines()

packages = [pkg.split('==')[0] for pkg in packages if '==' in pkg and not pkg.startswith('@')]

subprocess.call(['pip', 'uninstall', '-y'] + packages)
