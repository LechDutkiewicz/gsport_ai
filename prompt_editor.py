# prompt_editor.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from datetime import datetime

class PromptEditor:
    """A window for editing prompt templates"""
    
    def __init__(self, parent, prompt_manager):
        self.parent = parent
        self.prompt_manager = prompt_manager
        self.current_file = None
        self.modified = False
        
        # Create the editor window
        self.window = tk.Toplevel(parent)
        self.window.title("Edytor Promptów")
        self.window.geometry("1200x800")
        
        # Configure window
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Create UI
        self.create_ui()
        
        # Load first prompt file
        self.load_prompt_list()
        
    def create_ui(self):
        """Create the editor UI"""
        # Main container
        main_frame = tk.Frame(self.window, bg="#F9F9F9")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - prompt list
        left_panel = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        # Prompt list header
        list_header = tk.Label(
            left_panel,
            text="Pliki Promptów",
            font=("Helvetica", 12, "bold"),
            bg="#222645",
            fg="white",
            pady=10
        )
        list_header.pack(fill="x")
        
        # Prompt list
        list_frame = tk.Frame(left_panel, bg="#FFFFFF")
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.prompt_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 10),
            bg="#FFFFFF",
            selectmode="single",
            width=30
        )
        self.prompt_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.prompt_listbox.yview)
        
        # Bind selection event
        self.prompt_listbox.bind('<<ListboxSelect>>', self.on_prompt_select)
        
        # List actions
        list_actions = tk.Frame(left_panel, bg="#FFFFFF", pady=10)
        list_actions.pack(fill="x")
        
        ttk.Button(
            list_actions,
            text="Nowy Prompt",
            command=self.new_prompt
        ).pack(pady=2, padx=10, fill="x")
        
        ttk.Button(
            list_actions,
            text="Duplikuj",
            command=self.duplicate_prompt
        ).pack(pady=2, padx=10, fill="x")
        
        tk.Button(
            list_actions,
            text="Usuń",
            command=self.delete_prompt,
            bg="#E24B38",
            fg="white",
            font=("Helvetica", 10)
        ).pack(pady=2, padx=10, fill="x")
        
        # Right panel - editor
        right_panel = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Editor header
        editor_header = tk.Frame(right_panel, bg="#222645", pady=10)
        editor_header.pack(fill="x")
        
        self.file_label = tk.Label(
            editor_header,
            text="Wybierz plik promptu",
            font=("Helvetica", 12, "bold"),
            bg="#222645",
            fg="white"
        )
        self.file_label.pack(side="left", padx=20)
        
        # Save indicator
        self.save_indicator = tk.Label(
            editor_header,
            text="",
            font=("Helvetica", 10),
            bg="#222645",
            fg="#BFE02B"
        )
        self.save_indicator.pack(side="right", padx=20)
        
        # Toolbar
        toolbar = tk.Frame(right_panel, bg="#F0F0F0", pady=5)
        toolbar.pack(fill="x")
        
        tk.Button(
            toolbar,
            text="💾 Zapisz",
            command=self.save_prompt,
            bg="#BFE02B",
            font=("Helvetica", 10),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            toolbar,
            text="↩️ Cofnij zmiany",
            command=self.reload_current,
            bg="#F7F7F7",
            font=("Helvetica", 10),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            toolbar,
            text="📋 Kopiuj",
            command=self.copy_content,
            bg="#F7F7F7",
            font=("Helvetica", 10),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            toolbar,
            text="🔍 Podgląd",
            command=self.preview_prompt,
            bg="#F7F7F7",
            font=("Helvetica", 10),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        # Editor tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Raw editor tab
        raw_frame = tk.Frame(self.notebook)
        self.notebook.add(raw_frame, text="Edytor")
        
        # Text editor with syntax highlighting
        text_frame = tk.Frame(raw_frame)
        text_frame.pack(fill="both", expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(
            text_frame,
            width=4,
            padx=3,
            takefocus=0,
            border=0,
            state='disabled',
            wrap='none',
            bg="#F0F0F0",
            fg="#666666"
        )
        self.line_numbers.pack(side="left", fill="y")
        
        # Main text editor
        editor_scroll = tk.Scrollbar(text_frame)
        editor_scroll.pack(side="right", fill="y")
        
        self.text_editor = tk.Text(
            text_frame,
            wrap="none",
            undo=True,
            yscrollcommand=editor_scroll.set,
            font=("Consolas", 11),
            padx=10,
            pady=10
        )
        self.text_editor.pack(side="left", fill="both", expand=True)
        editor_scroll.config(command=self.sync_scroll)
        
        # Bind events
        self.text_editor.bind('<<Modified>>', self.on_text_modified)
        self.text_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.text_editor.bind('<MouseWheel>', self.sync_scroll)
        
        # Configure syntax highlighting tags
        self.setup_syntax_highlighting()
        
        # Structured editor tab
        structured_frame = tk.Frame(self.notebook)
        self.notebook.add(structured_frame, text="Edytor strukturalny")
        
        # Create structured editor
        self.create_structured_editor(structured_frame)
        
        # Variables tab
        vars_frame = tk.Frame(self.notebook)
        self.notebook.add(vars_frame, text="Zmienne")
        
        # Create variables viewer
        self.create_variables_viewer(vars_frame)
        
    def setup_syntax_highlighting(self):
        """Configure syntax highlighting for the editor"""
        # Headers
        self.text_editor.tag_configure("header", foreground="#0066CC", font=("Consolas", 11, "bold"))
        # Variables
        self.text_editor.tag_configure("variable", foreground="#009900", font=("Consolas", 11, "bold"))
        # Strings
        self.text_editor.tag_configure("string", foreground="#CC0000")
        # Comments
        self.text_editor.tag_configure("comment", foreground="#666666", font=("Consolas", 11, "italic"))
        
    def create_structured_editor(self, parent):
        """Create structured editor for prompt sections"""
        # Scrollable frame
        canvas = tk.Canvas(parent, bg="#FFFFFF")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Section editors
        self.section_editors = {}
        
        # CEL section
        self.create_section_editor(scrollable_frame, "CEL", "Cel promptu", height=5)
        
        # INSTRUKCJE DODATKOWE section
        self.create_section_editor(scrollable_frame, "INSTRUKCJE DODATKOWE", "Instrukcje dodatkowe", height=8)
        
        # ZMIENNE section
        self.create_section_editor(scrollable_frame, "ZMIENNE", "Zmienne", height=15)
        
        # STRUKTURA section
        self.create_section_editor(scrollable_frame, "STRUKTURA", "Struktura", height=15)
        
    def create_section_editor(self, parent, section_key, title, height=10):
        """Create an editor for a specific section"""
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", padx=10, pady=5)
        
        text_widget = tk.Text(
            frame,
            height=height,
            font=("Consolas", 10),
            wrap="word"
        )
        text_widget.pack(fill="x")
        
        # Bind modification event
        text_widget.bind('<<Modified>>', lambda e: self.on_structured_modified())
        
        self.section_editors[section_key] = text_widget
        
    def create_variables_viewer(self, parent):
        """Create variables viewer/editor"""
        # Instructions
        instructions = tk.Label(
            parent,
            text="Zmienne używane w promptach (kliknij aby skopiować):",
            font=("Helvetica", 10),
            bg="#F9F9F9",
            pady=10
        )
        instructions.pack(fill="x")
        
        # Variables frame
        vars_frame = tk.Frame(parent, bg="#FFFFFF")
        vars_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Common variables
        variables = [
            ("{{nazwa}}", "{prod_name}", "Nazwa produktu"),
            ("{{opis}}", "{prod_desclongription}", "Opis produktu"),
            ("{{specs}}", "{product_specification}", "Specyfikacja produktu"),
            ("{{struktura}}", "[definicja struktury]", "Struktura opisu"),
            ("{{tlum}}", "[tabela tłumaczeń]", "Tłumaczenia terminów"),
            ("{{tlum_naglowki}}", "[tabela nagłówków]", "Tłumaczenia nagłówków"),
            ("{{tlum_extras}}", "[tabela dodatków]", "Tłumaczenia dodatków"),
            ("{{specs_instrukcja}}", "[instrukcje specyfikacji]", "Instrukcje dla specyfikacji"),
            ("{{parametry}}", "[tabela parametrów]", "Parametry produktu"),
            ("{{spec_naglowki}}", "[nagłówki specyfikacji]", "Nagłówki specyfikacji")
        ]
        
        for i, (var_name, var_value, description) in enumerate(variables):
            var_frame = tk.Frame(vars_frame, bg="#F0F0F0", relief="raised", bd=1)
            var_frame.pack(fill="x", pady=2)
            
            # Variable name (clickable)
            var_label = tk.Label(
                var_frame,
                text=var_name,
                font=("Consolas", 11, "bold"),
                fg="#009900",
                bg="#F0F0F0",
                cursor="hand2",
                padx=10,
                width=20,
                anchor="w"
            )
            var_label.pack(side="left")
            var_label.bind("<Button-1>", lambda e, v=var_name: self.copy_variable(v))
            
            # Arrow
            tk.Label(
                var_frame,
                text="→",
                font=("Arial", 10),
                bg="#F0F0F0",
                padx=5
            ).pack(side="left")
            
            # Variable value
            tk.Label(
                var_frame,
                text=var_value,
                font=("Consolas", 10),
                fg="#666666",
                bg="#F0F0F0",
                width=30,
                anchor="w"
            ).pack(side="left")
            
            # Description
            tk.Label(
                var_frame,
                text=f"// {description}",
                font=("Arial", 9, "italic"),
                fg="#999999",
                bg="#F0F0F0",
                padx=10
            ).pack(side="left")
            
    def copy_variable(self, variable):
        """Copy variable to clipboard"""
        self.window.clipboard_clear()
        self.window.clipboard_append(variable)
        messagebox.showinfo("Skopiowano", f"Zmienna {variable} została skopiowana do schowka")
        
    def load_prompt_list(self):
        """Load list of prompt files"""
        self.prompt_listbox.delete(0, tk.END)
        
        # Create prompts folder if it doesn't exist
        if not os.path.exists('prompts'):
            os.makedirs('prompts')
            # Move existing prompt files to the new folder
            for f in os.listdir('.'):
                if f.startswith('prompt_') and f.endswith('.txt'):
                    os.rename(f, os.path.join('prompts', f))
        
        # Get all .txt files starting with "prompt_" from prompts folder
        prompt_files = []
        prompts_dir = 'prompts'
        if os.path.exists(prompts_dir):
            prompt_files = [f for f in os.listdir(prompts_dir) 
                          if f.startswith('prompt_') and f.endswith('.txt')]
        prompt_files.sort()
        
        for file in prompt_files:
            # Extract readable name
            name = file.replace('prompt_', '').replace('.txt', '').replace('_', ' ').title()
            self.prompt_listbox.insert(tk.END, name)
            
        # Store file mapping with full path
        self.file_mapping = {i: os.path.join('prompts', prompt_files[i]) 
                           for i in range(len(prompt_files))}
        
        # Select first item if available
        if prompt_files:
            self.prompt_listbox.selection_set(0)
            self.load_prompt_file(self.file_mapping[0])
            
    def on_prompt_select(self, event):
        """Handle prompt selection"""
        selection = self.prompt_listbox.curselection()
        if selection:
            if self.modified:
                response = messagebox.askyesnocancel(
                    "Niezapisane zmiany",
                    "Masz niezapisane zmiany. Czy chcesz je zapisać?"
                )
                if response is None:  # Cancel
                    return
                elif response:  # Yes
                    self.save_prompt()
                    
            index = selection[0]
            filename = self.file_mapping[index]
            self.load_prompt_file(filename)
            
    def load_prompt_file(self, filename):
        """Load a prompt file into the editor"""
        self.current_file = filename
        self.file_label.config(text=f"Edycja: {filename}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Load into raw editor
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, content)
            self.text_editor.edit_modified(False)
            
            # Parse and load into structured editor
            self.parse_prompt_content(content)
            
            # Apply syntax highlighting
            self.apply_syntax_highlighting()
            
            # Update line numbers
            self.update_line_numbers()
            
            self.modified = False
            self.update_save_indicator()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można wczytać pliku: {str(e)}")
            
    def parse_prompt_content(self, content):
        """Parse prompt content into sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('### ') and line.endswith(' ###'):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                # Start new section
                current_section = line.strip('# ').strip()
                current_content = []
            else:
                current_content.append(line)
                
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
            
        # Load into structured editor
        for section_key, editor in self.section_editors.items():
            editor.delete(1.0, tk.END)
            if section_key in sections:
                # Clean up the content
                content = sections[section_key].strip()
                editor.insert(1.0, content)
            editor.edit_modified(False)
            
    def apply_syntax_highlighting(self):
        """Apply syntax highlighting to the text"""
        # Remove all tags
        for tag in ["header", "variable", "string", "comment"]:
            self.text_editor.tag_remove(tag, 1.0, tk.END)
            
        content = self.text_editor.get(1.0, tk.END)
        
        # Highlight headers (### TEXT ###)
        for i, line in enumerate(content.split('\n'), 1):
            if line.startswith('### ') and line.endswith(' ###'):
                self.text_editor.tag_add("header", f"{i}.0", f"{i}.end")
                
        # Highlight variables ({{variable}} and {variable})
        import re
        for match in re.finditer(r'\{\{?\w+\}?\}', content):
            start = self.text_editor.index(f"1.0+{match.start()}c")
            end = self.text_editor.index(f"1.0+{match.end()}c")
            self.text_editor.tag_add("variable", start, end)
            
        # Highlight strings in quotes
        for match in re.finditer(r'"[^"]*"', content):
            start = self.text_editor.index(f"1.0+{match.start()}c")
            end = self.text_editor.index(f"1.0+{match.end()}c")
            self.text_editor.tag_add("string", start, end)
            
    def update_line_numbers(self, event=None):
        """Update line numbers"""
        lines = self.text_editor.get(1.0, tk.END).count('\n')
        line_numbers_text = '\n'.join(str(i) for i in range(1, lines + 1))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(1.0, line_numbers_text)
        self.line_numbers.config(state='disabled')
        
    def sync_scroll(self, *args):
        """Synchronize scrolling between text editor and line numbers"""
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)
        
    def on_text_modified(self, event=None):
        """Handle text modification"""
        if self.text_editor.edit_modified():
            self.modified = True
            self.update_save_indicator()
            self.apply_syntax_highlighting()
            self.text_editor.edit_modified(False)
            
    def on_structured_modified(self):
        """Handle structured editor modification"""
        self.modified = True
        self.update_save_indicator()
        
    def update_save_indicator(self):
        """Update save indicator"""
        if self.modified:
            self.save_indicator.config(text="● Niezapisane zmiany", fg="#E24B38")
        else:
            self.save_indicator.config(text="✓ Zapisano", fg="#BFE02B")
            
    def save_prompt(self):
        """Save the current prompt"""
        if not self.current_file:
            return
            
        try:
            # Get content based on active tab
            if self.notebook.index(self.notebook.select()) == 0:
                # Raw editor
                content = self.text_editor.get(1.0, tk.END).strip()
            else:
                # Structured editor - rebuild content
                content = self.build_structured_content()
                
            # Create backup
            backup_dir = os.path.join("prompts", "backups")
            os.makedirs(backup_dir, exist_ok=True)
            backup_file = os.path.join(
                backup_dir,
                f"{os.path.basename(self.current_file)}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            )
            
            # Copy current file to backup
            if os.path.exists(self.current_file):
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                    
            # Save new content
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(content)
                
            self.modified = False
            self.update_save_indicator()
            messagebox.showinfo("Zapisano", f"Plik {self.current_file} został zapisany.\nBackup: {backup_file}")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zapisać pliku: {str(e)}")
            
    def build_structured_content(self):
        """Build content from structured editor"""
        sections = []
        
        for section_key, editor in self.section_editors.items():
            content = editor.get(1.0, tk.END).strip()
            if content:
                sections.append(f"### {section_key} ###\n\n{content}")
                
        return '\n\n'.join(sections)
        
    def reload_current(self):
        """Reload current file"""
        if self.current_file and self.modified:
            response = messagebox.askyesno(
                "Cofnij zmiany",
                "Czy na pewno chcesz cofnąć wszystkie niezapisane zmiany?"
            )
            if response:
                self.load_prompt_file(self.current_file)
                
    def copy_content(self):
        """Copy current content to clipboard"""
        content = self.text_editor.get(1.0, tk.END).strip()
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        messagebox.showinfo("Skopiowano", "Treść promptu została skopiowana do schowka")
        
    def preview_prompt(self):
        """Preview prompt with sample data"""
        content = self.text_editor.get(1.0, tk.END).strip()
        
        # Replace variables with sample data
        sample_data = {
            '{prod_name}': '[Nazwa produktu]',
            '{prod_desclongription}': '[Opis produktu]',
            '{product_specification}': '[Specyfikacja produktu]'
        }
        
        preview_content = content
        for var, value in sample_data.items():
            preview_content = preview_content.replace(var, value)
            
        # Create preview window
        preview_window = tk.Toplevel(self.window)
        preview_window.title("Podgląd promptu")
        preview_window.geometry("800x600")
        
        # Preview text
        preview_text = tk.Text(
            preview_window,
            wrap="word",
            font=("Arial", 11),
            padx=20,
            pady=20
        )
        preview_text.pack(fill="both", expand=True)
        preview_text.insert(1.0, preview_content)
        preview_text.config(state='disabled')
        
    def new_prompt(self):
        """Create a new prompt file"""
        # Ask for filename
        dialog = tk.Toplevel(self.window)
        dialog.title("Nowy prompt")
        dialog.geometry("400x150")
        
        tk.Label(dialog, text="Nazwa pliku (bez rozszerzenia):").pack(pady=10)
        
        entry = tk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.insert(0, "prompt_newdesc_")
        
        def create_file():
            filename = entry.get().strip()
            if not filename:
                messagebox.showerror("Błąd", "Podaj nazwę pliku")
                return
                
            if not filename.startswith('prompt_'):
                filename = 'prompt_' + filename
                
            if not filename.endswith('.txt'):
                filename += '.txt'
                
            # Create in prompts folder
            full_path = os.path.join('prompts', filename)
                
            if os.path.exists(full_path):
                messagebox.showerror("Błąd", "Plik już istnieje")
                return
                
            # Create file with template
            template = """### CEL ###

Chcę, żebyś był ekspertem od copywritingu e-commerce i napisał zoptymalizowany pod SEO i angażujący użytkownika opis produktu dla {{nazwa}}, który będę mógł umieścić na mojej stronie produktu w sklepie e-commerce.

### INSTRUKCJE DODATKOWE ###

Język: polski.
Ton głosu: styl Martyny Wojciechowskiej - przyjazny, pełen pasji, ale profesjonalny.
Formatowanie tekstu: W opisie możesz dodawać następujące tagi HTML: h2, h3, ul, ol, li, table, tr, th, td, p, span. Nie używaj klas i inline style.

### ZMIENNE ###

{{nazwa}} = "{prod_name}"

{{opis}} = "{prod_desclongription}"

### STRUKTURA ###

1. Podsumowanie: "Opis struktury podsumowania"
2. Specyfikacja: "Opis struktury specyfikacji"
"""
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(template)
                
            dialog.destroy()
            self.load_prompt_list()
            
            # Select new file
            for i, mapped_file in self.file_mapping.items():
                if mapped_file == full_path:
                    self.prompt_listbox.selection_clear(0, tk.END)
                    self.prompt_listbox.selection_set(i)
                    self.load_prompt_file(full_path)
                    break
                    
        ttk.Button(dialog, text="Utwórz", command=create_file).pack(pady=10)
        
    def duplicate_prompt(self):
        """Duplicate selected prompt"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz plik do duplikacji")
            return
            
        index = selection[0]
        original_file = self.file_mapping[index]
        
        # Generate new filename
        base_name = os.path.basename(original_file).replace('.txt', '')
        counter = 1
        while os.path.exists(os.path.join('prompts', f"{base_name}_copy{counter}.txt")):
            counter += 1
            
        new_file = os.path.join('prompts', f"{base_name}_copy{counter}.txt")
        
        # Copy file
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        self.load_prompt_list()
        messagebox.showinfo("Sukces", f"Utworzono kopię: {new_file}")
        
    def delete_prompt(self):
        """Delete selected prompt"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz plik do usunięcia")
            return
            
        index = selection[0]
        filename = self.file_mapping[index]
        
        response = messagebox.askyesno(
            "Potwierdź usunięcie",
            f"Czy na pewno chcesz usunąć plik {filename}?\nOperacja jest nieodwracalna!"
        )
        
        if response:
            try:
                # Move to trash instead of deleting
                trash_dir = os.path.join("prompts", "trash")
                os.makedirs(trash_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                trash_file = os.path.join(trash_dir, f"{os.path.basename(filename)}.{timestamp}")
                
                os.rename(filename, trash_file)
                
                self.load_prompt_list()
                messagebox.showinfo("Usunięto", f"Plik został przeniesiony do kosza")
                
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można usunąć pliku: {str(e)}")
                
    def on_close(self):
        """Handle window closing"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Niezapisane zmiany",
                "Masz niezapisane zmiany. Czy chcesz je zapisać?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_prompt()
                
        self.window.destroy()


class PromptManager:
    """Manages prompt files and templates"""
    
    def __init__(self):
        self.prompt_files = {}
        self.load_prompts()
        
    def load_prompts(self):
        """Load all prompt files"""
        # Create prompts folder if it doesn't exist
        if not os.path.exists('prompts'):
            os.makedirs('prompts')
            
        # Check prompts folder
        prompts_dir = 'prompts'
        prompt_files = []
        
        if os.path.exists(prompts_dir):
            prompt_files = [os.path.join(prompts_dir, f) for f in os.listdir(prompts_dir) 
                          if f.startswith('prompt_') and f.endswith('.txt')]
        
        for file_path in prompt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.prompt_files[file_path] = content
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
    def get_prompt_list(self):
        """Get list of available prompts"""
        return list(self.prompt_files.keys())
        
    def get_prompt_content(self, filename):
        """Get content of a specific prompt"""
        return self.prompt_files.get(filename, "")
        
    def save_prompt(self, filename, content):
        """Save prompt content"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        self.prompt_files[filename] = content
        
    def create_backup(self, filename):
        """Create backup of prompt file"""
        if os.path.exists(filename):
            backup_dir = "prompt_backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
            
            with open(filename, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
                    
            return backup_file
        return None