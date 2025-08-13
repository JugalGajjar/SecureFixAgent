import subprocess

def unsafe():
    user_input = input("Enter command: ")
    # Use subprocess.run with shell=False to prevent command injection
    subprocess.run(user_input, check=True, shell=False)