# gsport_ai

---

## GSPORT REDAKTOR OPISÓW 2.0 - README

---

### OPIS APLIKACJI
Aplikacja służy do automatycznego generowania opisów produktów dla sklepu e-commerce GSport przy użyciu API OpenAI (ChatGPT). Umożliwia pobieranie danych produktów z systemu Sky-Shop, dodawanie specyfikacji technicznych i generowanie zoptymalizowanych opisów produktowych.

---

### WYMAGANIA SYSTEMOWE
- **Python** 3.8 lub nowszy  
- **System operacyjny**: Windows 10/11, macOS, Linux  
- Połączenie z internetem  
- Klucze API (GSport i OpenAI)  

---

### INSTALACJA BIBLIOTEK
1. Otwórz terminal/wiersz poleceń w folderze z aplikacją.  
2. *Opcjonalnie*: Utwórz wirtualne środowisko Python:  
   ```bash
   python -m venv venv
   ```
   - **Aktywacja (Windows)**:  
     ```bash
     venv\Scripts\activate
     ```
   - **Aktywacja (macOS/Linux)**:  
     ```bash
     source venv/bin/activate
     ```
3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```
   Jeśli nie masz pliku `requirements.txt`, zainstaluj ręcznie:
   ```bash
   pip install requests
   pip install beautifulsoup4
   pip install Pillow
   pip install tkinterweb
   ```
   > **Uwaga:** `tkinterweb` może wymagać dodatkowych zależności na niektórych systemach.  
   > W przypadku problemów:
   > ```bash
   > pip install --upgrade pip
   > pip install tkinterweb --no-cache-dir
   > ```

---

### KONFIGURACJA
1. Skopiuj plik `config_sample.py` i nazwij go `config.py`.  
2. Uzupełnij `config.py` swoimi danymi:
   ```python
   GSPORT_API_KEY = "twój_klucz_api_gsport"
   GPT_API_KEY    = "twój_klucz_api_openai"
   MODEL          = "gpt-4"          # lub "gpt-3.5-turbo" dla tańszej opcji
   MAX_TOKENS     = 2000             # możesz dostosować
   ```
3. Upewnij się, że masz wszystkie pliki promptów w folderze `prompts/`.

---

### STRUKTURA PLIKÓW
```
gsport-ai-tool/
├── main.py                # Główny plik aplikacji
├── product_manager.py     # Logika zarządzania produktami
├── api_client.py          # Klienci API
├── utils.py               # Funkcje pomocnicze
├── prompt_editor.py       # Edytor promptów
├── config.py              # Konfiguracja (musisz utworzyć)
├── prompts/               # Folder z promptami
│   ├── prompt_newdesc.txt
│   ├── prompt_newdesc_99spokes.txt
│   ├── prompt_shortdesc.txt
│   └── … (inne pliki promptów)
└── output/                # Folder na wygenerowane pliki XML
    ├── ok/                # Udane aktualizacje
    └── errors/            # Błędne aktualizacje
```

---

### URUCHOMIENIE APLIKACJI
1. Upewnij się, że jesteś w folderze z aplikacją.  
2. Jeśli używasz wirtualnego środowiska, aktywuj je.  
3. Uruchom aplikację:
   ```bash
   python main.py
   ```

---

### JAK UŻYWAĆ APLIKACJI

1. **ŁADOWANIE PRODUKTU**  
   - Wklej ID produktu lub link ze sklepu GSport.  
   - Naciśnij Enter lub kliknij poza polem.  
   - Dane produktu załadują się automatycznie.  

2. **DODAWANIE SPECYFIKACJI (opcjonalne)**  
   - **“Wgraj opis”** – zastępuje obecny opis produktu.  
   - **“JSON”** – wklej specyfikację JSON (np. z 99spokes).  
   - **“HTML”** – wklej specyfikację HTML.  

3. **GENEROWANIE OPISU**  
   - Zaznacz/odznacz “Rower” w zależności od typu produktu.  
   - Kliknij **“Generuj AI”**.  
   - Poczekaj na wygenerowanie opisów.  

4. **EDYCJA I PODGLĄD**  
   - Możesz edytować wygenerowane opisy bezpośrednio w aplikacji.  
   - Kliknij **“Podgląd HTML”**, aby zobaczyć, jak będzie wyglądał opis.  
   - Składnia HTML jest automatycznie kolorowana.  

5. **ZAPIS DO SKLEPU**  
   - Kliknij **“Zapisz w sklepie”**, aby wysłać opisy do systemu.  
   - Kopia XML zostanie zapisana w folderze `output/`.  

6. **EDYTOR PROMPTÓW**  
   - Kliknij **“Edytor promptów”**, aby modyfikować szablony.  
   - Możesz tworzyć, edytować i usuwać prompty.  

---

### ROZWIĄZYWANIE PROBLEMÓW
1. **“No module named 'tkinter'”**  
   - **Windows:** tkinter powinien być zainstalowany z Python.  
   - **Linux:**  
     ```bash
     sudo apt-get install python3-tk
     ```  
   - **macOS:** tkinter powinien być zainstalowany z Python.  

2. **“No module named 'PIL'”**  
   ```bash
   pip install Pillow
   ```

3. **Problemy z `tkinterweb`**  
   - Spróbuj:
     ```bash
     pip install --upgrade tkinterweb
     ```  
   - Alternatywnie:
     ```bash
     pip uninstall tkinterweb
     pip install tkinterweb
     ```

4. **Błędy API**  
   - Sprawdź, czy klucze API w `config.py` są poprawne.  
   - Sprawdź połączenie internetowe.  
   - Sprawdź limity API OpenAI.

5. **Brak obrazków produktów**  
   - Upewnij się, że masz połączenie z internetem.  
   - Niektóre produkty mogą nie mieć zdjęć.  

---

### KOSZTY UŻYWANIA
Aplikacja pokazuje koszt każdego zapytania do API OpenAI w centach USD.  
**Orientacyjne koszty:**
- **GPT-3.5-turbo**: ~0.1–0.3¢ za opis  
- **GPT-4**: ~1–3¢ za opis  

---

### KONTAKT I WSPARCIE
W przypadku problemów technicznych sprawdź:
- Logi w konsoli Python  
- Pliki XML w folderze `output/errors/`  
- Konfigurację w `config.py`  

---

### AKTUALIZACJE
Przed aktualizacją aplikacji:
1. Zrób kopię zapasową folderów `prompts/` i `output/`.  
2. Zachowaj swój plik `config.py`.  
3. Po aktualizacji może być konieczna reinstalacja bibliotek.

---

> **POWODZENIA!**
