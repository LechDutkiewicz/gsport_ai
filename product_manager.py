# product_manager.py
import re
import os
import json
import datetime
import xml.etree.ElementTree as ET
from tkinter import messagebox
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import webbrowser
import tempfile
from PIL import Image, ImageTk
from io import BytesIO
import os

from config import (
    GSPORT_API_URL, 
    GPT_API_KEY, 
    GSPORT_API_KEY, 
    MAX_TOKENS, 
    INPUT_COST, 
    OUTPUT_COST, 
    MODEL
)
from utils import extract_product_id, save_xml_copy
from api_client import GSportAPIClient, OpenAIClient

class ProductManager:
    """Manages product data operations and UI updates"""
    
    def __init__(self, app):
        self.app = app
        self.gsport_client = GSportAPIClient(GSPORT_API_URL, GSPORT_API_KEY)
        self.openai_client = OpenAIClient(GPT_API_KEY, MODEL, MAX_TOKENS)
        
        # Product data
        self.current_product_id = None
        self.product_data = {}
        self.producer_data = {}
        self.specifications = {
            'json': '',
            'html': ''
        }
        self.generated_descriptions = {
            'long': '',
            'short': ''
        }
        
        # Product parameters
        self.product_parameters = {
            'color': None,
            'color_remote_id': None
        }
        
        # Track processed IDs (simplified - no longer saving to files)
        self.processed_ids = []
        
    def load_product_data(self):
        """Load product data based on input"""
        input_text = self.app.input_product_link.get().strip()
        if not input_text:
            return
            
        product_id = extract_product_id(input_text)
        if not product_id:
            return
            
        # Clear fields before loading new data
        self.clear_all_fields()
        
        self.current_product_id = product_id
        
        try:
            # Fetch product data
            data = self.gsport_client.get_product_data(product_id)
            
            if not data:
                messagebox.showinfo("Brak danych", "Nie znaleziono danych dla podanego ID.")
                return
                
            # Store product data
            self.product_data = {
                'name': data.get("prod_name", "Brak nazwy"),
                'description': data.get("prod_desclong", "Brak opisu"),
                'image': data.get("prod_img_src", "")
            }
            
            # Store producer data
            self.producer_data = {
                'name': data.get("prd_name", ""),
                'logo': data.get("prd_logo", ""),
                'description': data.get("prd_link_text", "")
            }
            
            # Extract color from product options
            self._extract_product_color(data)
            
            # Update UI
            self._update_product_display()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać danych produktu: {str(e)}")
            
    def _extract_product_color(self, data):
        """Extract color parameter from product data"""
        # Look for color in prod_options
        if 'prod_options' in data:
            for prod_id, options in data['prod_options'].items():
                for opt_id, option in options.items():
                    if option.get('name') == 'Kolor dominujący' and option.get('type') == 'choose':
                        # Get the selected color value
                        for value_id, value_data in option.get('values', {}).items():
                            if value_data.get('selected'):  # This value is selected
                                remote_id = str(value_id)  # The value_id is the remote_id
                                color_name = value_data.get('name', '')
                                
                                # Store the color data
                                self.product_parameters['color'] = color_name
                                self.product_parameters['color_remote_id'] = remote_id
                                
                                # Update UI if available
                                if hasattr(self.app, 'set_color_from_remote_id'):
                                    self.app.set_color_from_remote_id(remote_id)
                                
                                print(f"Loaded color: {color_name} (remote_id: {remote_id})")
                                return
                                
    def _update_product_display(self):
        """Update UI with loaded product data"""
        # Update product name
        self.app.lbl_prod_name.config(text=self.product_data['name'])
        
        # Update product image
        self._load_and_display_image()
        
        # Update producer status
        if hasattr(self.app, 'update_producer_status'):
            # New Apple-style UI
            self.app.update_producer_status(
                bool(self.producer_data['name']),
                self.producer_data['name'],
                bool(self.producer_data['description'])
            )
        else:
            # Original UI
            if self.producer_data['name']:
                self.app.lbl_producer_present.config(
                    bg='#BFE02B',
                    text=f"Producent: {self.producer_data['name']}"
                )
            else:
                self.app.lbl_producer_present.config(
                    bg='#E24B38',
                    text="Brak producenta"
                )
                
            self.app.lbl_producerdesc_present.config(
                bg='#BFE02B' if self.producer_data['description'] else '#E24B38'
            )
        
        # Display product description
        self.app.html_original_desc.load_html(
            f"<html><body>{self.product_data['description']}</body></html>"
        )
        
    def _load_and_display_image(self):
        """Load and display product image"""
        image_path = self.product_data.get('image', '')
        
        if not image_path:
            self.app.lbl_product_image.config(text="[Brak obrazu]", image='')
            return
            
        # Construct full image URL
        # For thumbnail (100px width)
        image_url = f"https://www.gsport.pl{image_path}_100.jpg"
        # Store the base path for larger preview
        self.image_base_path = f"https://www.gsport.pl{image_path}"
            
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Open image with PIL
            img = Image.open(BytesIO(response.content))
            
            # Calculate size to fit in frame while maintaining aspect ratio
            frame_width = 120
            frame_height = 120
            
            # Get original dimensions
            width, height = img.size
            aspect_ratio = width / height
            
            # Calculate new dimensions
            if aspect_ratio > 1:  # Wider than tall
                new_width = frame_width
                new_height = int(frame_width / aspect_ratio)
            else:  # Taller than wide
                new_height = frame_height
                new_width = int(frame_height * aspect_ratio)
                
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update label
            self.app.lbl_product_image.config(text='', image=photo, cursor="hand2")
            self.app.lbl_product_image.image = photo  # Keep a reference
            
            # Bind click event to show larger preview
            self.app.lbl_product_image.bind("<Button-1>", lambda e: self._show_image_preview())
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.app.lbl_product_image.config(text="[Błąd ładowania]", image='', cursor="")
            self.app.lbl_product_image.unbind("<Button-1>")
            
    def _show_image_preview(self):
        """Show larger image preview in a new window"""
        if not hasattr(self, 'image_base_path'):
            return
            
        preview_window = tk.Toplevel(self.app.root)
        preview_window.title("Podgląd obrazu produktu")
        preview_window.geometry("600x600")
        preview_window.configure(bg="#F9F9F9")
        
        # Center the window
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() - 600) // 2
        y = (preview_window.winfo_screenheight() - 600) // 2
        preview_window.geometry(f"600x600+{x}+{y}")
        
        try:
            # Use larger image size (500px width)
            large_image_url = f"{self.image_base_path}_500.jpg"
            
            # Download image
            response = requests.get(large_image_url, timeout=10)
            response.raise_for_status()
            
            # Open image with PIL
            img = Image.open(BytesIO(response.content))
            
            # Calculate size to fit in window while maintaining aspect ratio
            max_width = 580
            max_height = 550
            
            # Get original dimensions
            width, height = img.size
            aspect_ratio = width / height
            
            # Calculate new dimensions
            if width > max_width or height > max_height:
                if aspect_ratio > max_width / max_height:
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
            else:
                new_width = width
                new_height = height
                
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create label for image
            image_label = tk.Label(preview_window, image=photo, bg="#F9F9F9")
            image_label.image = photo  # Keep a reference
            image_label.pack(expand=True, pady=10)
            
            # Add close button
            close_btn = tk.Button(
                preview_window,
                text="Zamknij",
                command=preview_window.destroy,
                bg="#E24B38",
                fg="white",
                font=("Helvetica", 10),
                padx=20,
                pady=5
            )
            close_btn.pack(pady=10)
            
        except Exception as e:
            error_label = tk.Label(
                preview_window,
                text=f"Nie można załadować obrazu:\n{str(e)}",
                bg="#F9F9F9",
                fg="#E24B38",
                font=("Helvetica", 10)
            )
            error_label.pack(expand=True)
        
    def paste_description(self):
        """Paste description from clipboard"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.product_data['description'] = clipboard_content
            self.app.html_original_desc.load_html(
                f"<html><body>{clipboard_content}</body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def paste_specification_json(self):
        """Paste JSON specification from clipboard"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.specifications['json'] = clipboard_content
            self.app.html_spec_json.load_html(
                f"<html><body><pre>{clipboard_content}</pre></body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def paste_specification(self):
        """Paste HTML specification from clipboard"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.specifications['html'] = clipboard_content
            self.app.html_spec_html.load_html(
                f"<html><body>{clipboard_content}</body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def generate_description(self):
        """Generate product description using AI"""
        if not self.product_data.get('name'):
            messagebox.showwarning("Błąd", "Najpierw załaduj dane produktu")
            return
            
        # Determine if it's a bike based on checkbox
        is_bike = self.app.is_bike_var.get()
        
        try:
            # Select appropriate prompt file and prepare specification
            prompt_file, specification = self._select_prompt_and_spec(is_bike)
            
            # Load and prepare prompt
            prompt = self._load_prompt(prompt_file, specification)
            
            # Generate long description
            long_desc_result = self.openai_client.generate_content(prompt)
            
            if long_desc_result['success']:
                self.generated_descriptions['long'] = long_desc_result['content']
                self._add_producer_section()
                
                # Update cost display
                cost = long_desc_result['cost'] * 100
                self.app.lbl_cost.config(text=f"Koszt: {cost:.5f}¢ USD")
                
                # Display long description in editable text widget
                self.app.text_ai_long.delete(1.0, tk.END)
                self.app.text_ai_long.insert(1.0, self.generated_descriptions['long'])
                
                # Trigger syntax highlighting
                if hasattr(self.app, 'highlight_syntax'):
                    self.app.highlight_syntax(self.app.text_ai_long)
                
                # Generate short description
                self._generate_short_description(is_bike)
                
                # Enable update button
                self.app.btn_update.config(state='normal')
                
                print(f"Użyto pliku z promptem: {prompt_file}")
                
            else:
                messagebox.showerror("Błąd", f"Nie udało się wygenerować opisu: {long_desc_result['error']}")
                
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas generowania opisu: {str(e)}")
            
    def _select_prompt_and_spec(self, is_bike):
        """Select appropriate prompt file and specification based on product type"""
        specification = self.specifications['html']
        
        if is_bike:
            # Bike prompt selection logic
            if self.specifications['json']:
                return "prompt_newdesc_99spokes.txt", self.specifications['json']
            elif self.producer_data['name'] == "SCOTT" and not specification:
                return "prompt_newdesc_scott.txt", ""
            elif specification:
                return "prompt_newdesc_with_specs.txt", specification
            else:
                return "prompt_newdesc.txt", ""
        else:
            # Non-bike prompt selection logic
            if self.specifications['json'] and self.producer_data['name'] == "Micro":
                return "prompt_newdesc_micro.txt", self.specifications['json']
            elif self.specifications['json'] and self.producer_data['name'] == "Leatt":
                return "prompt_newdesc_leatt.txt", self.specifications['json']
            elif self.specifications['json'] or specification:
                return "prompt_newdesc_notbike_with_specs.txt", specification or self.specifications['json']
            else:
                return "prompt_newdesc_notbike.txt", ""
                
    def _load_prompt(self, prompt_file, specification):
        """Load and prepare prompt from file"""
        # Check in prompts folder first, then in root for backward compatibility
        prompt_path = os.path.join('prompts', prompt_file) if os.path.exists(os.path.join('prompts', prompt_file)) else prompt_file
        
        # Reload the prompt file in case it was edited
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                prompt = file.read().replace("\n", "")
        except FileNotFoundError:
            # If custom prompt file doesn't exist, use a default
            print(f"Warning: {prompt_file} not found, using default prompt")
            prompt = """### CEL ###
Chcę, żebyś był ekspertem od copywritingu e-commerce i napisał opis produktu dla {prod_name}.

### OPIS ###
{prod_desclongription}

### SPECYFIKACJA ###
{product_specification}"""
            
        prompt = prompt.replace("{prod_name}", self.product_data['name'])
        prompt = prompt.replace("{prod_desclongription}", self.product_data['description'])
        prompt = prompt.replace("{product_specification}", specification)
        
        return prompt
        
    def _add_producer_section(self):
        """Add producer section to generated description"""
        if self.producer_data['name'] and self.producer_data['description']:
            producer_section = (
                f"<h2>O marce {self.producer_data['name']}</h2>"
                f"<p>{self.producer_data['description']}</p>"
            )
            self.generated_descriptions['long'] += producer_section
            
    def _generate_short_description(self, is_bike):
        """Generate short description based on long description"""
        try:
            # Parse the long description to find first <ul>
            soup = BeautifulSoup(self.generated_descriptions['long'], 'html.parser')
            first_ul = soup.find('ul')
            
            if not first_ul:
                return
                
            # Select appropriate short description prompt
            prompt_file = "prompt_shortdesc.txt" if is_bike else "prompt_shortdesc_short.txt"
            
            # Check in prompts folder first, then in root for backward compatibility
            prompt_path = os.path.join('prompts', prompt_file) if os.path.exists(os.path.join('prompts', prompt_file)) else prompt_file
            
            with open(prompt_path, "r", encoding="utf-8") as file:
                prompt = file.read().replace("\n", "")
                prompt = prompt.replace("{prod_desclongription}", str(first_ul))
                
            # Generate short description
            short_desc_result = self.openai_client.generate_content(prompt)
            
            if short_desc_result['success']:
                self.generated_descriptions['short'] = short_desc_result['content']
                # Display short description in editable text widget
                self.app.text_ai_short.delete(1.0, tk.END)
                self.app.text_ai_short.insert(1.0, self.generated_descriptions['short'])
                
                # Trigger syntax highlighting
                if hasattr(self.app, 'highlight_syntax'):
                    self.app.highlight_syntax(self.app.text_ai_short)
                
        except Exception as e:
            print(f"Error generating short description: {e}")
            
    def update_products(self):
        """Update product and similar products in the system"""
        if not self.current_product_id:
            messagebox.showwarning("Błąd", "Brak danych do zapisania")
            return
            
        # Get current content from text widgets
        self.generated_descriptions['long'] = self.app.text_ai_long.get(1.0, tk.END).strip()
        self.generated_descriptions['short'] = self.app.text_ai_short.get(1.0, tk.END).strip()
        
        if not self.generated_descriptions['long']:
            messagebox.showwarning("Błąd", "Brak opisu do zapisania")
            return
            
        try:
            # Update main product
            success = self._update_single_product(self.current_product_id)
            
            if success:
                self.processed_ids.append(self.current_product_id)
                
            # Update similar products (only if they exist)
            if hasattr(self.app, 'similar_product_entries'):
                for entry in self.app.similar_product_entries:
                    similar_url = entry.get().strip()
                    if similar_url:
                        similar_id = extract_product_id(similar_url)
                        if similar_id:
                            if self._update_single_product(similar_id):
                                self.processed_ids.append(similar_id)
                            
            messagebox.showinfo("Sukces", f"Zaktualizowano produkty: {', '.join(self.processed_ids)}")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas aktualizacji: {str(e)}")
            
    def _update_single_product(self, product_id):
        """Update a single product"""
        xml_content = self._build_xml(product_id)
        
        success = self.gsport_client.update_product(xml_content)
        
        # Save XML copy
        status = "ok" if success else "errors"
        save_xml_copy(xml_content, product_id, f"output/{status}")
        
        return success
        
    def set_product_color(self, color_key, remote_id):
        """Set the selected color for the product"""
        self.product_parameters['color'] = color_key
        self.product_parameters['color_remote_id'] = remote_id
        print(f"Color set: {color_key} (remote_id: {remote_id})")
        
    def _build_xml(self, product_id):
        """Build XML for product update"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Start building XML
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<products xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1" date="{now}">',
            '    <item>',
            f'        <prod_id>{product_id}</prod_id>',
            f'        <prod_shortdesc_pl><![CDATA[{self.generated_descriptions["short"]}]]></prod_shortdesc_pl>',
            f'        <prod_desc_pl><![CDATA[{self.generated_descriptions["long"]}]]></prod_desc_pl>'
        ]
        
        # Add color parameter if selected
        if self.product_parameters['color'] and self.product_parameters['color_remote_id']:
            xml_parts.extend([
                '        <options>',
                '            <options>',
                f'                <option name="Kolor dominujący" remote_id="{self.product_parameters["color_remote_id"]}" required="1">{self.product_parameters["color"]}</option>',
                '            </options>',
                '        </options>'
            ])
        
        xml_parts.extend([
            '    </item>',
            '</products>'
        ])
        
        return '\n'.join(xml_parts)
                
    def clear_all_fields(self):
        """Clear all fields and reset state"""
        # Reset data
        self.current_product_id = None
        self.product_data = {}
        self.producer_data = {}
        self.specifications = {'json': '', 'html': ''}
        self.generated_descriptions = {'long': '', 'short': ''}
        self.product_parameters = {'color': None, 'color_remote_id': None}
        
        # Clear UI elements
        self.app.lbl_prod_name.config(text="[Nazwa produktu]")
        self.app.lbl_producer_present.config(bg='#dedede', text="Producent")
        self.app.lbl_producerdesc_present.config(bg='#dedede')
        self.app.lbl_cost.config(text="")
        
        # Clear color selection
        if hasattr(self.app, 'clear_color_selection'):
            self.app.clear_color_selection()
        
        # Clear similar products (only if they exist)
        if hasattr(self.app, 'similar_product_entries'):
            for entry in self.app.similar_product_entries:
                entry.delete(0, 'end')
            
        # Clear HTML frames
        self.app.html_original_desc.load_html("")
        self.app.html_spec_json.load_html("")
        self.app.html_spec_html.load_html("")
        
        # Clear text widgets
        self.app.text_ai_long.delete(1.0, tk.END)
        self.app.text_ai_short.delete(1.0, tk.END)
        
        # Clear product image
        self.app.lbl_product_image.config(text="[Brak obrazu]", image='')
        
        # Disable update button
        self.app.btn_update.config(state='disabled')
        
    def preview_html(self, description_type: str):
        """Preview HTML content in a web browser"""
        content = ""
        if description_type == 'long':
            content = self.app.text_ai_long.get(1.0, tk.END).strip()
        elif description_type == 'short':
            content = self.app.text_ai_short.get(1.0, tk.END).strip()
            
        if not content:
            messagebox.showinfo("Info", "Brak treści do podglądu")
            return
            
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Podgląd opisu</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .content {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""
            f.write(html_content)
            temp_path = f.name
            
        # Open in default web browser
        webbrowser.open(f'file://{temp_path}')