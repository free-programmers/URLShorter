import os
import datetime
from pathlib import Path


import redis
from dotenv import load_dotenv
from core.utils import generate_random_string

load_dotenv()




class Setting:
    """ Flask configuration Class
        base Setting os.environ class for flask app
    """

    if not os.environ.get("APP_SECRET_KEY", False):
        print("SECRET_KEY was not found in .env file, fall back into generate_random_string() function. ")

    SECRET_KEY = os.environ.get("APP_SECRET_KEY", generate_random_string())

    API_TITLE = "UrlShorter API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"

    ADMIN_LOGIN_TOKEN = os.environ.get("ADMIN_LOGIN_TOKEN", "123654")

    APP_DEBUG_STATUS = os.environ.get("APP_DEBUG", "") == "True"
    DEBUG = APP_DEBUG_STATUS
    FLASK_DEBUG = APP_DEBUG_STATUS

    DOMAIN = os.environ.get("SERVER", "")
    SERVER_NAME = DOMAIN

    # SMS panel config
    SMS_LINE_NUMBER = os.environ.get("SMS_LINE_NUMBER", "")
    SMS_API_KEY = os.environ.get("SMS_API_KEY", "")

    # Paths
    BASE_DIR = Path(__file__).parent.parent.resolve()
    STORAGE_DIR = BASE_DIR / "Storage"

    MAX_CONTENT_LENGTH = 1024 * 1024 * 50  # global upload max size 50 MB

    # Database Config
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", "")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "")
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
    DATABASE_TABLE_PREFIX_NAME = os.environ.get("DATABASE_TABLE_PREFIX_NAME", "")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Config
    REDIS_DEFAULT_URL = os.environ.get("REDIS_DEFAULT_URI")
    REDIS_DEFAULT_INTERFACE = redis.Redis().from_url(REDIS_DEFAULT_URL)

    # session cookie setting
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=16)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_DOMAIN = False
    SESSION_COOKIE_NAME = '_session_cookie_'
    SESSION_REDIS = redis.Redis.from_url(os.environ.get("REDIS_SESSION_URI")) if os.environ.get("REDIS_SESSION_URI",
                                                                                                None) else REDIS_DEFAULT_INTERFACE

    # Recaptcha Config <Flask-captcha2>

    GOOGLE_CAPTCHA_V2_CONF = {
        "CAPTCHA_PRIVATE_KEY": os.environ.get("CAPTCHA_PRIVATE_KEY_V2", ""),
        "CAPTCHA_PUBLIC_KEY": os.environ.get("CAPTCHA_PUBLIC_KEY_V2", ""),
        "CAPTCHA_ENABLED": os.environ.get('CAPTCHA_ENABLED_V2', str(DEBUG)) == 'True',
        "CAPTCHA_LOG": os.environ.get('CAPTCHA_LOG_V2', str(DEBUG)) == 'True',
        "CAPTCHA_LANGUAGE": os.environ.get('CAPTCHA_LANGUAGE_V2', 'en')
    }

    GOOGLE_CAPTCHA_V3_CONF = {
        "CAPTCHA_PRIVATE_KEY": os.environ.get("CAPTCHA_PRIVATE_KEY_V3", ""),
        "CAPTCHA_PUBLIC_KEY": os.environ.get("CAPTCHA_PUBLIC_KEY_V3", ""),
        "CAPTCHA_ENABLED": os.environ.get('CAPTCHA_ENABLED_V3', str(DEBUG)) == 'True',
        "CAPTCHA_SCORE": float(os.environ.get('CAPTCHA_SCORE_V3', 0.5)) if os.environ.get('CAPTCHA_SCORE_V3',
                                                                                          '0.5').isdigit() else os.environ.get(
            'CAPTCHA_SCORE_V3', 0.5),
        "CAPTCHA_LOG": os.environ.get('CAPTCHA_LOG_V3', str(DEBUG)) == 'True'
    }

    # available languages
    LANGUAGES = {
        'fa': "فارسی/Farsi",
        'en': "English/American English",
        # 'ar': "عربي/Arabic",
        # 'tr': "Turkish/Türkçe",
        # 'ru': "Russian/Россия",
        # 'zh': "Chinese/中国人",
    }

    # Mail config
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = False
    MAIL_DEBUG = os.environ.get("MAIL_DEBUG") == "True"
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # CACHE_TYPE = "RedisCache"  # NullCache for disable Flask-Caching related os.environs
    CACHE_TYPE = os.environ.get("CACHE_TYPE", 'NullCache')
    CACHE_DEFAULT_TIMEOUT = ((60 * 60) * 12)
    CACHE_REDIS_URL = os.environ.get("REDIS_CACHE_URI", REDIS_DEFAULT_URL)

    # celery config
    CELERY = dict(
        broker_url=os.environ.get("REDIS_CELERY_BROKER_URI", REDIS_DEFAULT_URL),
        result_backend=os.environ.get("REDIS_CELERY_BACKEND_URI", REDIS_DEFAULT_URL),
        broker_connection_retry_on_startup=True,
        result_serializer="pickle",
        beat_schedule={
            "every-3-minutes": {
                "task": "Core.tasks.set_cny_currency_in_redis",
                "schedule": 180,
            }
        }
    )

