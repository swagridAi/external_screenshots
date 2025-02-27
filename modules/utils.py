"""
Utility functions for the Screenshot to Table application.
"""
import csv
import json
import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def format_timestamp():
    """Returns a formatted timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def convert_to_csv(table_data):
    """
    Converts table data to CSV format
    
    Args:
        table_data (dict): Table data with 'columns' and 'rows'
        
    Returns:
        str: CSV formatted string
    """
    if not table_data or 'columns' not in table_data or 'rows' not in table_data:
        return ''
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=table_data['columns'])
    
    # Write header
    writer.writeheader()
    
    # Write rows
    writer.writerows(table_data['rows'])
    
    return output.getvalue()

def convert_to_html_table(table_data):
    """
    Converts table data to HTML table
    
    Args:
        table_data (dict): Table data with 'columns' and 'rows'
        
    Returns:
        str: HTML table as string
    """
    if not table_data or 'columns' not in table_data or 'rows' not in table_data:
        return '<p>No valid table data found</p>'
    
    html = ['<table border="1" cellpadding="5" cellspacing="0">']
    
    # Header row
    html.append('<thead><tr>')
    for column in table_data['columns']:
        html.append(f'<th>{escape_html(column)}</th>')
    html.append('</tr></thead>')
    
    # Data rows
    html.append('<tbody>')
    for row in table_data['rows']:
        html.append('<tr>')
        for column in table_data['columns']:
            cell_value = row.get(column, '')
            html.append(f'<td>{escape_html(cell_value)}</td>')
        html.append('</tr>')
    html.append('</tbody>')
    
    html.append('</table>')
    return ''.join(html)

def escape_html(unsafe):
    """
    Escapes HTML special characters
    
    Args:
        unsafe: Value to escape
        
    Returns:
        str: Escaped string
    """
    if unsafe is None:
        return ''
    
    return (str(unsafe)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#039;'))

def setup_logger():
    """
    Sets up the logger configuration
    
    Returns:
        Logger: Configured logger
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler('screenshot_to_table.log')  # Log to file
        ]
    )
    
    return logging.getLogger(__name__)