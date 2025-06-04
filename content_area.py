# content_area.py
import tkinter as tk
from tkinter import ttk
from ui_components import SyntaxHighlighter

class ContentArea:
    """Obszar wyświetlania i edycji treści"""
    
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        self.create_content_area()
        
    def create_content_area(self):
        """Utwórz obszar treści"""
        # Import tutaj, aby uniknąć błędów cyklicznych
        try:
            from tkinterweb import HtmlFrame
        except ImportError:
            print("Warning: tkinterweb not available. HTML preview will be limited.")
            HtmlFrame = None
        
        content_frame = tk.Frame(self.parent, bg="#F9F9F9")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Konfiguruj siatkę
        content_frame.columnconfigure(0, weight=2)  # Opis oryginalny
        content_frame.columnconfigure(1, weight=3)  # Specyfikacje
        content_frame.columnconfigure(2, weight=2)  # Treść AI
        content_frame.rowconfigure(0, weight=2)     # Górny rząd
        content_frame.rowconfigure(1, weight=2)     # Dolny rząd
        
        # Opis oryginalny produktu
        self._create_original_description_frame(content_frame, HtmlFrame)
        
        # Ramki specyfikacji
        self._create_specification_frames(content_frame, HtmlFrame)
        
        # Wygenerowane opisy AI
        self._create_ai_description_frames(content_frame)
        
    def _create_original_description_frame(self, parent, HtmlFrame):
        """Utwórz ramkę oryginalnego opisu produktu"""
        frame_original = tk.LabelFrame(
            parent,
            text="Opis produktu ze sklepu",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_original.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        if HtmlFrame:
            self.html_original_desc = HtmlFrame(frame_original, messages_enabled=False)
            self.html_original_desc.pack(fill="both", expand=True)
        else:
            # Fallback dla braku tkinterweb
            self.html_original_desc = tk.Text(frame_original, wrap=tk.WORD)
            self.html_original_desc.pack(fill="both", expand=True)
            
    def _create_specification_frames(self, parent, HtmlFrame):
        """Utwórz ramki specyfikacji"""
        # Specyfikacja JSON
        frame_spec_json = tk.LabelFrame(
            parent,
            text="Specyfikacja JSON",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_spec_json.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        if HtmlFrame:
            self.html_spec_json = HtmlFrame(frame_spec_json, messages_enabled=False)
            self.html_spec_json.pack(fill="both", expand=True)
        else:
            self.html_spec_json = tk.Text(frame_spec_json, wrap=tk.WORD)
            self.html_spec_json.pack(fill="both", expand=True)
        
        # Specyfikacja HTML
        frame_spec_html = tk.LabelFrame(
            parent,
            text="Specyfikacja HTML",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_spec_html.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        if HtmlFrame:
            self.html_spec_html = HtmlFrame(frame_spec_html, messages_enabled=False)
            self.html_spec_html.pack(fill="both", expand=True)
        else:
            self.html_spec_html = tk.Text(frame_spec_html, wrap=tk.WORD)
            self.html_spec_html.pack(fill="both", expand=True)
            
    def _create_ai_description_frames(self, parent):
        """Utwórz ramki opisów AI"""
        # Długi opis AI
        frame_ai_long = tk.LabelFrame(
            parent,
            text="Długi opis AI (edytowalny)",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_ai_long.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self._create_editable_text_area(
            frame_ai_long, 
            'long',
            lambda: self.app.preview_html('long')
        )
        
        # Krótki opis AI
        frame_ai_short = tk.LabelFrame(
            parent,
            text="Krótki opis AI (edytowalny)",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_ai_short.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        self._create_editable_text_area(
            frame_ai_short, 
            'short',
            lambda: self.app.preview_html('short')
        )
        
    def _create_editable_text_area(self, parent, area_type, preview_command):
        """Utwórz edytowalny obszar tekstu z przyciskiem podglądu"""
        # Kontener
        container = tk.Frame(parent, bg="#FFFFFF")
        container.pack(fill="both", expand=True)
        
        # Ramka przycisku na górze
        button_frame = tk.Frame(container, bg="#FFFFFF", height=35)
        button_frame.pack(fill="x", side="top")
        button_frame.pack_propagate(False)
        
        # Przycisk podglądu
        preview_btn = ttk.Button(
            button_frame,
            text="Podgląd HTML",
            command=preview_command,
            style='Compact.TButton'
        )
        preview_btn.pack(side="right", padx=5, pady=5)
        
        # Ramka edytora tekstu
        text_frame = tk.Frame(container, bg="#FFFFFF")
        text_frame.pack(fill="both", expand=True, side="top")
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widget tekstu
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 11),
            padx=10,
            pady=10,
            bg="#FAFAFA"
        )
        text_widget.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Konfiguruj podświetlanie składni
        SyntaxHighlighter.setup_text_widget(text_widget)
        
        # Przypisz widget do odpowiedniego atrybutu
        if area_type == 'long':
            self.text_ai_long = text_widget
        else:
            self.text_ai_short = text_widget
            
        # Powiąż zdarzenia
        text_widget.bind("<KeyRelease>", lambda e: self._on_text_change(area_type))
        text_widget.bind("<<Paste>>", lambda e: self.app.root.after(10, lambda: self._on_text_change(area_type)))
        
    def _on_text_change(self, area_type):
        """Obsługuj zmianę tekstu"""
        if area_type == 'long':
            SyntaxHighlighter.highlight_syntax(self.text_ai_long)
        else:
            SyntaxHighlighter.highlight_syntax(self.text_ai_short)
            
    def load_html_content(self, frame_name, content):
        """Załaduj treść HTML do odpowiedniej ramki"""
        frame = getattr(self, frame_name, None)
        if frame:
            if hasattr(frame, 'load_html'):
                # tkinterweb HtmlFrame
                frame.load_html(content)
            else:
                # Fallback Text widget
                frame.delete(1.0, tk.END)
                frame.insert(1.0, content)
                
    def set_text_content(self, area_type, content):
        """Ustaw treść w edytowalnym obszarze tekstu"""
        if area_type == 'long':
            self.text_ai_long.delete(1.0, tk.END)
            self.text_ai_long.insert(1.0, content)
            SyntaxHighlighter.highlight_syntax(self.text_ai_long)
        elif area_type == 'short':
            self.text_ai_short.delete(1.0, tk.END)
            self.text_ai_short.insert(1.0, content)
            SyntaxHighlighter.highlight_syntax(self.text_ai_short)
            
    def get_text_content(self, area_type):
        """Pobierz treść z edytowalnego obszaru tekstu"""
        if area_type == 'long':
            return self.text_ai_long.get(1.0, tk.END).strip()
        elif area_type == 'short':
            return self.text_ai_short.get(1.0, tk.END).strip()
        return ""
        
    def clear_all_fields(self):
        """Wyczyść wszystkie pola"""
        # Wyczyść ramki HTML
        self.load_html_content('html_original_desc', "")
        self.load_html_content('html_spec_json', "")
        self.load_html_content('html_spec_html', "")
        
        # Wyczyść edytowalne pola tekstu
        self.text_ai_long.delete(1.0, tk.END)
        self.text_ai_short.delete(1.0, tk.END)