# scripts/validate_structure.py
"""
Skrypt walidacji struktury projektu
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple

class StructureValidator:
    """Walidator struktury projektu"""
    
    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        
        # Oczekiwana struktura
        self.expected_structure = {
            "files": [
                "main.py",
                "config_sample.py", 
                "requirements.txt",
                "README.md"
            ],
            "directories": [
                "src",
                "src/core",
                "src/api", 
                "src/ui",
                "src/ui/components",
                "src/ui/styles",
                "src/prompts",
                "src/utils",
                "prompts",
                "output",
                "output/ok",
                "output/errors"
            ],
            "python_packages": [
                "src",
                "src/core",
                "src/api",
                "src/ui", 
                "src/ui/components",
                "src/ui/styles",
                "src/prompts",
                "src/utils"
            ]
        }
        
    def check_files(self) -> Tuple[List[str], List[str]]:
        """Sprawdź obecność wymaganych plików"""
        found = []
        missing = []
        
        for file_name in self.expected_structure["files"]:
            file_path = self.root / file_name
            if file_path.exists():
                found.append(file_name)
            else:
                missing.append(file_name)
                
        return found, missing
        
    def check_directories(self) -> Tuple[List[str], List[str]]:
        """Sprawdź obecność katalogów"""
        found = []
        missing = []
        
        for dir_name in self.expected_structure["directories"]:
            dir_path = self.root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                found.append(dir_name)
            else:
                missing.append(dir_name)
                
        return found, missing
        
    def check_python_packages(self) -> Tuple[List[str], List[str]]:
        """Sprawdź obecność plików __init__.py w pakietach"""
        found = []
        missing = []
        
        for package_name in self.expected_structure["python_packages"]:
            init_file = self.root / package_name / "__init__.py"
            if init_file.exists():
                found.append(package_name)
            else:
                missing.append(package_name)
                
        return found, missing
        
    def validate(self) -> bool:
        """Wykonaj pełną walidację"""
        print("🔍 Walidacja struktury projektu")
        print("=" * 40)
        
        all_valid = True
        
        # Sprawdź pliki
        found_files, missing_files = self.check_files()
        print(f"\n📄 Pliki ({len(found_files)}/{len(self.expected_structure['files'])})")
        
        for file_name in found_files:
            print(f"  ✅ {file_name}")
            
        for file_name in missing_files:
            print(f"  ❌ {file_name}")
            all_valid = False
            
        # Sprawdź katalogi
        found_dirs, missing_dirs = self.check_directories()
        print(f"\n📁 Katalogi ({len(found_dirs)}/{len(self.expected_structure['directories'])})")
        
        for dir_name in found_dirs:
            print(f"  ✅ {dir_name}")
            
        for dir_name in missing_dirs:
            print(f"  ❌ {dir_name}")
            all_valid = False
            
        # Sprawdź pakiety Python
        found_packages, missing_packages = self.check_python_packages()
        print(f"\n🐍 Pakiety Python ({len(found_packages)}/{len(self.expected_structure['python_packages'])})")
        
        for package_name in found_packages:
            print(f"  ✅ {package_name}/__init__.py")
            
        for package_name in missing_packages:
            print(f"  ❌ {package_name}/__init__.py")
            all_valid = False
            
        print("\n" + "=" * 40)
        
        if all_valid:
            print("✅ Struktura projektu jest prawidłowa!")
        else:
            print("❌ Znaleziono problemy ze strukturą")
            print("🔧 Uruchom scripts/migrate_to_new_structure.py")
            
        return all_valid


def main():
    """Główna funkcja walidacji"""
    validator = StructureValidator()
    validator.validate()


if __name__ == "__main__":
    main()