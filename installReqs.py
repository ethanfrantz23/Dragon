import subprocess

with open('controller-requirements.txt', 'r') as file:
    for line in file.read().splitlines():
        subprocess.run(['mpremote','mip','install',line])