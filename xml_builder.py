# xml_builder.py
import datetime
from typing import List
from product_data_manager import ProductDataManager

def escape_xml(text: str) -> str:
    """
    Escape znaków specjalnych dla XML
    
    Args:
        text: Tekst do escapowania
        
    Returns:
        Tekst z escapowanymi znakami XML
    """
    if not text:
        return text
        
    # Mapowanie znaków specjalnych XML
    xml_escape_table = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }
    
    for char, escape_seq in xml_escape_table.items():
        text = text.replace(char, escape_seq)
        
    return text

class XMLBuilder:
    """Builder do tworzenia XML dla aktualizacji produktów"""
    
    @staticmethod
    def build_product_xml(product_id: str, data_manager: ProductDataManager) -> str:
        """
        Zbuduj XML dla aktualizacji pojedynczego produktu
        
        Args:
            product_id: ID produktu
            data_manager: Manager danych produktu
            
        Returns:
            XML jako string
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<products xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1" date="{now}">',
            '    <item>',
            f'        <prod_id>{product_id}</prod_id>',
            f'        <prod_shortdesc_pl><![CDATA[{data_manager.generated_descriptions.short}]]></prod_shortdesc_pl>',
            f'        <prod_desc_pl><![CDATA[{data_manager.generated_descriptions.long}]]></prod_desc_pl>'
        ]
        
        # Przygotuj parametry informacyjne (info_options)
        has_info_options = False
        info_options_xml = []
        
        # Dodaj oryginalne info_options (wykluczając wzrost)
        for original_option in data_manager.get_filtered_info_options():
            escaped_name = escape_xml(original_option.name)
            escaped_value = escape_xml(original_option.value)
            
            if original_option.type:
                info_options_xml.append(
                    f'            <option name="{escaped_name}" remote_id="{original_option.remote_id}" type="{original_option.type}">{escaped_value}</option>'
                )
            else:
                info_options_xml.append(
                    f'            <option name="{escaped_name}" remote_id="{original_option.remote_id}">{escaped_value}</option>'
                )
            has_info_options = True
        
        # Dodaj parametry wzrostu jeśli zostały wybrane (do info_options)
        height_options = data_manager.height_manager.get_height_values_for_xml()
        if height_options:
            for height_option in height_options:
                info_options_xml.append(
                    f'   <option name="{height_option["name"]}" remote_id="{height_option["remote_id"]}">{height_option["value"]}</option>'
                )
            has_info_options = True
            
        # Dodaj sekcję info_options jeśli są parametry wzrostu
        if has_info_options:
            xml_parts.append('        <info_options>')
            xml_parts.extend(info_options_xml)
            xml_parts.append('        </info_options>')
        
        # Przygotuj opcje klienta (options)
        has_options = False
        options_xml = []
        
        # Dodaj oryginalne options (wykluczając kolor dominujący)
        for original_option in data_manager.get_filtered_options():
            escaped_name = escape_xml(original_option.name)
            escaped_value = escape_xml(original_option.value)
            
            if original_option.type:
                options_xml.append(f'            <options>')
                options_xml.append(f'                <option name="{escaped_name}" remote_id="{original_option.remote_id}" type="{original_option.type}" required="1">{escaped_value}</option>')
                options_xml.append(f'            </options>')
            else:
                options_xml.append(f'            <options>')
                options_xml.append(f'                <option name="{escaped_name}" remote_id="{original_option.remote_id}" required="1">{escaped_value}</option>')
                options_xml.append(f'            </options>')
            has_options = True
        
        # Dodaj parametr koloru jeśli został wybrany (do options)
        if data_manager.parameters.color and data_manager.parameters.color_remote_id:
            options_xml.extend([
                '            <options>',
                f'                <option name="Kolor dominujący" remote_id="{data_manager.parameters.color_remote_id}" required="1">{data_manager.parameters.color}</option>',
                '            </options>'
            ])
            has_options = True
            
        # Dodaj sekcję options jeśli są opcje
        if has_options:
            xml_parts.append('        <options>')
            xml_parts.extend(options_xml)
            xml_parts.append('        </options>')
        
        xml_parts.extend([
            '    </item>',
            '</products>'
        ])
        
        return '\n'.join(xml_parts)
        
    @staticmethod
    def build_multiple_products_xml(product_ids: List[str], data_manager: ProductDataManager) -> str:
        """
        Zbuduj XML dla aktualizacji wielu produktów
        
        Args:
            product_ids: Lista ID produktów
            data_manager: Manager danych produktu
            
        Returns:
            XML jako string
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<products xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1" date="{now}">'
        ]
        
        # Dodaj każdy produkt
        for product_id in product_ids:
            xml_parts.extend([
                '    <item>',
                f'        <prod_id>{product_id}</prod_id>',
                f'        <prod_shortdesc_pl><![CDATA[{data_manager.generated_descriptions.short}]]></prod_shortdesc_pl>',
                f'        <prod_desc_pl><![CDATA[{data_manager.generated_descriptions.long}]]></prod_desc_pl>'
            ])
            
            # Przygotuj parametry informacyjne (info_options)
            has_info_options = False
            info_options_xml = []
            
            # Dodaj oryginalne info_options (wykluczając wzrost)
            for original_option in data_manager.get_filtered_info_options():
                if original_option.type:
                    info_options_xml.append(
                        f'       <option name="{original_option.name}" remote_id="{original_option.remote_id}" type="{original_option.type}">{original_option.value}</option>'
                    )
                else:
                    info_options_xml.append(
                        f'       <option name="{original_option.name}" remote_id="{original_option.remote_id}">{original_option.value}</option>'
                    )
                has_info_options = True
            
            # Dodaj parametry wzrostu jeśli zostały wybrane (do info_options)
            height_options = data_manager.height_manager.get_height_values_for_xml()
            if height_options:
                for height_option in height_options:
                    info_options_xml.append(
                        f'               <option name="{height_option["name"]}" remote_id="{height_option["remote_id"]}">{height_option["value"]}</option>'
                    )
                has_info_options = True
                
            # Dodaj sekcję info_options jeśli są parametry wzrostu
            if has_info_options:
                xml_parts.append('        <info_options>')
                xml_parts.extend(info_options_xml)
                xml_parts.append('        </info_options>')
            
            # Przygotuj opcje klienta (options)
            has_options = False
            options_xml = []
            
            # Dodaj oryginalne options (wykluczając kolor dominujący)
            for original_option in data_manager.get_filtered_options():
                if original_option.type:
                    options_xml.append(f'            <options>')
                    options_xml.append(f'                <option name="{original_option.name}" remote_id="{original_option.remote_id}" type="{original_option.type}" required="1">{original_option.value}</option>')
                    options_xml.append(f'            </options>')
                else:
                    options_xml.append(f'            <options>')
                    options_xml.append(f'                <option name="{original_option.name}" remote_id="{original_option.remote_id}" required="1">{original_option.value}</option>')
                    options_xml.append(f'            </options>')
                has_options = True
            
            # Dodaj parametr koloru jeśli został wybrany (do options)
            if data_manager.parameters.color and data_manager.parameters.color_remote_id:
                options_xml.extend([
                    '            <options>',
                    f'                <option name="Kolor dominujący" remote_id="{data_manager.parameters.color_remote_id}" required="1">{data_manager.parameters.color}</option>',
                    '            </options>'
                ])
                has_options = True
                
            # Dodaj sekcję options jeśli są opcje
            if has_options:
                xml_parts.append('        <options>')
                xml_parts.extend(options_xml)
                xml_parts.append('        </options>')
                
            xml_parts.append('    </item>')
        
        xml_parts.append('</products>')
        
        return '\n'.join(xml_parts)