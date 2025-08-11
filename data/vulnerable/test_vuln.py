import subprocess

def unsafe():
    user_input = input("Enter command:")
    subprocess.call(user_input, shell=True)

unsafe()
