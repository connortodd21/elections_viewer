import os
import subprocess

def getGitRoot() -> str:
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# will work if filename is included in path
def createDirectoryIfNotExists(path: str) -> None:
    directory = os.path.dirname(path)

    # Create directory if it doesn't exist
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def createFile(path: str) -> None:
    open(path, 'w').close()