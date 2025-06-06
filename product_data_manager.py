# product_data_manager.py - rozszerzona wersja
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from height_manager import HeightManager, HeightRange

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
    height_range: Optional[HeightRange] = None

@dataclass
class OriginalOption:
    """Oryginalny parametr z API"""
    name: str
    remote_id: str
    value: str
    type: Optional[str] = None  # dla type="hidden"

class ProductDataManager:
    """Manager danych produktu - centralizuje zarządzanie wszystkimi danymi"""
    
    def __init__(self):
        self.product_data = ProductData()
        self.producer_data = ProducerData()
        self.specifications = ProductSpecifications()
        self.generated_descriptions = GeneratedDescriptions()
        self.parameters = ProductParameters()
        self.processed_ids: List[str] = []
        
        # Manager wzrostu
        self.height_manager = HeightManager()
        
        # Oryginalne parametry z API
        self.original_info_options: List[OriginalOption] = []
        self.original_options: List[OriginalOption] = []
        
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
        
    def extract_original_parameters(self, api_data: Dict[str, Any]) -> None:
        """Wyodrębnij oryginalne parametry z danych API"""
        self.original_info_options.clear()
        self.original_options.clear()
        
        try:
            if 'prod_options' not in api_data:
                return
                
            prod_options = api_data['prod_options']
            
            if not isinstance(prod_options, dict):
                return
                
            # Iteruj po produktach
            for prod_id, product_options in prod_options.items():
                if not isinstance(product_options, dict):
                    continue
                    
                # Iteruj po parametrach produktu
                for param_id, param_data in product_options.items():
                    if not isinstance(param_data, dict):
                        continue
                        
                    param_name = param_data.get('name', '')
                    param_type = param_data.get('type', '')
                    values = param_data.get('values', {})
                    
                    if not isinstance(values, dict):
                        continue
                        
                    # Iteruj po wartościach parametru
                    for value_id, value_data in values.items():
                        if not isinstance(value_data, dict):
                            continue
                            
                        # Sprawdź czy wartość jest wybrana/aktywna
                        # Dla parametrów info - zawsze dodajemy (są to informacje o produkcie)
                        # Dla parametrów choose - tylko wybrane
                        # Dla parametrów hidden - zawsze dodajemy
                        
                        should_include = False
                        
                        if param_type == "info":
                            # Parametry informacyjne - zawsze dodajemy
                            should_include = True
                        elif param_type == "hidden":
                            # Parametry ukryte - zawsze dodajemy
                            should_include = True
                        elif param_type == "choose":
                            # Parametry wyboru - tylko wybrane
                            selected = value_data.get('selected', '')
                            should_include = bool(selected.strip())
                        
                        if should_include:
                            original_option = OriginalOption(
                                name=param_name,
                                remote_id=str(value_id),
                                value=value_data.get('name', ''),
                                type="hidden" if param_type == "hidden" else None
                            )
                            
                            # Dodaj do odpowiedniej listy
                            if param_type == "info":
                                self.original_info_options.append(original_option)
                            elif param_type in ["choose", "hidden"]:
                                self.original_options.append(original_option)

            # Debug output - wypisz pobrane parametry
            print("\n" + "="*60)
            print("POBRANE ORYGINALNE PARAMETRY:")
            print("="*60)
            
            if self.original_info_options:
                print(f"\nINFO_OPTIONS ({len(self.original_info_options)} elementów):")
                for i, option in enumerate(self.original_info_options, 1):
                    print(f"  {i:2d}. {option.name} = '{option.value}' (remote_id: {option.remote_id})")
            else:
                print("\nINFO_OPTIONS: BRAK")
                
            if self.original_options:
                print(f"\nOPTIONS ({len(self.original_options)} elementów):")
                for i, option in enumerate(self.original_options, 1):
                    type_info = f" [type: {option.type}]" if option.type else ""
                    print(f"  {i:2d}. {option.name} = '{option.value}' (remote_id: {option.remote_id}){type_info}")
            else:
                print("\nOPTIONS: BRAK")
                
            print("="*60)
            print()
                                
        except (AttributeError, KeyError, TypeError) as e:
            print(f"Warning: Could not extract original parameters: {e}")
        
    def get_filtered_info_options(self) -> List[OriginalOption]:
        """
        Pobierz oryginalne info_options z wykluczeniem wzrostu
        (wzrost będzie dodany przez nas)
        """
        filtered = []
        for option in self.original_info_options:
            # Wykluczamy wzrost - będziemy go dodawać sami
            if option.name != "Wzrost":
                filtered.append(option)
        return filtered
        
    def get_filtered_options(self) -> List[OriginalOption]:
        """
        Pobierz oryginalne options z wykluczeniem koloru dominującego
        (kolor będzie dodany przez nas jeśli został wybrany)
        """
        filtered = []
        for option in self.original_options:
            # Wykluczamy kolor dominujący - będziemy go dodawać sami
            if option.name != "Kolor dominujący":
                filtered.append(option)
        return filtered
        
    def extract_color_parameter(self, api_data: Dict[str, Any]) -> None:
        """Wyodrębnij parametr koloru z danych API"""
        try:
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
                                
        except (AttributeError, KeyError, TypeError) as e:
            print(f"Warning: Could not extract color parameter: {e}")
            
    def extract_height_parameter(self, api_data: Dict[str, Any]) -> None:
        """Wyodrębnij parametr wzrostu z danych API"""
        height_range = self.height_manager.extract_height_from_api_data(api_data)
        if height_range:
            self.parameters.height_range = height_range
            print(f"✅ Ustawiono zakres wzrostu z API: {height_range.min_height}-{height_range.max_height} cm")
            
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
        
    def set_product_height_range(self, min_height: int, max_height: int) -> bool:
        """
        Ustaw zakres wzrostu produktu
        
        Args:
            min_height: Minimalny wzrost w cm
            max_height: Maksymalny wzrost w cm
            
        Returns:
            True jeśli zakres został ustawiony poprawnie
        """
        success = self.height_manager.set_height_range(min_height, max_height)
        if success:
            self.parameters.height_range = self.height_manager.height_range
        return success
        
    def clear_product_height_range(self) -> None:
        """Wyczyść zakres wzrostu produktu"""
        self.height_manager.clear_height_range()
        self.parameters.height_range = None
        
    def get_height_range_summary(self) -> str:
        """Pobierz podsumowanie zakresu wzrostu"""
        return self.height_manager.get_height_range_summary()
        
    def get_selected_heights_count(self) -> int:
        """Pobierz liczbę wybranych wartości wzrostu"""
        return self.height_manager.get_selected_heights_count()
        
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
        
        # Wyczyść manager wzrostu
        self.height_manager.clear_height_range()
        
        # Wyczyść oryginalne parametry
        self.original_info_options.clear()
        self.original_options.clear()
        
    def add_processed_id(self, product_id: str) -> None:
        """Dodaj ID do listy przetworzonych"""
        if product_id not in self.processed_ids:
            self.processed_ids.append(product_id)