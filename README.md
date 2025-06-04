# GSPORT AI Tool 2.0

**Automatyczny generator opisów produktów dla sklepu e-commerce GSport**

---

## 📋 Spis treści

- [Opis aplikacji](#opis-aplikacji)
- [Wymagania systemowe](#wymagania-systemowe)
- [Instalacja](#instalacja)
- [Struktura projektu](#struktura-projektu)
- [Konfiguracja](#konfiguracja)
- [Użytkowanie](#użytkowanie)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [Dla deweloperów](#dla-deweloperów)

---

## 📖 Opis aplikacji

Aplikacja służy do automatycznego generowania opisów produktów dla sklepu e-commerce GSport przy użyciu API OpenAI (ChatGPT). Umożliwia:

- 🔍 Pobieranie danych produktów z systemu Sky-Shop
- 📝 Dodawanie specyfikacji technicznych (JSON/HTML)
- 🤖 Generowanie zoptymalizowanych opisów produktowych z AI
- 🎨 Edycję wygenerowanych opisów z podświetlaniem składni HTML
- 🔄 Aktualizację produktów w systemie GSport
- 🎯 Zarządzanie promptami AI przez dedykowany edytor

---

## 💻 Wymagania systemowe

- **Python** 3.8 lub nowszy
- **System operacyjny**: Windows 10/11, macOS, Linux
- **Połączenie z internetem**
- **Klucze API**: GSport i OpenAI

---

## 🚀 Instalacja

### Opcja 1: Automatyczna instalacja (zalecana)

```bash
# 1. Sklonuj/pobierz repozytorium
git clone <repository-url>
cd gsport-ai-tool

# 2. Uruchom skrypt instalacyjny
python scripts/setup.py
```

### Opcja 2: Manualna instalacja

```bash
# 1. Utwórz wirtualne środowisko (opcjonalnie)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Utwórz plik konfiguracyjny
cp config_sample.py config.py

# 4. Uzupełnij config.py swoimi kluczami API
```

---

## 📁 Struktura projektu

```
gsport-ai-tool/
├── main.py                     # 🚀 Punkt wejścia aplikacji
├── config.py                   # ⚙️  Konfiguracja (tworzy użytkownik)
├── requirements.txt            # 📦 Zależności
├── README.md                   # 📖 Dokumentacja
│
├── src/                        # 💻 Kod źródłowy
│   ├── core/                   # 🧠 Logika biznesowa
│   │   ├── product_data_manager.py
│   │   ├── ai_description_generator.py
│   │   ├── xml_builder.py
│   │   └── image_manager.py
│   │
│   ├── api/                    # 🌐 Klienty API
│   │   └── api_client.py
│   │
│   ├── ui/                     # 🎨 Interfejs użytkownika
│   │   ├── components/
│   │   └── styles/
│   │
│   ├── prompts/                # 📝 Zarządzanie promptami
│   └── utils/                  # 🛠️  Narzędzia pomocnicze
│
├── prompts/                    # 📄 Pliki promptów AI
├── output/                     # 📤 Pliki wyjściowe XML
├── scripts/                    # 🔧 Skrypty pomocnicze
└── tests/                      # 🧪 Testy (w przyszłości)
```

---

## ⚙️ Konfiguracja

### 1. Utwórz plik config.py

```bash
cp config_sample.py config.py
```

### 2. Uzupełnij dane API w config.py

```python
# GSport API Configuration
GSPORT_API_URL = "https://www.gsport.pl/api"
GSPORT_API_KEY = "twój_klucz_api_gsport"

# OpenAI API Configuration
GPT_API_KEY = "twój_klucz_api_openai"
MODEL = "gpt-4o-mini"
MAX_TOKENS = 4096

# Cost configuration (per token)
INPUT_COST = 0.15/1e6
OUTPUT_COST = 0.60/1e6
```

### 3. Sprawdź konfigurację

```bash
python scripts/validate_structure.py
```

---

## 🎯 Użytkowanie

### Uruchomienie aplikacji

```bash
python main.py
```

### Workflow pracy z aplikacją

1. **📥 Ładowanie produktu**
   - Wklej ID produktu lub link ze sklepu GSport
   - Naciśnij Enter lub kliknij poza polem
   - Dane produktu załadują się automatycznie

2. **📋 Dodawanie specyfikacji (opcjonalne)**
   - **"Wgraj opis"** – zastępuje obecny opis produktu
   - **"JSON"** – wklej specyfikację JSON (np. z 99spokes)
   - **"HTML"** – wklej specyfikację HTML

3. **🎨 Parametry produktu**
   - Ustaw kolor dominujący z listy
   - Wprowadź podobne produkty (opcjonalnie)

4. **🤖 Generowanie opisu**
   - Zaznacz/odznacz "Rower" w zależności od typu produktu
   - Kliknij **"Generuj AI"**
   - Poczekaj na wygenerowanie opisów

5. **✏️ Edycja i podgląd**
   - Edytuj wygenerowane opisy bezpośrednio w aplikacji
   - Kliknij **"Podgląd HTML"** aby zobaczyć efekt końcowy
   - Składnia HTML jest automatycznie kolorowana

6. **💾 Zapis do sklepu**
   - Kliknij **"Zapisz w sklepie"** aby wysłać opisy do systemu
   - Kopia XML zostanie zapisana w folderze `output/`

7. **📝 Edytor promptów**
   - Kliknij **"Edytor promptów"** aby modyfikować szablony
   - Twórz, edytuj i usuwaj prompty według potrzeb

---

## 💰 Koszty używania

Aplikacja pokazuje koszt każdego zapytania do API OpenAI w centach USD.

**Orientacyjne koszty:**
- **GPT-4o-mini**: ~0.1–0.3¢ za opis
- **GPT-4**: ~1–3¢ za opis

---

## 🔧 Rozwiązywanie problemów

### Problemy z importami po migracji

```bash
# Sprawdź strukturę projektu
python scripts/validate_structure.py

# Jeśli struktura nieprawidłowa, uruchom migrację
python scripts/migrate_to_new_structure.py
```

### Błędy zależności

```bash
# Problem z tkinter (Linux)
sudo apt-get install python3-tk

# Problem z PIL
pip install Pillow

# Problem z tkinterweb
pip install --upgrade tkinterweb
```

### Błędy API

1. Sprawdź klucze API w `config.py`
2. Sprawdź połączenie internetowe
3. Sprawdź limity API OpenAI
4. Sprawdź logi w konsoli

### Brak obrazków produktów

1. Sprawdź połączenie internetowe
2. Niektóre produkty mogą nie mieć zdjęć
3. Sprawdź czy URL GSport jest prawidłowy

---

## 👨‍💻 Dla deweloperów

### Uruchomienie testów

```bash
# Instalacja zależności deweloperskich
pip install pytest pytest-cov

# Uruchomienie testów
python -m pytest tests/

# Z pokryciem kodu
python -m pytest tests/ --cov=src
```

### Struktura kodu

- **`src/core/`** - Logika biznesowa bez zależności UI
- **`src/ui/`** - Komponenty interfejsu użytkownika
- **`src/api/`** - Komunikacja z zewnętrznymi API
- **`src/utils/`** - Narzędzia pomocnicze

### Zasady developmentu

1. **Single Responsibility Principle** - jedna klasa = jedna odpowiedzialność
2. **Separation of Concerns** - UI oddzielone od logiki biznesowej
3. **Type Hints** - używaj typów dla lepszej czytelności
4. **Docstrings** - dokumentuj funkcje i klasy
5. **Tests** - pisz testy dla nowych funkcji

### Dodawanie nowych funkcji

1. Dodaj logikę biznesową w `src/core/`
2. Dodaj komponenty UI w `src/ui/components/`
3. Dodaj testy w `tests/`
4. Zaktualizuj dokumentację

---

## 📞 Wsparcie

W przypadku problemów:

1. **Sprawdź logi** w konsoli Python
2. **Sprawdź pliki XML** w folderze `output/errors/`
3. **Zweryfikuj konfigurację** w `config.py`
4. **Uruchom walidację** `python scripts/validate_structure.py`

---

## 🔄 Aktualizacje

Przed aktualizacją aplikacji:

1. **Zrób kopię zapasową**:
   ```bash
   cp -r prompts/ prompts_backup/
   cp -r output/ output_backup/
   cp config.py config_backup.py
   ```

2. **Po aktualizacji**:
   ```bash
   pip install -r requirements.txt
   python scripts/validate_structure.py
   ```

---

## 📄 Licencja

© 2024 GSPORT Team. Wszystkie prawa zastrzeżone.

---

> **🎉 Powodzenia w generowaniu opisów!**