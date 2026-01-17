import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gmail Configuration
GMAIL_USER = os.getenv('GMAIL_USER', 'your-email@gmail.com')

# Google Sheets Configuration
SHEETS_ID = os.getenv('SHEETS_ID', '')
SHEET_NAME = os.getenv('SHEET_NAME', 'Leads')

# Email Search Configuration
SEARCH_QUERY = os.getenv('SEARCH_QUERY', 'subject:Nueva consulta')
MARK_AS_READ = os.getenv('MARK_AS_READ', 'True').lower() == 'true'
SEND_CONFIRMATION = os.getenv('SEND_CONFIRMATION', 'False').lower() == 'true'
CONFIRMATION_EMAIL = os.getenv('CONFIRMATION_EMAIL', 'noreply@mycompany.com')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/lead_extractor.log')

# Scheduling
RUN_EVERY_HOURS = int(os.getenv('RUN_EVERY_HOURS', '1'))

# Credentials file path
CREDENTIALS_FILE = 'credentials.json'

# Create logs directory if it doesn't exist
if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
