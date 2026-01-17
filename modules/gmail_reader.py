import base64
import pickle
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from modules.logger import setup_logger
from config import CREDENTIALS_FILE, GMAIL_USER

logger = setup_logger(__name__)

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailReader:
    """
    Handles Gmail API interactions.
    """
    
    def __init__(self):
        """
        Initialize Gmail API client.
        """
        self.service = self._authenticate()
    
    def _authenticate(self):
        """
        Authenticate with Gmail API using credentials file.
        
        Returns:
            Gmail API service instance
        """
        try:
            creds = None
            
            # Try loading from credentials.json
            try:
                creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
            except Exception as e:
                logger.warning(f"Could not load service account: {e}")
                logger.info("Attempting OAuth2 flow...")
                
                # Fallback to OAuth2 flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            service = build('gmail', 'v1', credentials=creds)
            logger.info(f"Successfully authenticated with Gmail API for {GMAIL_USER}")
            return service
        
        except Exception as e:
            logger.error(f"Failed to authenticate with Gmail API: {e}")
            raise
    
    def get_unread_emails(self, query):
        """
        Get unread emails matching query.
        
        Args:
            query: Gmail search query (e.g., 'subject:Nueva consulta')
        
        Returns:
            List of email dictionaries
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10  # Limit to 10 per run
            ).execute()
            
            messages = results.get('messages', [])
            logger.info(f"Found {len(messages)} emails matching query: {query}")
            
            email_list = []
            for message in messages:
                email = self.get_email_details(message['id'])
                email_list.append(email)
            
            return email_list
        
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []
    
    def get_email_details(self, message_id):
        """
        Get full details of a specific email.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with email details
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            email_data = {
                'id': message_id,
                'from': next((h['value'] for h in headers if h['name'] == 'From'), ''),
                'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), ''),
                'date': next((h['value'] for h in headers if h['name'] == 'Date'), ''),
                'body': self._get_email_body(message['payload'])
            }
            
            return email_data
        
        except Exception as e:
            logger.error(f"Error getting email details for {message_id}: {e}")
            return None
    
    def _get_email_body(self, payload):
        """
        Extract body from email payload.
        
        Args:
            payload: Gmail message payload
        
        Returns:
            Email body text
        """
        if 'parts' in payload:
            parts = payload['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            if 'body' in payload and 'data' in payload['body']:
                return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return ''
    
    def mark_as_read(self, message_id):
        """
        Mark email as read.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Boolean indicating success
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.debug(f"Marked email {message_id} as read")
            return True
        
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")
            return False
    
    def add_label(self, message_id, label_name):
        """
        Add label to email.
        
        Args:
            message_id: Gmail message ID
            label_name: Label name (e.g., 'Processed')
        
        Returns:
            Boolean indicating success
        """
        try:
            # Get label ID
            labels = self.service.users().labels().list(userId='me').execute()['labels']
            label_id = next((l['id'] for l in labels if l['name'] == label_name), None)
            
            if label_id:
                self.service.users().messages().modify(
                    userId='me',
                    id=message_id,
                    body={'addLabelIds': [label_id]}
                ).execute()
                logger.debug(f"Added label '{label_name}' to email {message_id}")
                return True
            else:
                logger.warning(f"Label '{label_name}' not found")
                return False
        
        except Exception as e:
            logger.error(f"Error adding label: {e}")
            return False
