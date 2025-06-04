# utils.py
import re
import os
import datetime
from tkinter import messagebox
from typing import Optional

def extract_product_id(text: str) -> Optional[str]:
    """
    Extract product ID from Sky-Shop link or return it if it's just a number.
    
    Args:
        text: Input text containing link or ID
        
    Returns:
        Product ID as string or None if invalid
    """
    if not text:
        messagebox.showerror("Błąd", "Pole jest puste. Wklej link do produktu lub numer ID.")
        return None
        
    text = text.strip()
    
    # Case: link contains p + numbers
    match = re.search(r'p(\d+)', text)
    if match:
        return match.group(1)
        
    # Case: just a number as ID
    if text.isdigit():
        return text
        
    # Otherwise: invalid input
    messagebox.showerror("Nieprawidłowe dane", "Wklej link do produktu Sky-Shop lub numer ID produktu.")
    return None
    

def save_xml_copy(xml_content: str, product_id: str, save_path: str) -> None:
    """
    Save a copy of XML to file with timestamp and product ID.
    
    Args:
        xml_content: XML content as string
        product_id: Product ID for filename
        save_path: Directory path where to save the file
    """
    # Ensure directory exists
    os.makedirs(save_path, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{product_id}.xml"
    file_path = os.path.join(save_path, filename)
    
    # Write file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_content)
        
    print(f"XML saved as: {file_path}")
    

def format_cost_display(cost_in_dollars: float) -> str:
    """
    Format cost for display in cents.
    
    Args:
        cost_in_dollars: Cost in dollars
        
    Returns:
        Formatted string with cost in cents
    """
    cost_in_cents = cost_in_dollars * 100
    return f"Koszt: {cost_in_cents:.5f}¢ USD"
    

def clean_html_for_display(html_content: str) -> str:
    """
    Prepare HTML content for display in HtmlFrame.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        Wrapped HTML ready for display
    """
    if not html_content:
        return ""
        
    # Ensure content is wrapped in html/body tags
    if not html_content.strip().startswith("<html>"):
        html_content = f"<html><body>{html_content}</body></html>"
        
    return html_content