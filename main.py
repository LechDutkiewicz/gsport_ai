# main.py - Refaktoryzowany
import tkinter as tk
from tkinter import ttk
from product_manager import ProductManager
from prompt_editor import PromptEditor, PromptManager
from ui_components import ProductInfoPanel, ControlPanel, HTMLPreviewManager, SyntaxHighlighter
from content_area import ContentArea
from styles import StyleManager

class ProductManagerApp:
    """Główna aplikacja do zarządzania opisami produktów"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Inicjalizuj managery
        self.style_manager = StyleManager()
        self.style_manager.setup_styles()
        
        self.prompt_manager = PromptManager()
        self.product_manager = ProductManager(self)
        
        # Utwórz interfejs
        self.create_interface()
        
        # Skonfiguruj powiązania
        self.setup_bindings()
        
    def setup_window(self):
        """Skonfiguruj główne okno"""
        self.root.configure(background="#FFFFFF", padx=0, pady=0)
        self.root.title("GSPORT Redaktor Opisów 2.0")
        self.root.geometry("{}x{}+0+0".format(
            self.root.winfo_screenwidth(), 
            self.root.winfo_screenheight()
        ))
        
    def create_interface(self):
        """Utwórz interfejs użytkownika"""
        # Główny kontener
        main_container = tk.Frame(self.root, bg="#FFFFFF")
        main_container.pack(fill="both", expand=True)
        
        # Panel informacji o produkcie (sidebar)
        self.product_info_panel = ProductInfoPanel(main_container, self)
        
        # Główny obszar aplikacji
        main_area = tk.Frame(main_container, bg="#F9F9F9")
        main_area.pack(side="left", fill="both", expand=True)
        
        # Panel kontrolny
        self.control_panel = ControlPanel(main_area, self)
        
        # Obszar treści
        self.content_area = ContentArea(main_area, self)
        
    def setup_bindings(self):
        """Skonfiguruj powiązania zdarzeń"""
        # Auto-ładowanie produktu
        self.product_info_panel.input_product_link.bind(
            '<Return>', 
            lambda e: self.product_manager.load_product_data()
        )
        self.product_info_panel.input_product_link.bind(
            '<FocusOut>', 
            lambda e: self.on_product_input_change()
        )
        
        # Śledzenie zmian w polach tekstowych
        self.content_area.text_ai_long.bind(
            '<<Modified>>', 
            lambda e: self.on_text_modified('long')
        )
        self.content_area.text_ai_short.bind(
            '<<Modified>>', 
            lambda e: self.on_text_modified('short')
        )
        
    def on_product_input_change(self):
        """Obsługuj zmianę w polu produktu"""
        current_value = self.product_info_panel.input_product_link.get().strip()
        if current_value and current_value != getattr(self, '_last_product_input', ''):
            self._last_product_input = current_value
            self.product_manager.load_product_data()
            
    def on_text_modified(self, field_type):
        """Obsługuj modyfikację tekstu"""
        if field_type == 'long' and self.content_area.text_ai_long.edit_modified():
            SyntaxHighlighter.highlight_syntax(self.content_area.text_ai_long)
            self.content_area.text_ai_long.edit_modified(False)
        elif field_type == 'short' and self.content_area.text_ai_short.edit_modified():
            SyntaxHighlighter.highlight_syntax(self.content_area.text_ai_short)
            self.content_area.text_ai_short.edit_modified(False)
            
    def open_prompt_editor(self):
        """Otwórz edytor promptów"""
        PromptEditor(self.root, self.prompt_manager)
        
    def preview_html(self, description_type):
        """Podgląd HTML w przeglądarce"""
        content = ""
        if description_type == 'long':
            content = self.content_area.text_ai_long.get(1.0, tk.END).strip()
        elif description_type == 'short':
            content = self.content_area.text_ai_short.get(1.0, tk.END).strip()
            
        HTMLPreviewManager.preview_html(content, description_type)
        
    def update_cost_display(self, cost_text):
        """Aktualizuj wyświetlanie kosztów"""
        self.control_panel.lbl_cost.config(text=cost_text)
        
    def enable_update_button(self):
        """Włącz przycisk aktualizacji"""
        self.control_panel.btn_update.config(state='normal')
        
    def disable_update_button(self):
        """Wyłącz przycisk aktualizacji"""
        self.control_panel.btn_update.config(state='disabled')
        
    def clear_all_fields(self):
        """Wyczyść wszystkie pola"""
        self.product_info_panel.clear_all_fields()
        self.content_area.clear_all_fields()
        self.control_panel.lbl_cost.config(text="")
        self.disable_update_button()
        
    def run(self):
        """Uruchom aplikację"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ProductManagerApp()
    app.run()