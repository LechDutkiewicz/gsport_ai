# xml_builder.py
import datetime
from typing import List
from product_data_manager import ProductDataManager

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
        
        # Dodaj parametr koloru jeśli został wybrany
        if data_manager.parameters.color and data_manager.parameters.color_remote_id:
            xml_parts.extend([
                '        <options>',
                '            <options>',
                f'                <option name="Kolor dominujący" remote_id="{data_manager.parameters.color_remote_id}" required="1">{data_manager.parameters.color}</option>',
                '            </options>',
                '        </options>'
            ])
        
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
            
            # Dodaj parametr koloru jeśli został wybrany
            if data_manager.parameters.color and data_manager.parameters.color_remote_id:
                xml_parts.extend([
                    '        <options>',
                    '            <options>',
                    f'                <option name="Kolor dominujący" remote_id="{data_manager.parameters.color_remote_id}" required="1">{data_manager.parameters.color}</option>',
                    '            </options>',
                    '        </options>'
                ])
                
            xml_parts.append('    </item>')
        
        xml_parts.append('</products>')
        
        return '\n'.join(xml_parts)