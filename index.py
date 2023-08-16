from app import app
from os import getenv

if __name__ == "__main__":
    app.run(debug=getenv("DEV", 0))