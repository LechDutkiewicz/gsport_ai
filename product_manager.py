# product_manager.py - Refaktoryzowany
from tkinter import messagebox
import tkinter as tk
from typing import List

from config import (
    GSPORT_API_URL, 
    GPT_API_KEY, 
    GSPORT_API_KEY, 
    MAX_TOKENS, 
    MODEL
)
from utils import extract_product_id, save_xml_copy
from api_client import GSportAPIClient, OpenAIClient
from product_data_manager import ProductDataManager
from image_manager import ImageManager
from ai_description_generator import AIDescriptionGenerator
from xml_builder import XMLBuilder

class ProductManager:
    """Główny manager produktów - koordynuje wszystkie operacje"""
    
    def __init__(self, app):
        self.app = app
        
        # Inicjalizuj klientów API
        self.gsport_client = GSportAPIClient(GSPORT_API_URL, GSPORT_API_KEY)
        self.openai_client = OpenAIClient(GPT_API_KEY, MODEL, MAX_TOKENS)
        
        # Inicjalizuj managery
        self.data_manager = ProductDataManager()
        self.image_manager = ImageManager()
        self.ai_generator = AIDescriptionGenerator(self.openai_client)
        
        # ID aktualnego produktu
        self.current_product_id = None
        
    def load_product_data(self):
        """Załaduj dane produktu na podstawie input"""
        input_text = self.app.product_info_panel.input_product_link.get().strip()
        if not input_text:
            return
            
        product_id = extract_product_id(input_text)
        if not product_id:
            return
            
        # Wyczyść pola przed załadowaniem nowych danych
        self.clear_all_fields()
        
        self.current_product_id = product_id
        self.data_manager.product_data.product_id = product_id
        
        try:
            # Pobierz dane produktu
            api_data = self.gsport_client.get_product_data(product_id)
            
            if not api_data:
                messagebox.showinfo("Brak danych", "Nie znaleziono danych dla podanego ID.")
                return
                
            # Ustaw dane w managerze
            self.data_manager.set_product_data(api_data)
            self.data_manager.set_producer_data(api_data)
            self.data_manager.extract_original_parameters(api_data)
            self.data_manager.extract_color_parameter(api_data)
            self.data_manager.extract_height_parameter(api_data)
            
            # Aktualizuj UI
            self._update_ui_with_product_data()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać danych produktu: {str(e)}")

    def load_product_data_preserve_ai(self):
        """Załaduj dane produktu zachowując wygenerowane opisy AI"""
        input_text = self.app.product_info_panel.input_product_link.get().strip()
        if not input_text:
            return
            
        product_id = extract_product_id(input_text)
        if not product_id:
            return
            
        # Zachowaj wygenerowane opisy AI przed czyszczeniem
        preserved_long_desc = self.data_manager.generated_descriptions.long
        preserved_short_desc = self.data_manager.generated_descriptions.short
        
        # Wyczyść wszystkie pola OPRÓCZ opisów AI
        self._clear_fields_except_ai()
        
        self.current_product_id = product_id
        self.data_manager.product_data.product_id = product_id
        
        try:
            # Pobierz dane produktu
            api_data = self.gsport_client.get_product_data(product_id)
            
            if not api_data:
                messagebox.showinfo("Brak danych", "Nie znaleziono danych dla podanego ID.")
                return
                
            # Ustaw dane w managerze
            self.data_manager.set_product_data(api_data)
            self.data_manager.set_producer_data(api_data)
            self.data_manager.extract_original_parameters(api_data)
            self.data_manager.extract_color_parameter(api_data)
            self.data_manager.extract_height_parameter(api_data)
            
            # Przywróć zachowane opisy AI
            self.data_manager.set_generated_description('long', preserved_long_desc)
            self.data_manager.set_generated_description('short', preserved_short_desc)
            
            # Aktualizuj UI
            self._update_ui_with_product_data()
            
            # Przywróć opisy AI w UI
            if preserved_long_desc:
                self.app.content_area.set_text_content('long', preserved_long_desc)
            if preserved_short_desc:
                self.app.content_area.set_text_content('short', preserved_short_desc)
                
            # Włącz przycisk aktualizacji jeśli są opisy AI
            # if preserved_long_desc or preserved_short_desc:
                # self.app.enable_update_button()
                
            print(f"✅ Załadowano produkt {product_id} zachowując opisy AI")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać danych produktu: {str(e)}")
            
    def _clear_fields_except_ai(self):
        """Wyczyść pola z wyjątkiem opisów AI"""
        # Wyczyść panel informacji o produkcie
        self.app.product_info_panel.lbl_prod_name.config(text="[Nazwa produktu]")
        self.app.product_info_panel.lbl_producer_present.config(bg='#dedede', text="Producent")
        self.app.product_info_panel.lbl_producerdesc_present.config(bg='#dedede')
        self.app.product_info_panel.lbl_product_image.config(text="[Brak obrazu]", image='')
        self.app.product_info_panel.clear_color_selection()
        self.app.product_info_panel.clear_height_range()
        
        # Wyczyść podobne produkty
        for entry in self.app.product_info_panel.similar_product_entries:
            entry.delete(0, 'end')
            
        # Wyczyść opis oryginalny i specyfikacje
        self.app.content_area.load_html_content('html_original_desc', "")
        self.app.content_area.load_html_content('html_spec_json', "")
        self.app.content_area.load_html_content('html_spec_html', "")
        
        # Wyczyść dane w managerze (oprócz opisów AI)
        preserved_long = self.data_manager.generated_descriptions.long
        preserved_short = self.data_manager.generated_descriptions.short
        
        self.data_manager.clear_all_data()
        
        # Przywróć opisy AI
        self.data_manager.set_generated_description('long', preserved_long)
        self.data_manager.set_generated_description('short', preserved_short)
            
    def _update_ui_with_product_data(self):
        """Aktualizuj UI z danymi produktu"""
        # Aktualizuj panel informacji o produkcie
        self.app.product_info_panel.update_product_display(
            self.data_manager.product_data.__dict__,
            self.data_manager.producer_data.__dict__
        )
        
        # Załaduj i wyświetl obraz
        success = self.image_manager.load_and_display_image(
            self.app.product_info_panel.lbl_product_image,
            self.data_manager.product_data.image
        )
        
        # Powiąż kliknięcie obrazu z podglądem
        if success:
            self.image_manager.bind_preview_click(
                self.app.product_info_panel.lbl_product_image,
                self.app.root
            )
        
        # Ustaw kolor jeśli został wyodrębniony
        if self.data_manager.parameters.color_remote_id:
            self.app.product_info_panel.set_color_from_remote_id(
                self.data_manager.parameters.color_remote_id
            )

        # Ustaw wzrost jeśli został wyodrębniony
        if self.data_manager.parameters.height_range:
            self.app.product_info_panel.update_height_display_from_api()
        
        # Wyświetl opis produktu
        self.app.content_area.load_html_content(
            'html_original_desc',
            f"<html><body>{self.data_manager.product_data.description}</body></html>"
        )
        
    def paste_description(self):
        """Wklej opis ze schowka"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.data_manager.product_data.description = clipboard_content
            self.app.content_area.load_html_content(
                'html_original_desc',
                f"<html><body>{clipboard_content}</body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def paste_specification_json(self):
        """Wklej specyfikację JSON ze schowka"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.data_manager.set_specification('json', clipboard_content)
            self.app.content_area.load_html_content(
                'html_spec_json',
                f"<html><body><pre>{clipboard_content}</pre></body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def paste_specification(self):
        """Wklej specyfikację HTML ze schowka"""
        try:
            clipboard_content = self.app.root.clipboard_get()
            self.data_manager.set_specification('html', clipboard_content)
            self.app.content_area.load_html_content(
                'html_spec_html',
                f"<html><body>{clipboard_content}</body></html>"
            )
        except:
            messagebox.showwarning("Błąd", "Nie można odczytać zawartości schowka")
            
    def generate_description(self):
        """Generuj opis produktu przy użyciu AI"""
        if not self.data_manager.product_data.name:
            messagebox.showwarning("Błąd", "Najpierw załaduj dane produktu")
            return
            
        # Sprawdź czy to rower na podstawie checkboxa
        is_bike = self.app.control_panel.is_bike_var.get()
        
        try:
            # Generuj opisy
            result = self.ai_generator.generate_descriptions(self.data_manager, is_bike)
            
            if result['success']:
                # Wyświetl długi opis
                self.app.content_area.set_text_content('long', result['long_description'])
                
                # Wyświetl krótki opis jeśli został wygenerowany
                if result.get('short_description'):
                    self.app.content_area.set_text_content('short', result['short_description'])
                
                # Aktualizuj wyświetlanie kosztów
                cost = result['cost'] * 100
                self.app.update_cost_display(f"Koszt: {cost:.5f}¢ USD")
                
                # Włącz przycisk aktualizacji
                # self.app.enable_update_button()
                
                print(f"Użyto pliku z promptem: {result.get('prompt_file', 'unknown')}")
                
            else:
                messagebox.showerror("Błąd", result['error'])
                
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas generowania opisu: {str(e)}")

    def load_original_description(self):
        """Wczytaj oryginalny opis produktu do edytora AI"""
        if not self.data_manager.product_data.description:
            messagebox.showwarning("Błąd", "Brak oryginalnego opisu produktu")
            return
            
        original_desc = self.data_manager.product_data.description.strip()
        
        if not original_desc:
            messagebox.showwarning("Błąd", "Oryginalny opis produktu jest pusty")
            return
            
        # Wczytaj oryginalny opis do długiego opisu AI
        self.app.content_area.set_text_content('long', original_desc)
        
        # Zapisz w managerze
        self.data_manager.set_generated_description('long', original_desc)
        
        # Wyczyść krótki opis
        self.app.content_area.set_text_content('short', '')
        self.data_manager.set_generated_description('short', '')
        
        print(f"📋 Wczytano oryginalny opis produktu do edytora ({len(original_desc)} znaków)")
        
        messagebox.showinfo(
            "Sukces", 
            f"Wczytano oryginalny opis produktu do edytora.\n"
            f"Długość: {len(original_desc)} znaków\n\n"
            f"Możesz teraz edytować opis i zapisać w sklepie."
        )
            
    def update_products(self):
        """Aktualizuj produkty w systemie"""
        if not self.current_product_id:
            messagebox.showwarning("Błąd", "Brak danych do zapisania")
            return
            
        # Pobierz aktualną treść z widgetów tekstowych
        long_desc = self.app.content_area.get_text_content('long')
        short_desc = self.app.content_area.get_text_content('short')
        
        # Walidacja
        if not long_desc.strip():
            response = messagebox.askyesno(
                "Brak długiego opisu", 
                "Długi opis jest pusty. Czy na pewno chcesz zapisać produkt bez opisu?\n\n"
                "Możesz:\n"
                "• Wygenerować opis AI\n"
                "• Wczytać opis oryginalny\n"
                "• Napisać własny opis"
            )
            if not response:
                return
            
        # Aktualizuj dane w managerze
        self.data_manager.set_generated_description('long', long_desc)
        self.data_manager.set_generated_description('short', short_desc)
        
        try:
            # Aktualizuj główny produkt
            success = self._update_single_product(self.current_product_id)
            
            if success:
                self.data_manager.add_processed_id(self.current_product_id)
                
            # Aktualizuj podobne produkty jeśli istnieją
            similar_ids = self._get_similar_product_ids()
            for similar_id in similar_ids:
                if self._update_single_product(similar_id):
                    self.data_manager.add_processed_id(similar_id)
                    
            messagebox.showinfo(
                "Sukces", 
                f"Zaktualizowano produkty: {', '.join(self.data_manager.processed_ids)}"
            )
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas aktualizacji: {str(e)}")
            
    def _get_similar_product_ids(self) -> List[str]:
        """Pobierz ID podobnych produktów z UI"""
        similar_ids = []
        
        if hasattr(self.app.product_info_panel, 'similar_product_entries'):
            for entry in self.app.product_info_panel.similar_product_entries:
                similar_url = entry.get().strip()
                if similar_url:
                    similar_id = extract_product_id(similar_url)
                    if similar_id:
                        similar_ids.append(similar_id)
                        
        return similar_ids
        
    def _update_single_product(self, product_id: str) -> bool:
        """Aktualizuj pojedynczy produkt"""
        
        # DODAJ DEBUG INFO:
        print(f"\n📤 GENEROWANIE XML DLA PRODUKTU {product_id}:")
        
        # Debug opisów
        long_desc = self.data_manager.generated_descriptions.long.strip()
        short_desc = self.data_manager.generated_descriptions.short.strip()
        
        if long_desc:
            print(f"   - Długi opis: BĘDZIE NADPISANY ({len(long_desc)} znaków)")
        else:
            print(f"   - Długi opis: ZOSTANIE BEZ ZMIAN (pusty)")
            
        if short_desc:
            print(f"   - Krótki opis: BĘDZIE NADPISANY ({len(short_desc)} znaków)")
        else:
            print(f"   - Krótki opis: ZOSTANIE BEZ ZMIAN (pusty)")
        
        # Debug parametrów
        print(f"   - Info options: {len(self.data_manager.original_info_options)} oryginalnych")
        if self.data_manager.height_manager.height_range:
            height_count = self.data_manager.get_selected_heights_count()
            height_summary = self.data_manager.get_height_range_summary()
            print(f"   - Wzrost: {height_count} nowych wartości ({height_summary})")
        else:
            print(f"   - Wzrost: BRAK nowych wartości")
        print(f"   - Options: {len(self.data_manager.original_options)} oryginalnych")
        if self.data_manager.parameters.color:
            print(f"   - Kolor: {self.data_manager.parameters.color}")
        else:
            print(f"   - Kolor: BRAK zmiany")
        print()
        
        # Zbuduj XML
        xml_content = XMLBuilder.build_product_xml(product_id, self.data_manager)
        
        # Wyślij aktualizację
        success = self.gsport_client.update_product(xml_content)
        
        # Zapisz kopię XML
        status = "ok" if success else "errors"
        save_xml_copy(xml_content, product_id, f"output/{status}")
        
        return success
        
    def set_product_color(self, color_key, remote_id):
        """Ustaw wybrany kolor produktu"""
        self.data_manager.set_product_color(color_key, remote_id)
        print(f"Color set: {color_key} (remote_id: {remote_id})")
        
    def clear_all_fields(self):
        """Wyczyść wszystkie pola i zresetuj stan"""
        # Zresetuj ID
        self.current_product_id = None
        
        # Wyczyść dane
        self.data_manager.clear_all_data()
        
        # Wyczyść UI przez główną aplikację
        self.app.clear_all_fields()