# Sprawdzenie, czy niezbędne bilioteki są zainstalowane
import sys, subprocess, pkg_resources

class Biblioteki():
    def __init__(self):
        required = {'numpy', 'simple-term-menu'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed

        if missing:
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
