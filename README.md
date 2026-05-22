# hackable

An application that lets you takes notes. However, beware since it is easily breachable by cybercriminals. The security flaws are intentionally created to demonstrate cybersecurity risks from the [OWASP Top 10 (2021)](https://owasp.org/Top10/2021/). Feel free to deploy it in production at your own risk ;D

>**DO NOT DEPLOY IN REAL PRODUCTION.**

## Flaws Included
- A01: Broken Access Control (IDOR)
- A02: Cryptographic Failures (plaintext password)
- A03: Injection (SQL injection)
- A05: Security Misconfiguration (DEBUG = True)
- CSRF Flaw

## Installation

- Ensure you have Python 3.10+

### For Windows Computers

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### For macOS and Linux Computers

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## How to use this application

1. Open `http://127.0.0.1:8000/register/` and create account.
2. Log into the application and take some notes.
3. Use a second browser session (incognito works) with a different account to test IDOR and CSRF flaws.
4. Use the search bar with a payload such as `' OR 1=1 --` to test SQL injection attacks.
5. Visit any nonexistent URL (e.g. `/doesnotexist/`) to trigger the `DEBUG = True` error page exposing private information.

## Screenshots

There are screenshots of each flaw (before and after being fixed) present in the [`screenshots/`](screenshots/) folder, with each flaw named `flaw-<N>-before-<M>.png` / `flaw-<N>-after-<M>.png`.
