# ai_description_generator.py
import os
from typing import Dict, Any, Tuple, Optional
from bs4 import BeautifulSoup
from api_client import OpenAIClient
from product_data_manager import ProductDataManager

class PromptSelector:
    """Selektor odpowiedniego promptu na podstawie typu produktu i dostępnych danych"""
    
    @staticmethod
    def select_prompt_and_spec(data_manager: ProductDataManager, is_bike: bool) -> Tuple[str, str]:
        """
        Wybierz odpowiedni plik promptu i specyfikację
        
        Args:
            data_manager: Manager danych produktu
            is_bike: Czy produkt to rower
            
        Returns:
            Tuple (nazwa_pliku_promptu, specyfikacja)
        """
        specification = data_manager.specifications.html
        
        if is_bike:
            return PromptSelector._select_bike_prompt(data_manager, specification)
        else:
            return PromptSelector._select_non_bike_prompt(data_manager, specification)
            
    @staticmethod
    def _select_bike_prompt(data_manager: ProductDataManager, specification: str) -> Tuple[str, str]:
        """Wybierz prompt dla rowerów"""
        if data_manager.specifications.json:
            return "prompt_newdesc_99spokes.txt", data_manager.specifications.json
        elif data_manager.producer_data.name == "SCOTT" and not specification:
            return "prompt_newdesc_scott.txt", ""
        elif specification:
            return "prompt_newdesc_with_specs.txt", specification
        else:
            return "prompt_newdesc.txt", ""
            
    @staticmethod
    def _select_non_bike_prompt(data_manager: ProductDataManager, specification: str) -> Tuple[str, str]:
        """Wybierz prompt dla produktów nie-rowerowych"""
        if data_manager.specifications.json and data_manager.producer_data.name == "Micro":
            return "prompt_newdesc_micro.txt", data_manager.specifications.json
        elif data_manager.specifications.json and data_manager.producer_data.name == "Leatt":
            return "prompt_newdesc_leatt.txt", data_manager.specifications.json
        elif data_manager.specifications.json or specification:
            return "prompt_newdesc_notbike_with_specs.txt", specification or data_manager.specifications.json
        else:
            return "prompt_newdesc_notbike.txt", ""


class PromptProcessor:
    """Procesor plików promptów"""
    
    @staticmethod
    def load_and_prepare_prompt(prompt_file: str, data_manager: ProductDataManager, 
                              specification: str) -> str:
        """
        Załaduj i przygotuj prompt z pliku
        
        Args:
            prompt_file: Nazwa pliku promptu
            data_manager: Manager danych produktu
            specification: Specyfikacja produktu
            
        Returns:
            Przygotowany prompt
        """
        # Sprawdź folder prompts, potem root dla kompatybilności wstecznej
        prompt_path = os.path.join('prompts', prompt_file) if os.path.exists(
            os.path.join('prompts', prompt_file)
        ) else prompt_file
        
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                prompt = file.read().replace("\n", "")
        except FileNotFoundError:
            print(f"Warning: {prompt_file} not found, using default prompt")
            prompt = PromptProcessor._get_default_prompt()
            
        # Zastąp zmienne w prompcie
        prompt = prompt.replace("{prod_name}", data_manager.product_data.name)
        prompt = prompt.replace("{prod_desclongription}", data_manager.product_data.description)
        prompt = prompt.replace("{product_specification}", specification)
        
        return prompt
        
    @staticmethod
    def _get_default_prompt() -> str:
        """Pobierz domyślny prompt jeśli plik nie istnieje"""
        return """### CEL ###
Chcę, żebyś był ekspertem od copywritingu e-commerce i napisał opis produktu dla {prod_name}.

### OPIS ###
{prod_desclongription}

### SPECYFIKACJA ###
{product_specification}"""


class ShortDescriptionGenerator:
    """Generator krótkich opisów na podstawie długich opisów"""
    
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        
    def generate_short_description(self, long_description: str, is_bike: bool) -> Optional[Dict[str, Any]]:
        """
        Generuj krótki opis na podstawie długiego opisu
        
        Args:
            long_description: Długi opis HTML
            is_bike: Czy produkt to rower
            
        Returns:
            Wynik generowania lub None w przypadku błędu
        """
        try:
            # Parsuj długi opis w poszukiwaniu pierwszej listy <ul>
            soup = BeautifulSoup(long_description, 'html.parser')
            first_ul = soup.find('ul')
            
            if not first_ul:
                return None
                
            # Wybierz odpowiedni prompt
            prompt_file = "prompt_shortdesc.txt" if is_bike else "prompt_shortdesc_short.txt"
            
            # Sprawdź folder prompts, potem root
            prompt_path = os.path.join('prompts', prompt_file) if os.path.exists(
                os.path.join('prompts', prompt_file)
            ) else prompt_file
            
            with open(prompt_path, "r", encoding="utf-8") as file:
                prompt = file.read().replace("\n", "")
                prompt = prompt.replace("{prod_desclongription}", str(first_ul))
                
            # Generuj krótki opis
            return self.openai_client.generate_content(prompt)
            
        except Exception as e:
            print(f"Error generating short description: {e}")
            return None


class AIDescriptionGenerator:
    """Główny generator opisów AI"""
    
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.short_desc_generator = ShortDescriptionGenerator(openai_client)
        
    def generate_descriptions(self, data_manager: ProductDataManager, 
                            is_bike: bool) -> Dict[str, Any]:
        """
        Generuj kompletne opisy produktu (długi i krótki)
        
        Args:
            data_manager: Manager danych produktu
            is_bike: Czy produkt to rower
            
        Returns:
            Słownik z wynikami generowania
        """
        try:
            # Wybierz prompt i specyfikację
            prompt_file, specification = PromptSelector.select_prompt_and_spec(
                data_manager, is_bike
            )
            
            # Załaduj i przygotuj prompt
            prompt = PromptProcessor.load_and_prepare_prompt(
                prompt_file, data_manager, specification
            )
            
            # Generuj długi opis
            long_desc_result = self.openai_client.generate_content(prompt)
            
            if not long_desc_result['success']:
                return {
                    'success': False,
                    'error': f"Błąd generowania długiego opisu: {long_desc_result['error']}",
                    'cost': 0
                }
            
            # Zapisz długi opis
            long_description = long_desc_result['content']
            
            # Dodaj sekcję producenta jeśli dostępna
            producer_section = data_manager.get_producer_section_html()
            if producer_section:
                long_description += producer_section
                
            data_manager.set_generated_description('long', long_description)
            
            total_cost = long_desc_result['cost']
            
            # Generuj krótki opis
            short_desc_result = self.short_desc_generator.generate_short_description(
                long_description, is_bike
            )
            
            if short_desc_result and short_desc_result['success']:
                data_manager.set_generated_description('short', short_desc_result['content'])
                total_cost += short_desc_result.get('cost', 0)
            
            return {
                'success': True,
                'long_description': long_description,
                'short_description': data_manager.generated_descriptions.short,
                'cost': total_cost,
                'prompt_file': prompt_file
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Wystąpił błąd podczas generowania opisów: {str(e)}",
                'cost': 0
            }