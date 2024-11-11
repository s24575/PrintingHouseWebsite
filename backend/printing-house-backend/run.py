import os

import stripe
from dotenv import load_dotenv

from app import create_app

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")

app = create_app()
app.run()
