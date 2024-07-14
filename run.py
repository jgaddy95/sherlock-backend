from dotenv import load_dotenv
load_dotenv()  # This line loads the variables from .env

import logging
logging.basicConfig(level=logging.INFO)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)