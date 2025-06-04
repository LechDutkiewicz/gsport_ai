# main.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from product_manager import ProductManager
from prompt_editor import PromptEditor, PromptManager

class ProductManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        
        # Initialize the product manager
        self.product_manager = ProductManager(self)
        
        # Initialize prompt manager
        self.prompt_manager = PromptManager()
        
        # Create UI
        self.create_widgets()
        
        # Bind auto-load functionality
        self.setup_bindings()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.configure(background="#FFFFFF", padx=0, pady=0)
        self.root.title("GSPORT Redaktor Opisów 2.0")
        self.root.geometry("{}x{}+0+0".format(
            self.root.winfo_screenwidth(), 
            self.root.winfo_screenheight()
        ))
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton', 
                       background='#222645',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 6))
        style.map('Primary.TButton',
                 background=[('active', '#333756')])
        
        style.configure('Secondary.TButton',
                       background='#F7F7F7',
                       foreground='black',
                       borderwidth=1,
                       padding=(12, 6))
        style.map('Secondary.TButton',
                 background=[('active', '#E0E0E0')])
        
        style.configure('Success.TButton',
                       background='#BFE02B',
                       foreground='black',
                       borderwidth=0,
                       padding=(12, 6))
        style.map('Success.TButton',
                 background=[('active', '#A0C020')])
        
        style.configure('Danger.TButton',
                       background='#E24B38',
                       foreground='white',
                       borderwidth=0,
                       padding=(12, 6))
        style.map('Danger.TButton',
                 background=[('active', '#C03020')])
        
        # Compact style for preview buttons
        style.configure('Compact.TButton',
                       background='#F7F7F7',
                       foreground='black',
                       borderwidth=1,
                       padding=(8, 4),
                       font=('Arial', 9))
        style.map('Compact.TButton',
                 background=[('active', '#E0E0E0')])
                 
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg="#FFFFFF")
        main_container.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar(main_container)
        
        # Create main content area
        self.create_main_content(main_container)
        
    def create_sidebar(self, parent):
        """Create left sidebar with product info and utility buttons"""
        sidebar = tk.Frame(parent, bg="#F0F0F0", width=350)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Sidebar title
        title_frame = tk.Frame(sidebar, bg="#222645", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Informacje o produkcie",
            font=("Arial", 14, "bold"),
            bg="#222645",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Product input section
        self.create_product_input_section(sidebar)
        
        # Product parameters section
        self.create_parameters_section(sidebar)
        
        # Similar products section
        self.create_similar_products_section(sidebar)
        
        # Spacer to push buttons to bottom
        spacer = tk.Frame(sidebar, bg="#F0F0F0")
        spacer.pack(fill="both", expand=True)
        
        # Utility buttons at bottom
        self.create_utility_buttons(sidebar)
        
    def create_product_input_section(self, parent):
        """Create product input section in sidebar"""
        section = tk.Frame(parent, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=15)
        
        # Inner container with padding
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=20)
        
        # Input label
        input_label = tk.Label(
            inner,
            text="ID lub link do produktu",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#666666"
        )
        input_label.pack(anchor="w", pady=(0, 5))
        
        # Product ID/Link entry
        self.input_product_link = tk.Entry(inner, width=35, font=("Arial", 11))
        self.input_product_link.pack(fill="x", pady=(0, 15))
        
        # Product image
        self.image_frame = tk.Frame(
            inner,
            bg="#E5E5E5",
            width=120,
            height=120
        )
        self.image_frame.pack(pady=(0, 10))
        self.image_frame.pack_propagate(False)
        
        self.lbl_product_image = tk.Label(
            self.image_frame,
            text="[Brak obrazu]",
            bg="#E5E5E5",
            fg="#999999"
        )
        self.lbl_product_image.pack(expand=True)
        
        # Product name label with smaller font
        self.lbl_prod_name = tk.Label(
            inner, 
            text="[Nazwa produktu]",
            bg="#FFFFFF",
            font=("Arial", 10),
            wraplength=280,
            justify="center"
        )
        self.lbl_prod_name.pack(pady=(0, 15))
        
        # Producer status frame - horizontal layout
        status_frame = tk.Frame(inner, bg="#FFFFFF")
        status_frame.pack()
        
        self.lbl_producer_present = tk.Label(
            status_frame, 
            text="Producent", 
            bg='#dedede',
            padx=10,
            pady=5,
            font=("Arial", 9)
        )
        self.lbl_producer_present.pack(side="left", padx=2)
        
        self.lbl_producerdesc_present = tk.Label(
            status_frame, 
            text="Opis producenta", 
            bg='#dedede',
            padx=10,
            pady=5,
            font=("Arial", 9)
        )
        self.lbl_producerdesc_present.pack(side="left", padx=2)
        
    def create_parameters_section(self, parent):
        """Create product parameters section in sidebar"""
        section = tk.Frame(parent, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=(0, 15))
        
        # Inner container
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=15)
        
        # Section label
        label = tk.Label(
            inner,
            text="Parametry produktu",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        label.pack(anchor="w", pady=(0, 10))
        
        # Color selector
        self.create_color_selector(inner)
        
    def create_color_selector(self, parent):
        """Create color selector with dropdown"""
        # Color frame
        color_frame = tk.Frame(parent, bg="#FFFFFF")
        color_frame.pack(fill="x", pady=(0, 10))
        
        # Label
        color_label = tk.Label(
            color_frame,
            text="Kolor dominujący:",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#666666"
        )
        color_label.pack(anchor="w", pady=(0, 5))
        
        # Colors with their hex codes and remote_ids
        self.colors = {
            'szary': {'hex': '#808080', 'name': 'Szary', 'remote_id': '10241'},
            'wielokolorowy': {'hex': 'multi', 'name': 'Wielokolorowy', 'remote_id': '10265'},
            'czarny': {'hex': '#000000', 'name': 'Czarny', 'remote_id': '10294'},
            'niebieski': {'hex': '#0000ff', 'name': 'Niebieski', 'remote_id': '10302'},
            'pomarańczowy': {'hex': '#ffa500', 'name': 'Pomarańczowy', 'remote_id': '10481'},
            'biały': {'hex': '#f7f7f7', 'name': 'Biały', 'remote_id': '10567'},
            'fioletowy': {'hex': '#800080', 'name': 'Fioletowy', 'remote_id': '10579'},
            'czerwony': {'hex': '#ff0000', 'name': 'Czerwony', 'remote_id': '10597'},
            'różowy': {'hex': '#ffc0cb', 'name': 'Różowy', 'remote_id': '10627'},
            'żółty': {'hex': '#ffff00', 'name': 'Żółty', 'remote_id': '11060'},
            'zielony': {'hex': '#008000', 'name': 'Zielony', 'remote_id': '11287'},
            'brązowy': {'hex': '#a52a2a', 'name': 'Brązowy', 'remote_id': '23465'},
            'złoty': {'hex': '#ebd271', 'name': 'Złoty', 'remote_id': '23491'}
        }
        
        # Create mapping from remote_id to color key
        self.color_by_remote_id = {data['remote_id']: key for key, data in self.colors.items()}
        
        # Store selected color
        self.selected_color = tk.StringVar(value="")
        
        # Create dropdown frame with color preview
        dropdown_frame = tk.Frame(color_frame, bg="#FFFFFF")
        dropdown_frame.pack(fill="x")
        
        # Color preview box
        self.color_preview = tk.Frame(
            dropdown_frame,
            width=30,
            height=30,
            bg="#E5E5E5",
            relief="solid",
            bd=1
        )
        self.color_preview.pack(side="left", padx=(0, 10))
        
        # Dropdown menu
        color_options = [""] + [f"{data['name']}" for data in self.colors.values()]
        self.color_dropdown = ttk.Combobox(
            dropdown_frame,
            values=color_options,
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        self.color_dropdown.pack(side="left", fill="x", expand=True)
        self.color_dropdown.bind("<<ComboboxSelected>>", self.on_color_selected)
        
        # Clear button
        self.btn_clear_color = tk.Button(
            dropdown_frame,
            text="✕",
            font=("Arial", 10),
            bg="#F0F0F0",
            fg="#666666",
            bd=1,
            relief="solid",
            width=3,
            command=self.clear_color_selection,
            state="disabled"
        )
        self.btn_clear_color.pack(side="left", padx=(5, 0))
        
    def on_color_selected(self, event):
        """Handle color selection from dropdown"""
        selected_name = self.color_dropdown.get()
        
        if not selected_name:
            self.clear_color_selection()
            return
            
        # Find the color key by name
        color_key = None
        for key, data in self.colors.items():
            if data['name'] == selected_name:
                color_key = key
                break
                
        if color_key:
            self.select_color(color_key)
            
    def select_color(self, color_key):
        """Handle color selection"""
        # Update selected color
        self.selected_color.set(color_key)
        
        # Update preview box
        color_data = self.colors[color_key]
        if color_data['hex'] == 'multi':
            # Multi-color preview
            self.color_preview.config(bg="#FFFFFF")
            # Add rainbow label if not exists
            if not hasattr(self, 'rainbow_label'):
                self.rainbow_label = tk.Label(
                    self.color_preview,
                    text="🌈",
                    bg="#FFFFFF",
                    font=("Arial", 14)
                )
            self.rainbow_label.pack(expand=True)
        else:
            # Solid color preview
            self.color_preview.config(bg=color_data['hex'])
            # Remove rainbow label if exists
            if hasattr(self, 'rainbow_label'):
                self.rainbow_label.pack_forget()
        
        # Update dropdown
        self.color_dropdown.set(color_data['name'])
        
        # Enable clear button
        self.btn_clear_color.config(state="normal")
        
        # Notify product manager
        if hasattr(self, 'product_manager'):
            self.product_manager.set_product_color(color_key, color_data['remote_id'])
    
    def clear_color_selection(self):
        """Clear color selection"""
        self.selected_color.set("")
        
        # Reset preview
        self.color_preview.config(bg="#E5E5E5")
        if hasattr(self, 'rainbow_label'):
            self.rainbow_label.pack_forget()
        
        # Reset dropdown
        self.color_dropdown.set("")
        
        # Disable clear button
        self.btn_clear_color.config(state="disabled")
        
        # Notify product manager
        if hasattr(self, 'product_manager'):
            self.product_manager.set_product_color(None, None)
            
    def set_color_from_remote_id(self, remote_id):
        """Set color selection from remote_id (used when loading product)"""
        if remote_id in self.color_by_remote_id:
            color_key = self.color_by_remote_id[remote_id]
            self.select_color(color_key)
        
    def create_similar_products_section(self, parent):
        """Create similar products section in sidebar"""
        section = tk.Frame(parent, bg="#FFFFFF", relief="flat", bd=1)
        section.pack(fill="x", padx=15, pady=(0, 15))
        
        # Inner container
        inner = tk.Frame(section, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=15)
        
        # Section label
        label = tk.Label(
            inner,
            text="Podobne produkty",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#666666"
        )
        label.pack(anchor="w", pady=(0, 10))
        
        # Similar product entries
        self.similar_product_entries = []
        for i in range(5):
            entry = tk.Entry(inner, width=35, font=("Arial", 9))
            entry.pack(fill="x", pady=2)
            self.similar_product_entries.append(entry)
            
    def create_utility_buttons(self, parent):
        """Create utility buttons at bottom of sidebar"""
        button_frame = tk.Frame(parent, bg="#F0F0F0")
        button_frame.pack(fill="x", padx=15, pady=15)
        
        # Prompt editor button
        self.btn_prompt_editor = ttk.Button(
            button_frame,
            text='Edytor promptów',
            command=self.open_prompt_editor,
            style='Secondary.TButton'
        )
        self.btn_prompt_editor.pack(fill="x", pady=(0, 10))
        
        # Clear all button
        self.btn_reset = ttk.Button(
            button_frame,
            text="Wyczyść wszystko",
            command=self.product_manager.clear_all_fields,
            style='Danger.TButton'
        )
        self.btn_reset.pack(fill="x")
        
    def create_main_content(self, parent):
        """Create main content area with buttons and content sections"""
        main_area = tk.Frame(parent, bg="#F9F9F9")
        main_area.pack(side="left", fill="both", expand=True)
        
        # Top control panel
        self.create_control_panel(main_area)
        
        # Content area
        self.create_content_area(main_area)
        
    def create_control_panel(self, parent):
        """Create top control panel with action buttons"""
        control_panel = tk.Frame(parent, bg="#FFFFFF", height=110, relief="flat", bd=1)
        control_panel.pack(fill="x", padx=20, pady=(20, 10))
        control_panel.pack_propagate(False)
        
        # Inner container
        inner = tk.Frame(control_panel, bg="#FFFFFF")
        inner.pack(fill="both", padx=20, pady=20)
        
        # Data import section
        import_frame = tk.Frame(inner, bg="#FFFFFF")
        import_frame.pack(side="left", padx=(0, 40))
        
        import_label = tk.Label(
            import_frame,
            text="Import danych",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        import_label.pack(anchor="w", pady=(0, 5))
        
        import_buttons = tk.Frame(import_frame, bg="#FFFFFF")
        import_buttons.pack()
        
        self.btn_paste_desc = ttk.Button(
            import_buttons,
            text='Wgraj opis',
            command=self.product_manager.paste_description,
            style='Secondary.TButton'
        )
        self.btn_paste_desc.pack(side="left", padx=3)
        
        self.btn_paste_json = ttk.Button(
            import_buttons,
            text='JSON',
            command=self.product_manager.paste_specification_json,
            style='Secondary.TButton'
        )
        self.btn_paste_json.pack(side="left", padx=3)
        
        self.btn_paste_spec = ttk.Button(
            import_buttons,
            text='HTML',
            command=self.product_manager.paste_specification,
            style='Secondary.TButton'
        )
        self.btn_paste_spec.pack(side="left", padx=3)
        
        # Generation section
        gen_frame = tk.Frame(inner, bg="#FFFFFF")
        gen_frame.pack(side="left", padx=(0, 40))
        
        gen_label = tk.Label(
            gen_frame,
            text="Generowanie",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        gen_label.pack(anchor="w", pady=(0, 5))
        
        gen_controls = tk.Frame(gen_frame, bg="#FFFFFF")
        gen_controls.pack()
        
        # Product type toggle
        self.is_bike_var = tk.BooleanVar(value=True)
        self.chk_is_bike = tk.Checkbutton(
            gen_controls,
            text="Rower",
            variable=self.is_bike_var,
            bg="#FFFFFF",
            font=("Arial", 11, "bold")
        )
        self.chk_is_bike.pack(side="left", padx=(0, 15))
        
        self.btn_generate = ttk.Button(
            gen_controls,
            text='Generuj AI',
            command=self.product_manager.generate_description,
            style='Primary.TButton'
        )
        self.btn_generate.pack(side="left")
        
        # Save section
        save_frame = tk.Frame(inner, bg="#FFFFFF")
        save_frame.pack(side="left")
        
        save_label = tk.Label(
            save_frame,
            text="Zapis",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#444444"
        )
        save_label.pack(anchor="w", pady=(0, 5))
        
        self.btn_update = ttk.Button(
            save_frame,
            text="Zapisz w sklepie",
            command=self.product_manager.update_products,
            style='Success.TButton',
            state=tk.DISABLED
        )
        self.btn_update.pack()
        
        # Cost display
        self.lbl_cost = tk.Label(
            inner,
            text="",
            bg="#FFFFFF",
            font=("Arial", 10),
            fg="#666666"
        )
        self.lbl_cost.pack(side="right", padx=20)
        
    def create_content_area(self, parent):
        """Create content display area"""
        # Import here to avoid circular import
        from tkinterweb import HtmlFrame
        
        content_frame = tk.Frame(parent, bg="#F9F9F9")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid weights for better sizing
        content_frame.columnconfigure(0, weight=2)  # Reduced for original desc
        content_frame.columnconfigure(1, weight=3)  # Specs columns
        content_frame.columnconfigure(2, weight=2)  # Increased for AI content
        content_frame.rowconfigure(0, weight=2)     # More weight for long descriptions
        content_frame.rowconfigure(1, weight=2)     # Less weight for bottom row
        
        # Original product description - smaller
        frame_original = tk.LabelFrame(
            content_frame,
            text="Opis produktu ze sklepu",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_original.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.html_original_desc = HtmlFrame(frame_original, messages_enabled=False)
        self.html_original_desc.pack(fill="both", expand=True)
        
        # Specifications
        frame_spec_json = tk.LabelFrame(
            content_frame,
            text="Specyfikacja JSON",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_spec_json.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.html_spec_json = HtmlFrame(frame_spec_json, messages_enabled=False)
        self.html_spec_json.pack(fill="both", expand=True)
        
        frame_spec_html = tk.LabelFrame(
            content_frame,
            text="Specyfikacja HTML",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_spec_html.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        self.html_spec_html = HtmlFrame(frame_spec_html, messages_enabled=False)
        self.html_spec_html.pack(fill="both", expand=True)
        
        # AI generated descriptions - larger
        frame_ai_long = tk.LabelFrame(
            content_frame,
            text="Długi opis AI (edytowalny)",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_ai_long.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Container for long description with button
        long_container = tk.Frame(frame_ai_long, bg="#FFFFFF")
        long_container.pack(fill="both", expand=True)
        
        # Button frame at top
        long_button_frame = tk.Frame(long_container, bg="#FFFFFF", height=35)
        long_button_frame.pack(fill="x", side="top")
        long_button_frame.pack_propagate(False)
        
        # Preview button for long description - positioned at top right
        self.btn_preview_long = ttk.Button(
            long_button_frame,
            text="Podgląd HTML",
            command=lambda: self.product_manager.preview_html('long'),
            style='Compact.TButton'
        )
        self.btn_preview_long.pack(side="right", padx=5, pady=5)
        
        # Text editor frame
        text_frame_long = tk.Frame(long_container, bg="#FFFFFF")
        text_frame_long.pack(fill="both", expand=True, side="top")
        
        scrollbar_long = tk.Scrollbar(text_frame_long)
        scrollbar_long.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_ai_long = tk.Text(
            text_frame_long,
            wrap=tk.WORD,
            yscrollcommand=scrollbar_long.set,
            font=("Consolas", 11),
            padx=10,
            pady=10,
            bg="#FAFAFA"
        )
        self.text_ai_long.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar_long.config(command=self.text_ai_long.yview)
        
        # Configure syntax highlighting tags for long description
        self.setup_syntax_highlighting(self.text_ai_long)
        
        # Short description frame
        frame_ai_short = tk.LabelFrame(
            content_frame,
            text="Krótki opis AI (edytowalny)",
            padx=10,
            pady=10,
            bg="#FFFFFF",
            font=("Arial", 10)
        )
        frame_ai_short.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        # Container for short description with button
        short_container = tk.Frame(frame_ai_short, bg="#FFFFFF")
        short_container.pack(fill="both", expand=True)
        
        # Button frame at top
        short_button_frame = tk.Frame(short_container, bg="#FFFFFF", height=35)
        short_button_frame.pack(fill="x", side="top")
        short_button_frame.pack_propagate(False)
        
        # Preview button for short description - positioned at top right
        self.btn_preview_short = ttk.Button(
            short_button_frame,
            text="Podgląd HTML",
            command=lambda: self.product_manager.preview_html('short'),
            style='Compact.TButton'
        )
        self.btn_preview_short.pack(side="right", padx=5, pady=5)
        
        # Text editor frame
        text_frame_short = tk.Frame(short_container, bg="#FFFFFF")
        text_frame_short.pack(fill="both", expand=True, side="top")
        
        scrollbar_short = tk.Scrollbar(text_frame_short)
        scrollbar_short.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_ai_short = tk.Text(
            text_frame_short,
            wrap=tk.WORD,
            yscrollcommand=scrollbar_short.set,
            font=("Consolas", 11),
            padx=10,
            pady=10,
            bg="#FAFAFA"
        )
        self.text_ai_short.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar_short.config(command=self.text_ai_short.yview)
        
        # Configure syntax highlighting tags for short description
        self.setup_syntax_highlighting(self.text_ai_short)
        
    def setup_syntax_highlighting(self, text_widget):
        """Configure syntax highlighting for HTML in text widget"""
        # Tag configuration for HTML syntax
        text_widget.tag_configure("html_tag", foreground="#0066CC", font=("Consolas", 11, "bold"))
        text_widget.tag_configure("html_attribute", foreground="#009900")
        text_widget.tag_configure("html_value", foreground="#CC0000")
        text_widget.tag_configure("html_content", foreground="#333333")
        
        # Bind events for syntax highlighting
        text_widget.bind("<KeyRelease>", lambda e: self.highlight_syntax(text_widget))
        text_widget.bind("<<Paste>>", lambda e: self.root.after(10, lambda: self.highlight_syntax(text_widget)))
        
    def highlight_syntax(self, text_widget):
        """Apply syntax highlighting to HTML content"""
        import re
        
        # Remove all existing tags
        for tag in ["html_tag", "html_attribute", "html_value"]:
            text_widget.tag_remove(tag, "1.0", "end")
            
        content = text_widget.get("1.0", "end-1c")
        
        # Highlight HTML tags
        for match in re.finditer(r'</?(\w+)(?:\s+[^>]*)?>|</\w+>', content):
            start = text_widget.index(f"1.0+{match.start()}c")
            end = text_widget.index(f"1.0+{match.end()}c")
            text_widget.tag_add("html_tag", start, end)
            
        # Highlight attributes and values
        for match in re.finditer(r'(\w+)=(["\'])([^"\']*)\2', content):
            # Attribute name
            attr_start = text_widget.index(f"1.0+{match.start(1)}c")
            attr_end = text_widget.index(f"1.0+{match.end(1)}c")
            text_widget.tag_add("html_attribute", attr_start, attr_end)
            
            # Attribute value (including quotes)
            val_start = text_widget.index(f"1.0+{match.start(2)}c")
            val_end = text_widget.index(f"1.0+{match.end(3)}c")
            text_widget.tag_add("html_value", val_start, val_end)
        
    def open_prompt_editor(self):
        """Open the prompt editor window"""
        PromptEditor(self.root, self.prompt_manager)
        
    def on_product_input_change(self):
        """Handle product input change"""
        current_value = self.input_product_link.get().strip()
        if current_value and current_value != getattr(self, '_last_product_input', ''):
            self._last_product_input = current_value
            self.product_manager.load_product_data()
            
    def on_text_modified(self, field_type):
        """Handle text modification events"""
        if field_type == 'long' and self.text_ai_long.edit_modified():
            # Trigger syntax highlighting
            self.highlight_syntax(self.text_ai_long)
            self.text_ai_long.edit_modified(False)
        elif field_type == 'short' and self.text_ai_short.edit_modified():
            # Trigger syntax highlighting
            self.highlight_syntax(self.text_ai_short)
            self.text_ai_short.edit_modified(False)
            
    def update_field_status(self, field_type, modified):
        """Update field label to show modification status"""
        # Disabled for now due to layout changes
        pass
        
    def setup_bindings(self):
        """Setup event bindings"""
        # Auto-load product when Enter is pressed or focus is lost
        self.input_product_link.bind('<Return>', lambda e: self.product_manager.load_product_data())
        self.input_product_link.bind('<FocusOut>', lambda e: self.on_product_input_change())
        
        # Track text changes in editable fields
        self.text_ai_long.bind('<<Modified>>', lambda e: self.on_text_modified('long'))
        self.text_ai_short.bind('<<Modified>>', lambda e: self.on_text_modified('short'))
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductManagerApp()
    app.run()