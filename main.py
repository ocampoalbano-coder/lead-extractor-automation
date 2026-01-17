#!/usr/bin/env python3
"""
Lead Extractor: Gmail to Google Sheets Automation

This script reads new emails from Gmail, extracts lead data,
and appends them to a Google Sheet automatically.

Usage:
    python main.py              # Run once
    python schedule_unix.py     # Run every hour (Linux/macOS)
    python schedule_windows.py  # Run every hour (Windows)
"""

import sys
from modules.logger import setup_logger
from modules.gmail_reader import GmailReader
from modules.data_extractor import DataExtractor
from modules.sheets_writer import SheetsWriter
from config import SEARCH_QUERY, MARK_AS_READ

# Initialize logger
logger = setup_logger(__name__)

def main():
    """
    Main orchestration function.
    """
    logger.info("="*50)
    logger.info("Starting Lead Extractor")
    logger.info("="*50)
    
    try:
        # Initialize components
        logger.info("Initializing Gmail Reader...")
        gmail = GmailReader()
        
        logger.info("Initializing Data Extractor...")
        extractor = DataExtractor()
        
        logger.info("Initializing Sheets Writer...")
        sheets = SheetsWriter()
        
        # Read emails
        logger.info(f"Fetching emails with query: {SEARCH_QUERY}")
        emails = gmail.get_unread_emails(SEARCH_QUERY)
        
        if not emails:
            logger.info("No new emails found.")
            return
        
        logger.info(f"Found {len(emails)} emails. Processing...")
        
        # Extract and append leads
        successful = 0
        failed = 0
        duplicates = 0
        
        for email in emails:
            try:
                # Extract data
                lead = extractor.extract_from_email(email)
                
                if not lead:
                    logger.warning(f"Failed to extract data from email: {email.get('subject', 'N/A')}")
                    failed += 1
                    continue
                
                # Validate lead
                if not extractor.validate_lead(lead):
                    logger.warning(f"Lead validation failed: {lead.get('email', 'N/A')}")
                    failed += 1
                    continue
                
                # Check duplicates
                if sheets.check_duplicate(lead['email']):
                    logger.info(f"Duplicate lead found: {lead['email']}")
                    duplicates += 1
                    continue
                
                # Append to sheets
                if sheets.append_lead(lead):
                    successful += 1
                    
                    # Mark email as read
                    if MARK_AS_READ:
                        gmail.mark_as_read(email['id'])
                else:
                    failed += 1
            
            except Exception as e:
                logger.error(f"Error processing email: {e}")
                failed += 1
        
        # Summary
        logger.info("="*50)
        logger.info(f"Processing Complete:")
        logger.info(f"  Successful: {successful}")
        logger.info(f"  Failed: {failed}")
        logger.info(f"  Duplicates: {duplicates}")
        logger.info(f"  Total Rows: {sheets.get_row_count()}")
        logger.info("="*50)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
