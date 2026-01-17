from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from modules.logger import setup_logger
from config import CREDENTIALS_FILE, SHEETS_ID, SHEET_NAME

logger = setup_logger(__name__)

# Sheets API Scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsWriter:
    """
    Handles Google Sheets API interactions.
    """
    
    def __init__(self):
        """
        Initialize Sheets API client.
        """
        self.service = self._authenticate()
        self.sheet_name = SHEET_NAME
    
    def _authenticate(self):
        """
        Authenticate with Sheets API.
        
        Returns:
            Sheets API service instance
        """
        try:
            creds = Credentials.from_service_account_file(
                CREDENTIALS_FILE,
                scopes=SCOPES
            )
            service = build('sheets', 'v4', credentials=creds)
            logger.info(f"Successfully authenticated with Sheets API")
            return service
        
        except Exception as e:
            logger.error(f"Failed to authenticate with Sheets API: {e}")
            raise
    
    def get_headers(self):
        """
        Get header row from sheet.
        
        Returns:
            List of header strings
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!A1:Z1"
            ).execute()
            
            headers = result.get('values', [[]])[0]
            logger.info(f"Retrieved headers: {headers}")
            return headers
        
        except Exception as e:
            logger.error(f"Error getting headers: {e}")
            # Return default headers if sheet is empty
            return ['Timestamp', 'Source', 'Nombre', 'Email', 'Teléfono', 'Empresa', 'Asunto', 'Estado']
    
    def append_lead(self, lead):
        """
        Append lead to sheet.
        
        Args:
            lead: Dictionary with lead data
        
        Returns:
            Boolean indicating success
        """
        try:
            # Get headers to map data correctly
            headers = self.get_headers()
            
            # Create row based on headers
            row = []
            for header in headers:
                value = lead.get(header.lower().replace('á', 'a').replace('é', 'e'), '')
                row.append(value)
            
            # Append to sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!A:Z",
                valueInputOption='USER_ENTERED',
                body={'values': [row]}
            ).execute()
            
            logger.info(f"Lead appended successfully: {lead.get('email', 'N/A')}")
            return True
        
        except Exception as e:
            logger.error(f"Error appending lead: {e}")
            return False
    
    def append_multiple_leads(self, leads):
        """
        Append multiple leads to sheet.
        
        Args:
            leads: List of lead dictionaries
        
        Returns:
            Tuple (successful_count, total_count)
        """
        try:
            headers = self.get_headers()
            rows = []
            
            for lead in leads:
                row = []
                for header in headers:
                    value = lead.get(header.lower().replace('á', 'a').replace('é', 'e'), '')
                    row.append(value)
                rows.append(row)
            
            # Batch append
            result = self.service.spreadsheets().values().append(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!A:Z",
                valueInputOption='USER_ENTERED',
                body={'values': rows}
            ).execute()
            
            logger.info(f"Appended {len(leads)} leads to sheet")
            return len(leads), len(leads)
        
        except Exception as e:
            logger.error(f"Error appending multiple leads: {e}")
            return 0, len(leads)
    
    def check_duplicate(self, email):
        """
        Check if email already exists in sheet.
        
        Args:
            email: Email to search for
        
        Returns:
            Boolean indicating if email exists
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!D:D"  # Assuming column D is Email
            ).execute()
            
            emails = [row[0] for row in result.get('values', []) if row]
            return email in emails
        
        except Exception as e:
            logger.warning(f"Error checking duplicate: {e}")
            return False
    
    def update_cell(self, row, col, value):
        """
        Update specific cell.
        
        Args:
            row: Row number (1-indexed)
            col: Column letter (e.g., 'A', 'B', 'C')
            value: New value
        
        Returns:
            Boolean indicating success
        """
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!{col}{row}",
                valueInputOption='USER_ENTERED',
                body={'values': [[value]]}
            ).execute()
            
            logger.debug(f"Updated cell {col}{row} with value: {value}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating cell: {e}")
            return False
    
    def get_row_count(self):
        """
        Get total number of rows in sheet.
        
        Returns:
            Integer row count
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SHEETS_ID,
                range=f"{self.sheet_name}!A:A"
            ).execute()
            
            rows = result.get('values', [])
            return len(rows)
        
        except Exception as e:
            logger.error(f"Error getting row count: {e}")
            return 0
