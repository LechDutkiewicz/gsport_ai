# html_text_widget.py
import tkinter as tk
import re

class HTMLTextWidget(tk.Text):
    """Text widget with HTML syntax highlighting"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure tags for syntax highlighting
        self.tag_configure("html_tag", foreground="#0066CC")
        self.tag_configure("html_attribute", foreground="#009900")
        self.tag_configure("html_value", foreground="#CC0000")
        self.tag_configure("html_comment", foreground="#666666", font=("Arial", 10, "italic"))
        
        # Bind events
        self.bind("<<Modified>>", self._on_change)
        self.bind("<KeyRelease>", self._on_key_release)
        
    def _on_change(self, event=None):
        """Handle text change events"""
        self.highlight_syntax()
        
    def _on_key_release(self, event=None):
        """Handle key release events"""
        # Only highlight on certain keys to improve performance
        if event.keysym in ['greater', 'less', 'quotedbl', 'apostrophe', 'space', 'Return']:
            self.highlight_syntax()
            
    def highlight_syntax(self):
        """Apply syntax highlighting to HTML content"""
        # Remove all existing tags
        for tag in ["html_tag", "html_attribute", "html_value", "html_comment"]:
            self.tag_remove(tag, "1.0", "end")
            
        content = self.get("1.0", "end-1c")
        
        # Highlight HTML comments
        for match in re.finditer(r'<!--.*?-->', content, re.DOTALL):
            start = self.index(f"1.0+{match.start()}c")
            end = self.index(f"1.0+{match.end()}c")
            self.tag_add("html_comment", start, end)
            
        # Highlight HTML tags and attributes
        tag_pattern = r'<(/?)(\w+)((?:\s+\w+(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?)*)\s*(/?)>'
        
        for match in re.finditer(tag_pattern, content):
            # Tag name
            tag_start = self.index(f"1.0+{match.start()}c")
            tag_name_start = match.start() + len(match.group(1)) + 1
            tag_name_end = tag_name_start + len(match.group(2))
            
            self.tag_add("html_tag", 
                        self.index(f"1.0+{match.start()}c"),
                        self.index(f"1.0+{match.start() + 1}c"))
            
            self.tag_add("html_tag",
                        self.index(f"1.0+{tag_name_start}c"),
                        self.index(f"1.0+{tag_name_end}c"))
            
            # Closing bracket
            self.tag_add("html_tag",
                        self.index(f"1.0+{match.end() - 1}c"),
                        self.index(f"1.0+{match.end()}c"))
            
            # Attributes
            attr_string = match.group(3)
            if attr_string:
                attr_pattern = r'(\w+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?'
                attr_start_pos = tag_name_end
                
                for attr_match in re.finditer(attr_pattern, attr_string):
                    attr_pos = match.start() + len(match.group(1)) + 1 + len(match.group(2)) + attr_match.start()
                    
                    # Attribute name
                    self.tag_add("html_attribute",
                               self.index(f"1.0+{attr_pos}c"),
                               self.index(f"1.0+{attr_pos + len(attr_match.group(1))}c"))
                    
                    # Attribute value
                    if attr_match.group(2) is not None:  # Double quotes
                        value_start = attr_pos + len(attr_match.group(1)) + attr_match.group(0).find('"')
                        self.tag_add("html_value",
                                   self.index(f"1.0+{value_start}c"),
                                   self.index(f"1.0+{value_start + len(attr_match.group(2)) + 2}c"))
                    elif attr_match.group(3) is not None:  # Single quotes
                        value_start = attr_pos + len(attr_match.group(1)) + attr_match.group(0).find("'")
                        self.tag_add("html_value",
                                   self.index(f"1.0+{value_start}c"),
                                   self.index(f"1.0+{value_start + len(attr_match.group(3)) + 2}c"))
                    elif attr_match.group(4) is not None:  # No quotes
                        value_start = attr_pos + len(attr_match.group(1)) + attr_match.group(0).find('=') + 1
                        self.tag_add("html_value",
                                   self.index(f"1.0+{value_start}c"),
                                   self.index(f"1.0+{value_start + len(attr_match.group(4))}c"))
                                   
    def insert(self, index, text, *args):
        """Override insert to trigger highlighting"""
        super().insert(index, text, *args)
        self.highlight_syntax()
        
    def delete(self, start, end=None):
        """Override delete to trigger highlighting"""
        super().delete(start, end)
        self.highlight_syntax()