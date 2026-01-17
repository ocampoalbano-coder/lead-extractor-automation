import re
from email_validator import validate_email, EmailNotValidError
from bs4 import BeautifulSoup
from modules.logger import setup_logger

logger = setup_logger(__name__)

class DataExtractor:
    """
    Extracts structured data from email content.
    """
    
    # Common patterns for lead data
    PATTERNS = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'(?:\+\d{1,3})?\s?(?:\(?\d{1,4}\)?[-\s.]?)?\d{1,4}[-\s.]?\d{1,4}[-\s.]?\d{1,9}',
        'company': r'(?:empresa|company|compañía|sociedad)\s*:?\s*([^\n,]+)',
        'name': r'(?:nombre|name)\s*:?\s*([^\n,]+)'
    }
    
    def extract_from_email(self, email_data):
        """
        Extract structured data from email.
        
        Args:
            email_data: Dictionary with 'from', 'subject', 'body' fields
        
        Returns:
            Dictionary with extracted fields
        """
        try:
            # Clean HTML if present
            body = self._clean_html(email_data.get('body', ''))
            full_text = f"{email_data.get('subject', '')} {body}"
            
            lead = {
                'timestamp': email_data.get('date', ''),
                'source': 'Gmail',
                'name': self._extract_name(email_data, full_text),
                'email': self._extract_email(email_data, full_text),
                'phone': self._extract_phone(full_text),
                'company': self._extract_company(full_text),
                'subject': email_data.get('subject', ''),
                'status': 'Nuevo'
            }
            
            # Validate extracted data
            if not lead['email']:
                logger.warning("Lead extracted without email - skipping")
                return None
            
            logger.info(f"Successfully extracted lead: {lead['email']}")
            return lead
        
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            return None
    
    def _clean_html(self, html_text):
        """
        Clean HTML tags from text.
        
        Args:
            html_text: Text potentially containing HTML
        
        Returns:
            Cleaned text
        """
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            return soup.get_text(separator='\n')
        except:
            return html_text
    
    def _extract_name(self, email_data, text):
        """
        Extract name from email.
        
        Args:
            email_data: Email dictionary
            text: Full text to search
        
        Returns:
            Name string or None
        """
        try:
            # Try from 'From' field
            from_field = email_data.get('from', '')
            if '<' in from_field:
                name = from_field.split('<')[0].strip()
                if name and name != from_field:
                    return name
            
            # Try pattern matching
            match = re.search(self.PATTERNS['name'], text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            return ''
        except:
            return ''
    
    def _extract_email(self, email_data, text):
        """
        Extract email address.
        
        Args:
            email_data: Email dictionary
            text: Full text to search
        
        Returns:
            Valid email string or None
        """
        try:
            # Priority 1: From field
            from_field = email_data.get('from', '')
            if '<' in from_field and '>' in from_field:
                email = from_field.split('<')[1].split('>')[0]
                validate_email(email)
                return email
            
            # Priority 2: Body text
            matches = re.findall(self.PATTERNS['email'], text)
            for email in matches:
                try:
                    validate_email(email)
                    return email
                except EmailNotValidError:
                    continue
            
            return None
        except:
            return None
    
    def _extract_phone(self, text):
        """
        Extract phone number.
        
        Args:
            text: Full text to search
        
        Returns:
            Phone string or None
        """
        try:
            match = re.search(self.PATTERNS['phone'], text)
            if match:
                phone = match.group(0).strip()
                # Remove extra spaces
                phone = re.sub(r'\s+', ' ', phone)
                return phone
            return ''
        except:
            return ''
    
    def _extract_company(self, text):
        """
        Extract company name.
        
        Args:
            text: Full text to search
        
        Returns:
            Company string or None
        """
        try:
            match = re.search(self.PATTERNS['company'], text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                # Clean up
                company = re.sub(r'[^a-zA-Z0-9\s.-]', '', company)
                return company[:100]  # Limit to 100 chars
            return ''
        except:
            return ''
    
    def validate_lead(self, lead):
        """
        Validate if lead has minimum required data.
        
        Args:
            lead: Lead dictionary
        
        Returns:
            Boolean indicating if lead is valid
        """
        if not lead:
            return False
        
        # Minimum required: email and name
        if lead.get('email') and lead.get('name'):
            return True
        
        # Accept if at least email and phone
        if lead.get('email') and lead.get('phone'):
            return True
        
        logger.warning(f"Lead validation failed: {lead}")
        return False
