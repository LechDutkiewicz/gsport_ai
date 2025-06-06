# height_manager.py
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class HeightRange:
    """Zakres wzrostu"""
    min_height: int
    max_height: int
    
    def __post_init__(self):
        """Walidacja po inicjalizacji"""
        if self.min_height > self.max_height:
            self.min_height, self.max_height = self.max_height, self.min_height

class HeightManager:
    """Manager do zarządzania parametrem wzrostu"""
    
    # Mapowanie wzrostu do remote_id na podstawie XML
    HEIGHT_TO_REMOTE_ID = {
        82: "26031", 83: "26030", 84: "26029", 85: "26028", 86: "26027", 87: "26026",
        88: "26025", 89: "26024", 90: "26023", 91: "26022", 92: "26021", 93: "26020",
        94: "26019", 95: "25963", 96: "25964", 97: "25965", 98: "25966", 99: "25967",
        100: "25968", 101: "25969", 102: "25970", 103: "25971", 104: "25972", 105: "25973",
        106: "25974", 107: "25975", 108: "25976", 109: "25977", 110: "25978", 111: "25979",
        112: "25980", 113: "25981", 114: "25982", 115: "25983", 116: "25984", 117: "25985",
        118: "25986", 119: "25987", 120: "25988", 121: "25989", 122: "25990", 123: "25991",
        124: "25992", 125: "25993", 126: "25994", 127: "25995", 128: "25996", 129: "25997",
        130: "25998", 131: "25999", 132: "26000", 133: "26001", 134: "26002", 135: "26003",
        136: "26004", 137: "26005", 138: "26006", 139: "26007", 140: "23503", 141: "23504",
        142: "23505", 143: "23506", 144: "23507", 145: "23508", 146: "23509", 147: "23510",
        148: "23511", 149: "23512", 150: "23513", 151: "23514", 152: "23515", 153: "23516",
        154: "23517", 155: "23518", 156: "23519", 157: "23520", 158: "23521", 159: "23522",
        160: "23523", 161: "23524", 162: "23525", 163: "23526", 164: "23527", 165: "23528",
        166: "23529", 167: "23530", 168: "23531", 169: "23532", 170: "23533", 171: "23534",
        172: "23535", 173: "23536", 174: "23537", 175: "23538", 176: "23539", 177: "23540",
        178: "23541", 179: "23542", 180: "23543", 181: "23544", 182: "23545", 183: "23546",
        184: "23547", 185: "23548", 186: "23549", 187: "23550", 188: "23551", 189: "23552",
        190: "23554", 191: "23555", 192: "23556", 193: "23557", 194: "23558", 195: "23559",
        196: "23560", 197: "23561", 198: "23562", 199: "23563", 200: "23564", 201: "23565",
        202: "23567", 203: "23568", 204: "23569", 205: "23570"
    }
    
    # Odwrotne mapowanie dla szybkiego wyszukiwania
    REMOTE_ID_TO_HEIGHT = {v: k for k, v in HEIGHT_TO_REMOTE_ID.items()}
    
    # Zakres dostępnych wzrostów
    MIN_HEIGHT = min(HEIGHT_TO_REMOTE_ID.keys())
    MAX_HEIGHT = max(HEIGHT_TO_REMOTE_ID.keys())
    
    def __init__(self):
        self.height_range: Optional[HeightRange] = None
        
    def set_height_range(self, min_height: int, max_height: int) -> bool:
        """
        Ustaw zakres wzrostu
        
        Args:
            min_height: Minimalny wzrost w cm
            max_height: Maksymalny wzrost w cm
            
        Returns:
            True jeśli zakres jest prawidłowy
        """
        # Walidacja
        if not self.is_valid_height(min_height) or not self.is_valid_height(max_height):
            return False
            
        if min_height > max_height:
            min_height, max_height = max_height, min_height
            
        self.height_range = HeightRange(min_height, max_height)
        return True
        
    def clear_height_range(self) -> None:
        """Wyczyść zakres wzrostu"""
        self.height_range = None
        
    def get_height_values_for_xml(self) -> List[Dict[str, str]]:
        """
        Pobierz listę wartości wzrostu do XML
        
        Returns:
            Lista słowników z danymi do XML
        """
        if not self.height_range:
            return []
            
        height_options = []
        
        for height in range(self.height_range.min_height, self.height_range.max_height + 1):
            if height in self.HEIGHT_TO_REMOTE_ID:
                height_options.append({
                    'name': 'Wzrost',
                    'remote_id': self.HEIGHT_TO_REMOTE_ID[height],
                    'value': str(height)
                })
                
        return height_options
        
    def get_height_range_summary(self) -> str:
        """
        Pobierz podsumowanie zakresu wzrostu
        
        Returns:
            String z podsumowaniem lub pusty string
        """
        if not self.height_range:
            return ""
            
        return f"{self.height_range.min_height}-{self.height_range.max_height} cm"
        
    def get_selected_heights_count(self) -> int:
        """
        Pobierz liczbę wybranych wartości wzrostu
        
        Returns:
            Liczba wartości w zakresie
        """
        if not self.height_range:
            return 0
            
        count = 0
        for height in range(self.height_range.min_height, self.height_range.max_height + 1):
            if height in self.HEIGHT_TO_REMOTE_ID:
                count += 1
                
        return count
        
    def is_valid_height(self, height: int) -> bool:
        """
        Sprawdź czy wzrost jest prawidłowy
        
        Args:
            height: Wzrost w cm
            
        Returns:
            True jeśli wzrost jest w dostępnym zakresie
        """
        return height in self.HEIGHT_TO_REMOTE_ID
        
    def get_available_heights(self) -> List[int]:
        """
        Pobierz listę dostępnych wzrostów
        
        Returns:
            Posortowana lista dostępnych wzrostów
        """
        return sorted(self.HEIGHT_TO_REMOTE_ID.keys())
        
    def extract_height_from_api_data(self, api_data: Dict) -> Optional[HeightRange]:
        """
        Wyodrębnij zakres wzrostu z danych API (jeśli jest ustawiony)
        
        Args:
            api_data: Dane z API
            
        Returns:
            HeightRange jeśli znaleziony, None w przeciwnym razie
        """
        try:
            if 'prod_options' not in api_data:
                return None
                
            prod_options = api_data['prod_options']
            
            if not isinstance(prod_options, dict):
                return None
                
            selected_heights = []
            
            # Iteruj po produktach
            for prod_id, product_options in prod_options.items():
                if not isinstance(product_options, dict):
                    continue
                    
                # Iteruj po parametrach produktu
                for param_id, param_data in product_options.items():
                    if not isinstance(param_data, dict):
                        continue
                        
                    # Sprawdź czy to parametr wzrostu
                    if param_data.get('name') == 'Wzrost' and param_data.get('type') == 'info':
                        values = param_data.get('values', {})
                        if not isinstance(values, dict):
                            continue
                            
                        # Zbierz wszystkie wartości wzrostu (dla parametrów info są zawsze aktywne)
                        for value_id, value_data in values.items():
                            if isinstance(value_data, dict):
                                try:
                                    height_value = int(value_data.get('name', '0'))
                                    if self.is_valid_height(height_value):
                                        selected_heights.append(height_value)
                                except (ValueError, TypeError):
                                    continue
                                    
            if selected_heights:
                selected_heights.sort()
                height_range = HeightRange(min(selected_heights), max(selected_heights))
                
                # Debug output
                print(f"🔍 Znaleziono istniejący zakres wzrostu: {height_range.min_height}-{height_range.max_height} cm ({len(selected_heights)} wartości)")
                
                # Ustaw zakres w managerze
                self.height_range = height_range
                return height_range
                
        except Exception as e:
            print(f"Warning: Could not extract height from API data: {e}")
            
        return None
        
    def get_suggested_ranges(self) -> List[Tuple[int, int, str]]:
        """
        Pobierz sugerowane zakresy wzrostu
        
        Returns:
            Lista tupli (min, max, nazwa)
        """
        return [
            (82, 95, "Bardzo małe dzieci (82-95 cm)"),
            (95, 110, "Małe dzieci (95-110 cm)"),
            (110, 130, "Dzieci (110-130 cm)"),
            (130, 150, "Młodzież (130-150 cm)"),
            (150, 170, "Dorośli niskiego wzrostu (150-170 cm)"),
            (170, 185, "Dorośli średniego wzrostu (170-185 cm)"),
            (185, 205, "Dorośli wysokiego wzrostu (185-205 cm)"),
            (82, 205, "Wszystkie dostępne wzrosty (82-205 cm)")
        ]