# image_manager.py
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from typing import Optional, Tuple

class ImageManager:
    """Manager obrazów produktów"""
    
    def __init__(self):
        self.image_base_path: Optional[str] = None
        
    def load_and_display_image(self, image_label: tk.Label, image_path: str, 
                             frame_width: int = 120, frame_height: int = 120) -> bool:
        """
        Załaduj i wyświetl obraz produktu w miniaturze
        
        Args:
            image_label: Label do wyświetlenia obrazu
            image_path: Ścieżka do obrazu
            frame_width: Szerokość ramki
            frame_height: Wysokość ramki
            
        Returns:
            True jeśli obraz został załadowany pomyślnie
        """
        if not image_path:
            image_label.config(text="[Brak obrazu]", image='', cursor="")
            if hasattr(image_label, 'unbind'):
                image_label.unbind("<Button-1>")
            return False
            
        # Konstruuj URL obrazu (miniatura 100px)
        image_url = f"https://www.gsport.pl{image_path}_100.jpg"
        self.image_base_path = f"https://www.gsport.pl{image_path}"
        
        try:
            # Pobierz obraz
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Otwórz obraz z PIL
            img = Image.open(BytesIO(response.content))
            
            # Oblicz rozmiar zachowując proporcje
            new_width, new_height = self._calculate_image_size(
                img.size, frame_width, frame_height
            )
            
            # Zmień rozmiar obrazu
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Konwertuj do PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Aktualizuj label
            image_label.config(text='', image=photo, cursor="hand2")
            image_label.image = photo  # Zachowaj referencję
            
            return True
            
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text="[Błąd ładowania]", image='', cursor="")
            return False
            
    def _calculate_image_size(self, original_size: Tuple[int, int], 
                            max_width: int, max_height: int) -> Tuple[int, int]:
        """
        Oblicz nowy rozmiar obrazu zachowując proporcje
        
        Args:
            original_size: Oryginalny rozmiar (width, height)
            max_width: Maksymalna szerokość
            max_height: Maksymalna wysokość
            
        Returns:
            Nowy rozmiar (width, height)
        """
        width, height = original_size
        aspect_ratio = width / height
        
        if aspect_ratio > 1:  # Szerszy niż wysoki
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:  # Wyższy niż szeroki
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
            
        return new_width, new_height
        
    def show_image_preview(self, parent_window: tk.Tk) -> None:
        """
        Pokaż podgląd obrazu w większym rozmiarze
        
        Args:
            parent_window: Okno rodzic
        """
        if not self.image_base_path:
            return
            
        preview_window = tk.Toplevel(parent_window)
        preview_window.title("Podgląd obrazu produktu")
        preview_window.geometry("600x600")
        preview_window.configure(bg="#F9F9F9")
        
        # Wycentruj okno
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() - 600) // 2
        y = (preview_window.winfo_screenheight() - 600) // 2
        preview_window.geometry(f"600x600+{x}+{y}")
        
        try:
            # Użyj większego obrazu (500px szerokości)
            large_image_url = f"{self.image_base_path}_500.jpg"
            
            # Pobierz obraz
            response = requests.get(large_image_url, timeout=10)
            response.raise_for_status()
            
            # Otwórz obraz z PIL
            img = Image.open(BytesIO(response.content))
            
            # Oblicz rozmiar dla okna podglądu
            max_width = 580
            max_height = 550
            
            width, height = img.size
            new_width, new_height = self._calculate_image_size(
                (width, height), max_width, max_height
            )
            
            # Zmień rozmiar tylko jeśli konieczne
            if width > max_width or height > max_height:
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Konwertuj do PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Utwórz label dla obrazu
            image_label = tk.Label(preview_window, image=photo, bg="#F9F9F9")
            image_label.image = photo  # Zachowaj referencję
            image_label.pack(expand=True, pady=10)
            
            # Dodaj przycisk zamknięcia
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
            
    def bind_preview_click(self, image_label: tk.Label, parent_window: tk.Tk) -> None:
        """
        Powiąż kliknięcie obrazu z podglądem
        
        Args:
            image_label: Label z obrazem
            parent_window: Okno rodzic
        """
        image_label.bind("<Button-1>", lambda e: self.show_image_preview(parent_window))