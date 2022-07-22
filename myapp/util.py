import os
from itsdangerous import URLSafeTimedSerializer

secret = os.getenv("SECRET_KEY")
ts = URLSafeTimedSerializer(secret)