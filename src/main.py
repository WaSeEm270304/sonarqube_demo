# vulnerable_test.py
import os
import subprocess
import hashlib
import pickle
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/exec')
def dangerous_exec():
    # SQUID: S4721 - OS Command Injection (Critical)
    user_input = request.args.get('cmd')
    subprocess.call(user_input, shell=True)  # Extremely dangerous

    # SQUID: S4829 - Command Injection via subprocess (Critical)
    subprocess.Popen(user_input, shell=True)

    return "Executed"

@app.route('/hash')
def weak_hash():
    # SQUID: S2257 - Use of weak cryptographic hash (MD5/SHA1)
    password = request.args.get('pass', 'secret')
    hashed = hashlib.md5(password.encode()).hexdigest()  # Weak algorithm
    return hashed

@app.route('/upload', methods=['POST'])
def insecure_deserialization():
    # SQUID: S2631 - Insecure deserialization with pickle (Critical)
    data = request.data
    obj = pickle.loads(data)  # Very dangerous - RCE possible
    return str(obj)

@app.route('/download')
def no_ssl_verification():
    # SQUID: S4426 - Disable SSL certificate verification (Security Hotspot → Critical in many rulesets)
    url = request.args.get('url')
    response = requests.get(url, verify=False)  # NOSONAR can be added, but still flagged
    return response.text

def hardcoded_credentials():
    # SQUID: S2068 - Hard-coded password (Critical)
    db_password = "admin123!@#"
    api_key = "AKIAIOSFODNN7EXAMPLE"  # Looks like AWS key

    # SQUID: S4792 - Logging sensitive information
    print(f"Connecting with password: {db_password}")

def insecure_random():
    # SQUID: S2245 - Using cryptographically weak pseudo-random generator
    import random
    token = str(random.randint(100000, 999999))
    return token

# SQUID: S4487 - Unused private variable (Code Smell) + name starts with __ (mangling)
__unused_secret = "supersecret"

if __name__ == "__main__":
    # SQUID: S4507 - Running Flask in debug mode in production (Critical)
    app.run(debug=True, host='0.0.0.0', port=5000)
