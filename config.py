import os
from dotenv import load_dotenv

load_dotenv()
TRUYENWIKI = {
    'book_domain': os.getenv('BOOK_DOMAIN'),
    'cookie_domain': os.getenv('COOKIES_DOMAIN'),
    'book_path': os.getenv('BOOK_PATH'),
    'logs_path': os.getenv('LOGS_PATH'),
    'uidcms': os.getenv('UIDCMS'),
    'uif': os.getenv('UIF'),
    'express_sid': os.getenv('EXPRESS_SID'),
    'rigelcdp_session_id': os.getenv('RIGELCDP_SESSION_ID'),
    'ga': os.getenv('GA')
}