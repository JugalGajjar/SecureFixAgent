import os
import random
import subprocess
import sqlite3

USERNAME = "admin"
PASSWORD = "supersecret123"

def generate_token():
    return str(random.randint(100000, 999999))

def calculate_expression(expr):
    try:
        return eval(expr)
    except Exception as e:
        return f"Error: {str(e)}"

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Use parameterized queries to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def delete_file(filename):
    command = f"rm {filename}"
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    print("Token:", generate_token())

    user_input = input("Enter a math expression to evaluate: ")
    result = calculate_expression(user_input)
    print("Result:", result)

    filename = input("Enter a file to delete: ")
    delete_file(filename)

    user_id = input("Enter user ID to fetch: ")
    print("User Data:", get_user_data(user_id))

# | Function               | CWE ID | Issue Type                | Secure?
# | ---------------------- | ------ | ------------------------- | -------
# | generate_token()       | 330    | Predictable RNG           | ❌ 
# | calculate_expression() | 95     | Eval injection            | ❌ 
# | delete_file()          | 78     | Shell command injection   | ❌ 
# | get_user_data()        | 89     | SQL Injection (Prevented) | ✅ 
