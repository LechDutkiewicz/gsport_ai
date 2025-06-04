# scripts/setup.py
"""
Skrypt instalacyjny i konfiguracyjny dla GSPORT AI Tool
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict

class GSportToolSetup:
    """Konfigurator aplikacji GSPORT AI Tool"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_sample = self.project_root / "config_sample.py"
        self.config_file = self.project_root / "config.py"
        
    def check_python_version(self) -> bool:
        """Sprawdź wersję Pythona"""
        version = sys.version_info
        required = (3, 8)
        
        if version >= required:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} - wymagany Python {required[0]}.{required[1]}+")
            return False
            
    def install_dependencies(self) -> bool:
        """Zainstaluj zależności"""
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ Brak pliku requirements.txt")
            return False
            
        print("📦 Instalowanie zależności...")
        
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Zależności zainstalowane pomyślnie")
                return True
            else:
                print(f"❌ Błąd instalacji: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Błąd instalacji: {e}")
            return False
            
    def create_config_file(self) -> bool:
        """Utwórz plik konfiguracyjny"""
        if self.config_file.exists():
            response = input("⚠️  config.py już istnieje. Nadpisać? (tak/nie): ")
            if response.lower() not in ['tak', 't', 'yes', 'y']:
                print("➡️  Pozostawiono istniejący config.py")
                return True
                
        if not self.config_sample.exists():
            print("❌ Brak pliku config_sample.py")
            return False
            
        try:
            shutil.copy2(self.config_sample, self.config_file)
            print("✅ Utworzono config.py z szablonu")
            
            print("\n⚠️  WAŻNE: Uzupełnij klucze API w config.py!")
            print("   - GSPORT_API_KEY")
            print("   - GPT_API_KEY") 
            
            return True
            
        except Exception as e:
            print(f"❌ Błąd tworzenia config.py: {e}")
            return False
            
    def create_output_directories(self) -> None:
        """Utwórz katalogi wyjściowe"""
        directories = [
            "output",
            "output/ok", 
            "output/errors",
            "prompts/backups",
            "prompts/trash"
        ]
        
        print("📁 Tworzenie katalogów...")
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  📂 {directory}")
            
    def check_tkinterweb(self) -> bool:
        """Sprawdź dostępność tkinterweb"""
        try:
            import tkinterweb
            print("✅ tkinterweb - dostępny")
            return True
        except ImportError:
            print("⚠️  tkinterweb - niedostępny (podgląd HTML będzie ograniczony)")
            return False
            
    def validate_config(self) -> bool:
        """Waliduj plik konfiguracyjny"""
        if not self.config_file.exists():
            print("❌ Brak pliku config.py")
            return False
            
        try:
            # Dodaj katalog do sys.path tymczasowo
            sys.path.insert(0, str(self.project_root))
            import config
            
            required_settings = [
                'GSPORT_API_KEY',
                'GPT_API_KEY', 
                'MODEL',
                'MAX_TOKENS'
            ]
            
            missing = []
            for setting in required_settings:
                if not hasattr(config, setting) or not getattr(config, setting):
                    missing.append(setting)
                    
            if missing:
                print(f"❌ Brak ustawień w config.py: {', '.join(missing)}")
                return False
            else:
                print("✅ Konfiguracja - prawidłowa")
                return True
                
        except ImportError as e:
            print(f"❌ Błąd importu config.py: {e}")
            return False
        except Exception as e:
            print(f"❌ Błąd walidacji config.py: {e}")
            return False
        finally:
            # Usuń z sys.path
            if str(self.project_root) in sys.path:
                sys.path.remove(str(self.project_root))
                
    def run_setup(self) -> bool:
        """Uruchom pełny setup"""
        print("🚀 Konfiguracja GSPORT AI Tool 2.0")
        print("=" * 50)
        
        steps = [
            ("Sprawdzanie wersji Python", self.check_python_version),
            ("Instalowanie zależności", self.install_dependencies),
            ("Tworzenie pliku konfiguracyjnego", self.create_config_file), 
            ("Tworzenie katalogów", lambda: (self.create_output_directories(), True)[1]),
            ("Sprawdzanie tkinterweb", self.check_tkinterweb),
            ("Walidacja konfiguracji", self.validate_config)
        ]
        
        all_passed = True
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                success = step_func()
                if not success:
                    all_passed = False
            except Exception as e:
                print(f"❌ Błąd w kroku '{step_name}': {e}")
                all_passed = False
                
        print("\n" + "=" * 50)
        
        if all_passed:
            print("✅ Setup zakończony pomyślnie!")
            print("\n🎯 Możesz teraz uruchomić aplikację:")
            print("   python main.py")
        else:
            print("❌ Setup zakończony z błędami")
            print("🔧 Sprawdź błędy powyżej i uruchom ponownie")
            
        return all_passed


def main():
    """Główna funkcja setup"""
    setup = GSportToolSetup()
    setup.run_setup()


if __name__ == "__main__":
    main()