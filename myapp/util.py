import os
from itsdangerous import URLSafeTimedSerializer

SECRET_KEYS = os.getenv("SECRET_KEY")
ts = URLSafeTimedSerializer(SECRET_KEYS)