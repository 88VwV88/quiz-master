import os
from flask import Config


class AppConfig(Config):
  DEBUG = True
  SECRET_KEY = os.environ.get("SECRET_KEY", 'VRZ-bPBF53wXt84l5svAzRZVbjcPNYpNhv-ZQA6fIXs')
  JWT_TOKEN_LOCATION = ['cookies']
  JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
  JWT_ACCESS_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
  JWT_ACCESS_CSRF_FIELD_NAME = 'csrf_access_token'
  JWT_COOKIE_SECURE = False
  JWT_COOKIE_CSRF_PROTECT = False