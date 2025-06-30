# ui_components.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tempfile
import webbrowser
from utils import extract_product_id

class ProductInfoPanel:
    """Panel z informacjami o produkcie (sidebar)"""
    
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        self.colors = {
            'szary': {'hex': '#808080', 'name': 'Szary', 'remote_id': '10241'},
            'wielokolorowy': {'hex': 'multi', 'name': 'Wielokolorowy', 'remote_id': '10265'},
            'czarny': {'hex': '#000000', 'name': 'Czarny', 'remote_id': '10294'},
            'niebieski': {'hex': '#0000ff', 'name': 'Niebieski', 'remote_id': '10302'},
            'pomarańczowy': {'hex': '#ffa500', 'name': 'Pomarańczowy', 'remote_id': '10481'},
            'biały': {'hex': '#f7f7f7', 'name': 'Biały', 'remote_id': '10567'},
            'fioletowy': {'hex': '#800080', 'name': 'Fioletowy', 'remote_id': '10579'},
            'czerwony': {'hex': '#ff0000', 'name': 'Czerwony', 'remote_id': '10597'},
            'różowy': {'hex': '#ffc0cb', 'name': 'Różowy', 'remote_id': '10627'},
            'żółty': {'hex': '#ffff00', 'name': 'Żółty', 'remote_id': '11060'},
            'zielony': {'hex': '#008000', 'name': 'Zielony', 'remote_id': '11287'},
            'brązowy': {'hex': '#a52a2a', 'name': 'Brązowy', 'remote_id': '23465'},
            'złoty': {'hex': '#ebd271', 'name': 'Złoty', 'remote_id': '23491'}
        }
        self.color_by_remote_id = {data['remote_id']: key for key, data in self.colors.items()}
        self.selected_color = tk.StringVar(value="")
        
        self.create_panel()
        
    def create_panel(self):
        """Utwórz panel boczny"""
        self.sidebar = tk.Frame(self.parent, bg="#F0F0F0", width=350)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Tytuł
        self._create_title()
        
        # Sekcja input produktu
        self._create_product_input_section()
        
        # Sekcja parametrów
        self._create_parameters_section()
        
        # Sekcja podobnych produktów
        self._create_similar_products_section()
        
        # Spacer
        spacer = tk.Frame(self.sidebar, bg="#F0F0F0")
        spacer.pack(fill="both", expand=True)
        
        # Przyciski narzędziowe
        self._create_utility_buttons()
        
    def _create_title(self):
        """Utwórz tytuł panelu"""
        title_frame = tk.Frame(self.sidebar, bg="#222645", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Informacje o produkcie",
            font=("Arial", 14, "bold"),
            bg="#222645",
            fg="white"
        )
        title_label.pack(expand=True)
        
    def _create_product_input_section(self):
        """Utwórz sekcję wprowadzania produktu"""
        section = tk.Frame(self.sidebar, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=15)
        
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=20)
        
        # Etykieta input
        input_label = tk.Label(
            inner,
            text="ID lub link do produktu",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#666666"
        )
        input_label.pack(anchor="w", pady=(0, 5))
        
        # Pole input
        self.input_product_link = tk.Entry(inner, width=35, font=("Arial", 11))
        self.input_product_link.pack(fill="x", pady=(0, 10))
        
        # Przyciski ładowania
        buttons_frame = tk.Frame(inner, bg="#FFFFFF")
        buttons_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_load_normal = tk.Button(
            buttons_frame,
            text="Załaduj produkt",
            font=("Arial", 9),
            bg="#222645",
            fg="white",
            bd=1,
            relief="solid",
            padx=10,
            pady=3,
            command=self.app.product_manager.load_product_data
        )
        self.btn_load_normal.pack(side="left", padx=(0, 5))
        
        self.btn_load_preserve = tk.Button(
            buttons_frame,
            text="Załaduj zachowując AI",
            font=("Arial", 9),
            bg="#BFE02B",
            fg="black",
            bd=1,
            relief="solid",
            padx=10,
            pady=3,
            command=self.app.product_manager.load_product_data_preserve_ai
        )
        self.btn_load_preserve.pack(side="left")

        # Opis przycisków
        help_label = tk.Label(
            inner,
            text="Enter = Załaduj produkt  |  Przyciski = wybierz tryb ładowania",
            font=("Arial", 8),
            fg="#999999",
            bg="#FFFFFF"
        )
        help_label.pack(pady=(5, 0))
        
        # Ramka obrazka
        self.image_frame = tk.Frame(
            inner,
            bg="#E5E5E5",
            width=120,
            height=120
        )
        self.image_frame.pack(pady=(0, 10))
        self.image_frame.pack_propagate(False)
        
        self.lbl_product_image = tk.Label(
            self.image_frame,
            text="[Brak obrazu]",
            bg="#E5E5E5",
            fg="#999999"
        )
        self.lbl_product_image.pack(expand=True)
        
        # Nazwa produktu
        self.lbl_prod_name = tk.Label(
            inner, 
            text="[Nazwa produktu]",
            bg="#FFFFFF",
            font=("Arial", 10),
            wraplength=280,
            justify="center"
        )
        self.lbl_prod_name.pack(pady=(0, 15))
        
        # Status producenta
        status_frame = tk.Frame(inner, bg="#FFFFFF")
        status_frame.pack()
        
        self.lbl_producer_present = tk.Label(
            status_frame, 
            text="Producent", 
            bg='#dedede',
            padx=10,
            pady=5,
            font=("Arial", 9)
        )
        self.lbl_producer_present.pack(side="left", padx=2)
        
        self.lbl_producerdesc_present = tk.Label(
            status_frame, 
            text="Opis producenta", 
            bg='#dedede',
            padx=10,
            pady=5,
            font=("Arial", 9)
        )
        self.lbl_producerdesc_present.pack(side="left", padx=2)
        
    def _create_parameters_section(self):
        """Utwórz sekcję parametrów produktu"""
        section = tk.Frame(self.sidebar, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=(0, 15))
        
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=15)
        
        # Etykieta sekcji
        label = tk.Label(
            inner,
            text="Parametry produktu",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        label.pack(anchor="w", pady=(0, 10))
        
        # Selektor koloru
        self._create_color_selector(inner)
        
    def _create_color_selector(self, parent):
        """Utwórz selektor koloru"""
        color_frame = tk.Frame(parent, bg="#FFFFFF")
        color_frame.pack(fill="x", pady=(0, 10))
        
        color_label = tk.Label(
            color_frame,
            text="Kolor dominujący:",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        )
        color_label.pack(anchor="w", pady=(0, 5))
        
        dropdown_frame = tk.Frame(color_frame, bg="#FFFFFF")
        dropdown_frame.pack(fill="x")
        
        # Podgląd koloru
        self.color_preview = tk.Frame(
            dropdown_frame,
            width=30,
            height=30,
            bg="#E5E5E5",
            relief="solid",
            bd=1
        )
        self.color_preview.pack(side="left", padx=(0, 10))
        
        # Dropdown - posortowany alfabetycznie
        sorted_colors = sorted(self.colors.values(), key=lambda x: x['name'])
        color_options = [""] + [f"{data['name']}" for data in sorted_colors]
        self.color_dropdown = ttk.Combobox(
            dropdown_frame,
            values=color_options,
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        self.color_dropdown.pack(side="left", fill="x", expand=True)
        self.color_dropdown.bind("<<ComboboxSelected>>", self.on_color_selected)
        
        # Przycisk czyszczenia
        self.btn_clear_color = tk.Button(
            dropdown_frame,
            text="✕",
            font=("Arial", 10),
            bg="#F0F0F0",
            fg="#666666",
            bd=1,
            relief="solid",
            width=3,
            command=self.clear_color_selection,
            state="disabled"
        )
        self.btn_clear_color.pack(side="left", padx=(5, 0))
        self._create_height_selector(parent)

    def _create_height_selector(self, parent):
        """Utwórz selektor zakresu wzrostu"""
        print("🔧 Tworzenie selektora wzrostu...")

        from height_manager import HeightManager
        
        self.height_frame = tk.Frame(parent, bg="#FFFFFF")
        self.height_frame.pack(fill="x", pady=(0, 15))
        
        height_label = tk.Label(
            self.height_frame,
            text="Zakres wzrostu (dla rowerów):",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        )
        height_label.pack(anchor="w", pady=(0, 5))
        
        # Ramka z inputami zakresu
        range_frame = tk.Frame(self.height_frame, bg="#FFFFFF")
        range_frame.pack(fill="x", pady=(0, 5))
        
        # Minimalny wzrost
        tk.Label(
            range_frame,
            text="Od:",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        ).pack(side="left")
        
        self.height_min_var = tk.StringVar()
        self.height_min_entry = tk.Entry(
            range_frame,
            textvariable=self.height_min_var,
            width=5,
            font=("Arial", 9),
            justify="center"
        )
        self.height_min_entry.pack(side="left", padx=(5, 10))
        
        tk.Label(
            range_frame,
            text="Do:",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        ).pack(side="left")
        
        self.height_max_var = tk.StringVar()
        self.height_max_entry = tk.Entry(
            range_frame,
            textvariable=self.height_max_var,
            width=5,
            font=("Arial", 9),
            justify="center"
        )
        self.height_max_entry.pack(side="left", padx=(5, 10))
        
        tk.Label(
            range_frame,
            text="cm",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        ).pack(side="left")
        
        # Przyciski
        button_frame = tk.Frame(range_frame, bg="#FFFFFF")
        button_frame.pack(side="right")
        
        self.btn_set_height = tk.Button(
            button_frame,
            text="Ustaw",
            font=("Arial", 8),
            bg="#BFE02B",
            fg="black",
            bd=1,
            relief="solid",
            padx=8,
            pady=2,
            command=self.set_height_range
        )
        self.btn_set_height.pack(side="left", padx=(0, 5))
        
        self.btn_clear_height = tk.Button(
            button_frame,
            text="✕",
            font=("Arial", 8),
            bg="#F0F0F0",
            fg="#666666",
            bd=1,
            relief="solid",
            width=3,
            pady=2,
            command=self.clear_height_range,
            state="disabled"
        )
        self.btn_clear_height.pack(side="left")
        
        # Dropdown z sugerowanymi zakresami
        suggestions_frame = tk.Frame(self.height_frame, bg="#FFFFFF")
        suggestions_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(
            suggestions_frame,
            text="Szybki wybór:",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#999999"
        ).pack(anchor="w", pady=(0, 5))
        
        # Kategoria
        category_frame = tk.Frame(suggestions_frame, bg="#FFFFFF")
        category_frame.pack(fill="x", pady=(0, 3))
        
        tk.Label(
            category_frame,
            text="Kategoria:",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#666666",
            width=10,
            anchor="w"
        ).pack(side="left")
        
        height_manager = HeightManager()
        categories = [""] + height_manager.get_category_list()
        
        self.height_category = ttk.Combobox(
            category_frame,
            values=categories,
            state="readonly",
            width=20,
            font=("Arial", 8)
        )
        self.height_category.pack(side="left", padx=(5, 0), fill="x", expand=True)
        self.height_category.bind("<<ComboboxSelected>>", self.on_category_selected)
        
        # Rozmiar (drugi rząd)
        size_frame = tk.Frame(suggestions_frame, bg="#FFFFFF")
        size_frame.pack(fill="x", pady=(0, 3))
        
        tk.Label(
            size_frame,
            text="Rozmiar:",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#666666",
            width=10,
            anchor="w"
        ).pack(side="left")
        
        self.height_size = ttk.Combobox(
            size_frame,
            values=[""],
            state="readonly",
            width=35,
            font=("Arial", 8)
        )
        self.height_size.pack(side="left", padx=(5, 0), fill="x", expand=True)
        self.height_size.bind("<<ComboboxSelected>>", self.on_size_selected)
        
        # Przechowuj referencję do height_manager
        self.height_manager = height_manager

        # Status wzrostu
        self.height_status = tk.Label(
            self.height_frame,
            text="",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#666666"
        )
        self.height_status.pack(anchor="w")

        print("✅ Selektor wzrostu utworzony pomyślnie")
        
    def _create_similar_products_section(self):
        """Utwórz sekcję podobnych produktów"""
        section = tk.Frame(self.sidebar, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=(0, 15))
        
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=15)
        
        label = tk.Label(
            inner,
            text="Podobne produkty",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#666666"
        )
        label.pack(anchor="w", pady=(0, 10))
        
        self.similar_product_entries = []
        for i in range(5):
            entry = tk.Entry(inner, width=35, font=("Arial", 9))
            entry.pack(fill="x", pady=2)
            self.similar_product_entries.append(entry)
            
    def _create_utility_buttons(self):
        """Utwórz przyciski narzędziowe"""
        button_frame = tk.Frame(self.sidebar, bg="#F0F0F0")
        button_frame.pack(fill="x", padx=15, pady=15)
        
        self.btn_prompt_editor = ttk.Button(
            button_frame,
            text='Edytor promptów',
            command=self.app.open_prompt_editor,
            style='Secondary.TButton'
        )
        self.btn_prompt_editor.pack(fill="x", pady=(0, 10))
        
        self.btn_reset = ttk.Button(
            button_frame,
            text="Wyczyść wszystko",
            command=self.app.product_manager.clear_all_fields,
            style='Danger.TButton'
        )
        self.btn_reset.pack(fill="x")
        
    def on_color_selected(self, event):
        """Obsługuj wybór koloru"""
        selected_name = self.color_dropdown.get()
        
        if not selected_name:
            self.clear_color_selection()
            return
            
        color_key = None
        for key, data in self.colors.items():
            if data['name'] == selected_name:
                color_key = key
                break
                
        if color_key:
            self.select_color(color_key)
            
    def select_color(self, color_key):
        """Wybierz kolor"""
        self.selected_color.set(color_key)
        
        color_data = self.colors[color_key]
        if color_data['hex'] == 'multi':
            self.color_preview.config(bg="#FFFFFF")
            if not hasattr(self, 'rainbow_label'):
                self.rainbow_label = tk.Label(
                    self.color_preview,
                    text="🌈",
                    bg="#FFFFFF",
                    font=("Arial", 14)
                )
            self.rainbow_label.pack(expand=True)
        else:
            self.color_preview.config(bg=color_data['hex'])
            if hasattr(self, 'rainbow_label'):
                self.rainbow_label.pack_forget()
        
        self.color_dropdown.set(color_data['name'])
        self.btn_clear_color.config(state="normal")
        
        # Powiadom product manager
        if hasattr(self.app, 'product_manager'):
            self.app.product_manager.set_product_color(color_key, color_data['remote_id'])
    
    def clear_color_selection(self):
        """Wyczyść wybór koloru"""
        self.selected_color.set("")
        self.color_preview.config(bg="#E5E5E5")
        if hasattr(self, 'rainbow_label'):
            self.rainbow_label.pack_forget()
        self.color_dropdown.set("")
        self.btn_clear_color.config(state="disabled")
        
        if hasattr(self.app, 'product_manager'):
            self.app.product_manager.set_product_color(None, None)

    def set_height_range(self):
        """Ustaw zakres wzrostu"""
        try:
            min_height = int(self.height_min_var.get())
            max_height = int(self.height_max_var.get())
            
            if hasattr(self.app, 'product_manager'):
                success = self.app.product_manager.data_manager.set_product_height_range(min_height, max_height)
                if success:
                    self.btn_clear_height.config(state="normal")
                    self.update_height_status()
                else:
                    messagebox.showerror(
                        "Błąd", 
                        f"Nieprawidłowy zakres wzrostu. Dostępne wartości: 82-205 cm"
                    )
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź prawidłowe wartości liczbowe")
            
    def clear_height_range(self):
        """Wyczyść zakres wzrostu"""
        print(f"🗑️ Czyszczenie zakresu wzrostu")
        
        if hasattr(self.app, 'product_manager'):
            self.app.product_manager.data_manager.clear_product_height_range()
            
        # Sprawdź czy elementy UI istnieją przed ich użyciem
        if hasattr(self, 'height_min_var'):
            self.height_min_var.set("")
        if hasattr(self, 'height_max_var'):
            self.height_max_var.set("")
        if hasattr(self, 'height_category'):
            self.height_category.set("")
        if hasattr(self, 'height_size'):
            self.height_size.set("")
        if hasattr(self, 'btn_clear_height'):
            self.btn_clear_height.config(state="disabled")
        if hasattr(self, 'height_status'):
            self.height_status.config(text="")
        
    def on_height_suggestion_selected(self, event):
        """Obsługuj wybór sugerowanego zakresu wzrostu"""
        selected_desc = self.height_suggestions.get()
        if not selected_desc:
            return
            
        # Znajdź odpowiadający zakres
        for min_h, max_h, desc in self.suggested_ranges:
            if desc == selected_desc:
                self.height_min_var.set(str(min_h))
                self.height_max_var.set(str(max_h))
                self.set_height_range()
                break
                
    def update_height_status(self):
        """Aktualizuj status wzrostu"""
        if not hasattr(self, 'height_status'):
            return
            
        if hasattr(self.app, 'product_manager'):
            summary = self.app.product_manager.data_manager.get_height_range_summary()
            count = self.app.product_manager.data_manager.get_selected_heights_count()
            
            if summary:
                self.height_status.config(
                    text=f"Zakres: {summary} ({count} wartości)",
                    fg="#008000"
                )
            else:
                self.height_status.config(text="", fg="#666666")
                
    def set_height_from_api_data(self):
        """Ustaw wzrost na podstawie danych z API"""
        if hasattr(self.app, 'product_manager'):
            height_range = self.app.product_manager.data_manager.parameters.height_range
            if height_range:
                self.height_min_var.set(str(height_range.min_height))
                self.height_max_var.set(str(height_range.max_height))
                self.btn_clear_height.config(state="normal")
                self.update_height_status()

    def update_height_display_from_api(self):
        """Aktualizuj wyświetlanie wzrostu na podstawie danych z API"""
        if hasattr(self.app, 'product_manager'):
            height_range = self.app.product_manager.data_manager.parameters.height_range
            if height_range:
                # Ustaw wartości w polach
                self.height_min_var.set(str(height_range.min_height))
                self.height_max_var.set(str(height_range.max_height))
                
                # Włącz przycisk czyszczenia
                self.btn_clear_height.config(state="normal")
                
                # Aktualizuj status
                self.update_height_status()
                
                # Sprawdź czy pasuje do któregoś z sugerowanych zakresów
                self._match_suggested_range_new(height_range)
                
                print(f"📋 UI: Ustawiono zakres wzrostu {height_range.min_height}-{height_range.max_height} cm")
            else:
                print(f"📋 UI: Brak zakresu wzrostu do ustawienia")

    def _match_suggested_range(self, height_range):
        """Sprawdź czy zakres pasuje do któregoś z sugerowanych"""
        if not hasattr(self, 'suggested_ranges'):
            return
            
        for min_h, max_h, desc in self.suggested_ranges:
            if min_h == height_range.min_height and max_h == height_range.max_height:
                self.height_suggestions.set(desc)
                print(f"🎯 Znaleziono pasujący sugerowany zakres: {desc}")
                return
                
        # Jeśli nie ma dokładnego dopasowania, wyczyść dropdown
        self.height_suggestions.set("")

    def on_category_selected(self, event):
        """Obsługuj wybór kategorii"""
        selected_category = self.height_category.get()
        
        if not selected_category:
            # Jeśli pusta kategoria, wyczyść rozmiary
            self.height_size.config(values=[""])
            self.height_size.set("")
            return
            
        # Pobierz rozmiary dla wybranej kategorii
        ranges = self.height_manager.get_ranges_for_category(selected_category)
        size_options = [""] + [desc for _, _, desc in ranges]
        
        # Aktualizuj dropdown rozmiarów
        self.height_size.config(values=size_options)
        self.height_size.set("")  # Wyczyść wybór
        
        print(f"📋 Wybrano kategorię: {selected_category} ({len(ranges)} rozmiarów)")

    def on_size_selected(self, event):
        """Obsługuj wybór rozmiaru"""
        selected_category = self.height_category.get()
        selected_size = self.height_size.get()
        
        if not selected_category or not selected_size:
            return
            
        # Znajdź odpowiadający zakres
        ranges = self.height_manager.get_ranges_for_category(selected_category)
        
        for min_h, max_h, desc in ranges:
            if desc == selected_size:
                self.height_min_var.set(str(min_h))
                self.height_max_var.set(str(max_h))
                self.set_height_range()
                print(f"🎯 Ustawiono preset: {desc}")
                break

    def _match_suggested_range_new(self, height_range):
        """Sprawdź czy zakres pasuje do któregoś z presetów (nowa wersja)"""
        all_ranges = self.height_manager.get_suggested_ranges()
        
        for category, ranges in all_ranges.items():
            for min_h, max_h, desc in ranges:
                if min_h == height_range.min_height and max_h == height_range.max_height:
                    self.height_category.set(category)
                    self.on_category_selected(None)  # Załaduj rozmiary dla kategorii
                    self.height_size.set(desc)
                    print(f"🎯 Znaleziono pasujący preset: {category} -> {desc}")
                    return
                    
        # Jeśli nie ma dopasowania, wyczyść
        self.height_category.set("")
        self.height_size.set("")
            
    def set_color_from_remote_id(self, remote_id):
        """Ustaw kolor na podstawie remote_id"""
        if remote_id in self.color_by_remote_id:
            color_key = self.color_by_remote_id[remote_id]
            self.select_color(color_key)
            
    def update_product_display(self, product_data, producer_data):
        """Aktualizuj wyświetlanie produktu"""
        # Nazwa produktu
        self.lbl_prod_name.config(text=product_data.get('name', '[Nazwa produktu]'))
        
        # Status producenta
        if producer_data.get('name'):
            self.lbl_producer_present.config(
                bg='#BFE02B',
                text=f"Producent: {producer_data['name']}"
            )
        else:
            self.lbl_producer_present.config(
                bg='#E24B38',
                text="Brak producenta"
            )
            
        self.lbl_producerdesc_present.config(
            bg='#BFE02B' if producer_data.get('description') else '#E24B38'
        )
        
    def update_product_image(self, image_manager, image_path):
        """Aktualizuj obraz produktu używając ImageManager"""
        success = image_manager.load_and_display_image(
            self.lbl_product_image, 
            image_path
        )
        if success:
            image_manager.bind_preview_click(self.lbl_product_image, self.app.root)
        
    def _load_and_display_image(self, image_path):
        """Załaduj i wyświetl obraz produktu"""
        if not image_path:
            self.lbl_product_image.config(text="[Brak obrazu]", image='')
            return
            
        image_url = f"https://www.gsport.pl{image_path}_100.jpg"
        self.image_base_path = f"https://www.gsport.pl{image_path}"
            
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # Oblicz rozmiar
            frame_width = 120
            frame_height = 120
            
            width, height = img.size
            aspect_ratio = width / height
            
            if aspect_ratio > 1:
                new_width = frame_width
                new_height = int(frame_width / aspect_ratio)
            else:
                new_height = frame_height
                new_width = int(frame_height * aspect_ratio)
                
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.lbl_product_image.config(text='', image=photo, cursor="hand2")
            self.lbl_product_image.image = photo
            
            self.lbl_product_image.bind("<Button-1>", lambda e: self._show_image_preview())
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.lbl_product_image.config(text="[Błąd ładowania]", image='', cursor="")
            self.lbl_product_image.unbind("<Button-1>")
            
    def _show_image_preview(self):
        """Pokaż podgląd obrazu"""
        if not hasattr(self, 'image_base_path'):
            return
            
        preview_window = tk.Toplevel(self.app.root)
        preview_window.title("Podgląd obrazu produktu")
        preview_window.geometry("600x600")
        preview_window.configure(bg="#F9F9F9")
        
        # Wycentruj okno
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() - 600) // 2
        y = (preview_window.winfo_screenheight() - 600) // 2
        preview_window.geometry(f"600x600+{x}+{y}")
        
        try:
            large_image_url = f"{self.image_base_path}_500.jpg"
            
            response = requests.get(large_image_url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            max_width = 580
            max_height = 550
            
            width, height = img.size
            aspect_ratio = width / height
            
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
                
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            image_label = tk.Label(preview_window, image=photo, bg="#F9F9F9")
            image_label.image = photo
            image_label.pack(expand=True, pady=10)
            
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
    
            
    def clear_all_fields(self):
        """Wyczyść wszystkie pola"""
        self.lbl_prod_name.config(text="[Nazwa produktu]")
        self.lbl_producer_present.config(bg='#dedede', text="Producent")
        self.lbl_producerdesc_present.config(bg='#dedede')
        self.lbl_product_image.config(text="[Brak obrazu]", image='')
        self.clear_color_selection()
        self.clear_height_range()
        
        for entry in self.similar_product_entries:
            entry.delete(0, 'end')


class ControlPanel:
    """Panel kontrolny z przyciskami akcji"""
    
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        self.create_panel()
        
    def create_panel(self):
        """Utwórz panel kontrolny"""
        control_panel = tk.Frame(self.parent, bg="#FFFFFF", height=110, relief="flat", bd=1)
        control_panel.pack(fill="x", padx=20, pady=(20, 10))
        control_panel.pack_propagate(False)
        
        inner = tk.Frame(control_panel, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=20)
        
        # Sekcja importu danych
        self._create_import_section(inner)
        
        # Sekcja generowania
        self._create_generation_section(inner)
        
        # Sekcja zapisu
        self._create_save_section(inner)
        
        # Wyświetlanie kosztów
        self._create_cost_display(inner)
        
    def _create_import_section(self, parent):
        """Utwórz sekcję importu danych"""
        import_frame = tk.Frame(parent, bg="#FFFFFF")
        import_frame.pack(side="left", padx=(0, 40))
        
        import_label = tk.Label(
            import_frame,
            text="Import danych",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        import_label.pack(anchor="w", pady=(0, 5))
        
        import_buttons = tk.Frame(import_frame, bg="#FFFFFF")
        import_buttons.pack()
        
        self.btn_paste_desc = ttk.Button(
            import_buttons,
            text='Wgraj opis',
            command=self.app.product_manager.paste_description,
            style='Secondary.TButton'
        )
        self.btn_paste_desc.pack(side="left", padx=3)
        
        self.btn_paste_json = ttk.Button(
            import_buttons,
            text='JSON',
            command=self.app.product_manager.paste_specification_json,
            style='Secondary.TButton'
        )
        self.btn_paste_json.pack(side="left", padx=3)
        
        self.btn_paste_spec = ttk.Button(
            import_buttons,
            text='HTML',
            command=self.app.product_manager.paste_specification,
            style='Secondary.TButton'
        )
        self.btn_paste_spec.pack(side="left", padx=3)
        
    def _create_generation_section(self, parent):
        """Utwórz sekcję generowania"""
        gen_frame = tk.Frame(parent, bg="#FFFFFF")
        gen_frame.pack(side="left", padx=(0, 40))
        
        gen_label = tk.Label(
            gen_frame,
            text="Generowanie",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        gen_label.pack(anchor="w", pady=(0, 5))
        
        gen_controls = tk.Frame(gen_frame, bg="#FFFFFF")
        gen_controls.pack()
        
        # Checkbox typu produktu
        self.is_bike_var = tk.BooleanVar(value=True)
        self.chk_is_bike = tk.Checkbutton(
            gen_controls,
            text="Rower",
            variable=self.is_bike_var,
            bg="#FFFFFF",
            font=("Arial", 11, "bold")
        )
        self.chk_is_bike.pack(side="left", padx=(0, 15))
        
        self.btn_generate = ttk.Button(
            gen_controls,
            text='Generuj AI',
            command=self.app.product_manager.generate_description,
            style='Primary.TButton'
        )
        self.btn_generate.pack(side="left")
        
    def _create_save_section(self, parent):
        """Utwórz sekcję zapisu"""
        save_frame = tk.Frame(parent, bg="#FFFFFF")
        save_frame.pack(side="left")
        
        save_label = tk.Label(
            save_frame,
            text="Zapis",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        save_label.pack(anchor="w", pady=(0, 5))
        
        self.btn_update = ttk.Button(
            save_frame,
            text="Zapisz w sklepie",
            command=self.app.product_manager.update_products,
            style='Success.TButton',
            state=tk.DISABLED
        )
        self.btn_update.pack()
        
    def _create_cost_display(self, parent):
        """Utwórz wyświetlanie kosztów"""
        self.lbl_cost = tk.Label(
            parent,
            text="",
            bg="#FFFFFF",
            font=("Arial", 10),
            fg="#666666"
        )
        self.lbl_cost.pack(side="right", padx=20)


class HTMLPreviewManager:
    """Manager podglądu HTML"""
    
    @staticmethod
    def preview_html(content: str, description_type: str = ""):
        """Wyświetl podgląd HTML w przeglądarce"""
        if not content:
            from tkinter import messagebox
            messagebox.showinfo("Info", "Brak treści do podglądu")
            return
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Podgląd opisu {description_type}</title>
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
            
        webbrowser.open(f'file://{temp_path}')


class SyntaxHighlighter:
    """Manager podświetlania składni HTML"""
    
    @staticmethod
    def setup_text_widget(text_widget):
        """Skonfiguruj podświetlanie składni dla widgetu tekstu"""
        text_widget.tag_configure("html_tag", foreground="#0066CC", font=("Consolas", 11, "bold"))
        text_widget.tag_configure("html_attribute", foreground="#009900")
        text_widget.tag_configure("html_value", foreground="#CC0000")
        text_widget.tag_configure("html_content", foreground="#333333")
        
    @staticmethod
    def highlight_syntax(text_widget):
        """Zastosuj podświetlanie składni"""
        import re
        
        # Usuń istniejące tagi
        for tag in ["html_tag", "html_attribute", "html_value"]:
            text_widget.tag_remove(tag, "1.0", "end")
            
        content = text_widget.get("1.0", "end-1c")
        
        # Podświetl tagi HTML
        for match in re.finditer(r'</?(\w+)(?:\s+[^>]*)?>|</\w+>', content):
            start = text_widget.index(f"1.0+{match.start()}c")
            end = text_widget.index(f"1.0+{match.end()}c")
            text_widget.tag_add("html_tag", start, end)
            
        # Podświetl atrybuty i wartości
        for match in re.finditer(r'(\w+)=(["\'])([^"\']*)\2', content):
            # Nazwa atrybutu
            attr_start = text_widget.index(f"1.0+{match.start(1)}c")
            attr_end = text_widget.index(f"1.0+{match.end(1)}c")
            text_widget.tag_add("html_attribute", attr_start, attr_end)
            
            # Wartość atrybutu (z cudzysłowami)
            val_start = text_widget.index(f"1.0+{match.start(2)}c")
            val_end = text_widget.index(f"1.0+{match.end(3)}c")
            text_widget.tag_add("html_value", val_start, val_end)