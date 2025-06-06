# product_data_manager.py
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class ProductData:
    """Dane produktu"""
    product_id: str = ""
    name: str = ""
    description: str = ""
    image: str = ""

@dataclass
class ProducerData:
    """Dane producenta"""
    name: str = ""
    logo: str = ""
    description: str = ""

@dataclass
class ProductSpecifications:
    """Specyfikacje produktu"""
    json: str = ""
    html: str = ""

@dataclass
class GeneratedDescriptions:
    """Wygenerowane opisy"""
    long: str = ""
    short: str = ""

@dataclass
class ProductParameters:
    """Parametry produktu"""
    color: Optional[str] = None
    color_remote_id: Optional[str] = None

class ProductDataManager:
    """Manager danych produktu - centralizuje zarządzanie wszystkimi danymi"""
    
    def __init__(self):
        self.product_data = ProductData()
        self.producer_data = ProducerData()
        self.specifications = ProductSpecifications()
        self.generated_descriptions = GeneratedDescriptions()
        self.parameters = ProductParameters()
        self.processed_ids: List[str] = []
        
    def set_product_data(self, api_data: Dict[str, Any]) -> None:
        """Ustaw dane produktu z odpowiedzi API"""
        self.product_data = ProductData(
            name=api_data.get("prod_name", "Brak nazwy"),
            description=api_data.get("prod_desclong", "Brak opisu"),
            image=api_data.get("prod_img_src", "")
        )
        
    def set_producer_data(self, api_data: Dict[str, Any]) -> None:
        """Ustaw dane producenta z odpowiedzi API"""
        self.producer_data = ProducerData(
            name=api_data.get("prd_name", ""),
            logo=api_data.get("prd_logo", ""),
            description=api_data.get("prd_link_text", "")
        )
        
    def extract_color_parameter(self, api_data: Dict[str, Any]) -> None:
        """Wyodrębnij parametr koloru z danych API"""
        if 'prod_options' not in api_data:
            return
        
        prod_options = api_data['prod_options']
        
        # Sprawdź czy prod_options to słownik czy lista
        if isinstance(prod_options, list):
            # Jeśli to lista, znaczy że nie ma parametrów lub jest pusta
            return
        
        if not isinstance(prod_options, dict):
            # Jeśli to ani lista, ani słownik, to też kończymy
            return
            
        # Teraz bezpiecznie iterujemy po słowniku
        for prod_id, options in prod_options.items():
            if not isinstance(options, dict):
                continue
                
            for opt_id, option in options.items():
                if not isinstance(option, dict):
                    continue
                    
                if (option.get('name') == 'Kolor dominujący' and 
                    option.get('type') == 'choose'):
                    
                    values = option.get('values', {})
                    if not isinstance(values, dict):
                        continue
                        
                    for value_id, value_data in values.items():
                        if isinstance(value_data, dict) and value_data.get('selected'):
                            self.parameters.color = value_data.get('name', '')
                            self.parameters.color_remote_id = str(value_id)
                            return
                            
    def set_specification(self, spec_type: str, content: str) -> None:
        """Ustaw specyfikację określonego typu"""
        if spec_type == 'json':
            self.specifications.json = content
        elif spec_type == 'html':
            self.specifications.html = content
            
    def set_generated_description(self, desc_type: str, content: str) -> None:
        """Ustaw wygenerowany opis określonego typu"""
        if desc_type == 'long':
            self.generated_descriptions.long = content
        elif desc_type == 'short':
            self.generated_descriptions.short = content
            
    def set_product_color(self, color_key: Optional[str], remote_id: Optional[str]) -> None:
        """Ustaw kolor produktu"""
        self.parameters.color = color_key
        self.parameters.color_remote_id = remote_id
        
    def get_producer_section_html(self) -> str:
        """Pobierz HTML sekcji producenta"""
        if self.producer_data.name and self.producer_data.description:
            return (
                f"<h2>O marce {self.producer_data.name}</h2>"
                f"<p>{self.producer_data.description}</p>"
            )
        return ""
        
    def has_producer_info(self) -> bool:
        """Sprawdź czy są informacje o producencie"""
        return bool(self.producer_data.name)
        
    def has_producer_description(self) -> bool:
        """Sprawdź czy jest opis producenta"""
        return bool(self.producer_data.description)
        
    def clear_all_data(self) -> None:
        """Wyczyść wszystkie dane"""
        self.product_data = ProductData()
        self.producer_data = ProducerData()
        self.specifications = ProductSpecifications()
        self.generated_descriptions = GeneratedDescriptions()
        self.parameters = ProductParameters()
        self.processed_ids.clear()
        
    def add_processed_id(self, product_id: str) -> None:
        """Dodaj ID do listy przetworzonych"""
        if product_id not in self.processed_ids:
            self.processed_ids.append(product_id)