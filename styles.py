# styles.py
from tkinter import ttk

class StyleManager:
    """Manager stylów dla interfejsu użytkownika"""
    
    def __init__(self):
        self.style = ttk.Style()
        
    def setup_styles(self):
        """Skonfiguruj wszystkie style ttk"""
        self.style.theme_use('clam')
        
        # Style przycisków
        self._setup_button_styles()
        
    def _setup_button_styles(self):
        """Skonfiguruj style przycisków"""
        # Główny przycisk (Primary)
        self.style.configure('Primary.TButton', 
                           background='#222645',
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(12, 6))
        self.style.map('Primary.TButton',
                      background=[('active', '#333756')])
        
        # Przycisk drugorzędny (Secondary)
        self.style.configure('Secondary.TButton',
                           background='#F7F7F7',
                           foreground='black',
                           borderwidth=1,
                           padding=(12, 6))
        self.style.map('Secondary.TButton',
                      background=[('active', '#E0E0E0')])
        
        # Przycisk sukcesu (Success)
        self.style.configure('Success.TButton',
                           background='#BFE02B',
                           foreground='black',
                           borderwidth=0,
                           padding=(12, 6))
        self.style.map('Success.TButton',
                      background=[('active', '#A0C020')])
        
        # Przycisk niebezpieczeństwa (Danger)
        self.style.configure('Danger.TButton',
                           background='#E24B38',
                           foreground='white',
                           borderwidth=0,
                           padding=(12, 6))
        self.style.map('Danger.TButton',
                      background=[('active', '#C03020')])
        
        # Kompaktowy przycisk (Compact)
        self.style.configure('Compact.TButton',
                           background='#F7F7F7',
                           foreground='black',
                           borderwidth=1,
                           padding=(8, 4),
                           font=('Arial', 9))
        self.style.map('Compact.TButton',
                      background=[('active', '#E0E0E0')])


class ColorScheme:
    """Schemat kolorów aplikacji"""
    
    # Kolory główne
    PRIMARY = "#222645"
    PRIMARY_ACTIVE = "#333756"
    
    # Kolory funkcjonalne
    SUCCESS = "#BFE02B"
    SUCCESS_ACTIVE = "#A0C020"
    DANGER = "#E24B38"
    DANGER_ACTIVE = "#C03020"
    
    # Kolory neutralne
    BACKGROUND = "#FFFFFF"
    SECONDARY_BG = "#F9F9F9"
    SIDEBAR_BG = "#F0F0F0"
    BORDER = "#E0E0E0"
    
    # Kolory tekstu
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"
    TEXT_MUTED = "#999999"
    
    # Kolory składni
    HTML_TAG = "#0066CC"
    HTML_ATTRIBUTE = "#009900"
    HTML_VALUE = "#CC0000"
    HTML_COMMENT = "#666666"


class Fonts:
    """Definicje czcionek"""
    
    # Główne czcionki
    MAIN = ("Arial", 10)
    MAIN_BOLD = ("Arial", 10, "bold")
    TITLE = ("Arial", 14, "bold")
    
    # Czcionki specjalne
    CODE = ("Consolas", 11)
    CODE_SMALL = ("Consolas", 10)
    SMALL = ("Arial", 9)
    
    # Czcionki UI
    BUTTON = ("Arial", 10)
    LABEL = ("Arial", 9)


class Dimensions:
    """Wymiary i odstępy"""
    
    # Wysokości
    HEADER_HEIGHT = 50
    CONTROL_PANEL_HEIGHT = 110
    BUTTON_AREA_HEIGHT = 35
    
    # Szerokości
    SIDEBAR_WIDTH = 350
    COLOR_PREVIEW_SIZE = 30
    
    # Padding i marginy
    SECTION_PADDING = 15
    INNER_PADDING = 20
    BUTTON_PADDING = (12, 6)
    COMPACT_BUTTON_PADDING = (8, 4)
    
    # Odstępy
    ELEMENT_SPACING = 5
    SECTION_SPACING = 10