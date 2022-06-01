# Miscellaneous functions
import os
import sys
import psutil
import platform


# Experimental: This is a custom exit handler which can be used to replace any direct calls to sys.exit()
# Allows the compiled program to pause before closing the window when run directly from explorer.exe in Windows...
# There is no need to pause program if run from within PowerShell or the Command Prompt terminal
def system_exit(exit_code):
    # Determine parent process name on Windows
    # Returns: pycharm64.exe, explorer.exe, powershell.exe, or cmd.exe, etc...
    parent = psutil.Process(os.getppid()).parent().name()

    # If the direct parent process is explorer.exe: pause before exiting the program to show or browse results
    # There is no need to pause if run from within powershell.exe, cmd.exe, or pycharm64.exe, etc...
    if platform.system() == "Windows" and parent == "explorer.exe":
        input('\nPress Enter to continue...')

    sys.exit(exit_code)


if __name__ == '__main__':
    system_exit(0)
