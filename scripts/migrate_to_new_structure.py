#!/usr/bin/env python3
# scripts/migrate_to_new_structure.py
"""
Skrypt migracji do nowej struktury folderów
Przenieś pliki z obecnej struktury do nowej architektury
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class StructureMigrator:
    """Migrator struktury plików"""
    
    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        self.backup_dir = self.root / "backup_old_structure"
        
        # Mapowanie starych plików do nowych lokalizacji
        self.file_mappings = {
            # Główne pliki (zostają w root)
            "main.py": "main.py",
            "config.py": "config.py", 
            "config_sample.py": "config_sample.py",
            "requirements.txt": "requirements.txt",
            "README.md": "README.md",
            
            # Pliki do src/core/
            "product_data_manager.py": "src/core/product_data_manager.py",
            "ai_description_generator.py": "src/core/ai_description_generator.py", 
            "xml_builder.py": "src/core/xml_builder.py",
            "image_manager.py": "src/core/image_manager.py",
            
            # Pliki do src/api/
            "api_client.py": "src/api/api_client.py",
            
            # Pliki do src/ui/
            "ui_components.py": "src/ui/components/ui_components.py",
            "content_area.py": "src/ui/components/content_area.py",
            "styles.py": "src/ui/styles/style_manager.py",
            "html_text_widget.py": "src/ui/components/syntax_highlighter.py",
            
            # Pliki do src/prompts/
            "prompt_editor.py": "src/prompts/prompt_editor.py",
            
            # Pliki do src/utils/
            "utils.py": "src/utils/file_utils.py"  # Zostanie podzielony
        }
        
        # Foldery do utworzenia
        self.directories_to_create = [
            "src",
            "src/core", 
            "src/api",
            "src/ui",
            "src/ui/components",
            "src/ui/styles", 
            "src/prompts",
            "src/utils",
            "tests",
            "tests/test_core",
            "tests/test_api", 
            "tests/test_ui",
            "tests/fixtures",
            "docs",
            "scripts"
        ]
        
    def create_backup(self) -> None:
        """Utwórz kopię zapasową obecnej struktury"""
        print("📦 Tworzenie kopii zapasowej...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
            
        self.backup_dir.mkdir()
        
        # Kopiuj wszystkie pliki .py
        for file_path in self.root.glob("*.py"):
            if file_path.name != "migrate_to_new_structure.py":
                shutil.copy2(file_path, self.backup_dir / file_path.name)
                print(f"  📄 Skopiowano: {file_path.name}")
                
        print(f"✅ Kopia zapasowa utworzona w: {self.backup_dir}")
        
    def create_directory_structure(self) -> None:
        """Utwórz nową strukturę katalogów"""
        print("📁 Tworzenie struktury katalogów...")
        
        for directory in self.directories_to_create:
            dir_path = self.root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  📂 Utworzono: {directory}")
            
            # Utwórz __init__.py w pakietach Python
            if directory.startswith("src"):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
                    print(f"  📄 Utworzono: {directory}/__init__.py")
                    
    def migrate_files(self) -> None:
        """Przenieś pliki do nowych lokalizacji"""
        print("🚚 Migracja plików...")
        
        for old_path, new_path in self.file_mappings.items():
            old_file = self.root / old_path
            new_file = self.root / new_path
            
            if old_file.exists():
                # Upewnij się, że katalog docelowy istnieje
                new_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Przenieś plik
                shutil.move(str(old_file), str(new_file))
                print(f"  ➡️  {old_path} -> {new_path}")
            else:
                print(f"  ⚠️  Nie znaleziono: {old_path}")
                
    def create_init_files(self) -> None:
        """Utwórz pliki __init__.py z odpowiednimi importami"""
        print("📝 Tworzenie plików __init__.py...")
        
        init_contents = {
            "src/__init__.py": '''"""
GSPORT AI Tool - Główny pakiet aplikacji
"""

__version__ = "2.0.0"
__author__ = "GSPORT Team"
__description__ = "Automatyczny generator opisów produktów dla sklepu e-commerce"
''',
            
            "src/core/__init__.py": '''"""
Moduł logiki biznesowej aplikacji
"""

from .product_data_manager import ProductDataManager
from .ai_description_generator import AIDescriptionGenerator
from .xml_builder import XMLBuilder
from .image_manager import ImageManager

__all__ = [
    'ProductDataManager',
    'AIDescriptionGenerator', 
    'XMLBuilder',
    'ImageManager'
]
''',
            
            "src/api/__init__.py": '''"""
Moduł klientów API
"""

from .api_client import GSportAPIClient, OpenAIClient

__all__ = ['GSportAPIClient', 'OpenAIClient']
''',
            
            "src/ui/__init__.py": '''"""
Moduł interfejsu użytkownika
"""

# Import będzie dodany po refaktoryzacji main.py
''',
            
            "src/utils/__init__.py": '''"""
Narzędzia pomocnicze
"""

from .file_utils import save_xml_copy, ensure_directory_exists
from .text_utils import extract_product_id, clean_html_for_display

__all__ = [
    'save_xml_copy',
    'ensure_directory_exists',
    'extract_product_id', 
    'clean_html_for_display'
]
'''
        }
        
        for file_path, content in init_contents.items():
            full_path = self.root / file_path
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📄 Utworzono: {file_path}")
            
    def update_imports(self) -> None:
        """Aktualizuj importy w przenosionych plikach"""
        print("🔄 Aktualizacja importów...")
        
        # To będzie wymagało ręcznej edycji każdego pliku
        # Można to zautomatyzować, ale bezpieczniej zrobić ręcznie
        print("  ⚠️  Importy wymagają ręcznej aktualizacji w każdym pliku")
        
    def create_migration_report(self) -> None:
        """Utwórz raport migracji"""
        report_path = self.root / "MIGRATION_REPORT.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("""# Raport Migracji do Nowej Struktury

## ✅ Wykonane kroki:

1. Utworzono kopię zapasową w `backup_old_structure/`
2. Utworzono nową strukturę katalogów
3. Przeniesiono pliki do nowych lokalizacji
4. Utworzono pliki `__init__.py`

## ⚠️ Wymagane ręczne kroki:

1. **Aktualizacja importów** - wszystkie pliki wymagają aktualizacji importów:
   - Zmień `from utils import` na `from src.utils import`
   - Zmień `from api_client import` na `from src.api.api_client import`
   - Itd.

2. **Refaktoryzacja main.py** - zastąp obecny main.py nową wersją

3. **Podział utils.py** - podziel na:
   - `src/utils/file_utils.py`
   - `src/utils/text_utils.py` 
   - `src/utils/validation.py`

4. **Testowanie** - przetestuj aplikację po zmianach

## 📁 Nowa struktura:

```
src/
├── core/          # Logika biznesowa
├── api/           # Klienty API
├── ui/            # Interfejs użytkownika
├── prompts/       # Zarządzanie promptami
└── utils/         # Narzędzia pomocnicze
```

## 🔧 Następne kroki:

1. Uruchom `python main.py` i sprawdź błędy importów
2. Popraw importy zgodnie z nową strukturą
3. Przetestuj wszystkie funkcje aplikacji
4. Usuń folder `backup_old_structure/` po potwierdzeniu, że wszystko działa
""")
        
        print(f"📋 Raport migracji zapisany: {report_path}")
        
    def run_migration(self) -> None:
        """Uruchom pełną migrację"""
        print("🚀 Rozpoczynam migrację do nowej struktury...\n")
        
        try:
            self.create_backup()
            print()
            
            self.create_directory_structure()
            print()
            
            self.migrate_files()
            print()
            
            self.create_init_files()
            print()
            
            self.update_imports()
            print()
            
            self.create_migration_report()
            print()
            
            print("✅ Migracja zakończona pomyślnie!")
            print("\n📋 Następne kroki:")
            print("1. Sprawdź MIGRATION_REPORT.md")
            print("2. Zaktualizuj importy w plikach")
            print("3. Przetestuj aplikację")
            
        except Exception as e:
            print(f"❌ Błąd podczas migracji: {e}")
            print("🔄 Możesz przywrócić pliki z backup_old_structure/")


def main():
    """Główna funkcja skryptu migracji"""
    print("=" * 60)
    print("🏗️  GSPORT AI Tool - Migracja do Nowej Struktury")
    print("=" * 60)
    
    migrator = StructureMigrator()
    
    # Potwierdź migrację
    response = input("\n❓ Czy chcesz rozpocząć migrację? (tak/nie): ").lower()
    if response not in ['tak', 't', 'yes', 'y']:
        print("❌ Migracja anulowana")
        return
        
    migrator.run_migration()


if __name__ == "__main__":
    main()