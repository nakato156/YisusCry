from flask import redirect

def status_401(*args):
    return redirect("/login")