import os


class Config:
    PAYBC_API_SECRET = os.getenv('PAYBC_API_SECRET')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    OAUTH2_USER = os.getenv('OAUTH2_USER', 'admin')

