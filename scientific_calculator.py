import tkinter as tk
import math
from tkinter import ttk

class SimpleScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("360x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")
        
        # Set color variables
        self.dark_bg = "#121212"
        self.button_bg = "#333333"
        self.button_hover = "#444444"
        self.accent = "#ff9500"
        self.text = "#ffffff"
        self.text_secondary = "#aaaaaa"
        
        # Calculator variables
        self.current_input = "0"
        self.current_operation = None
        self.previous_input = None
        self.result = None
        self.should_reset_display = False
        self.degree_mode = True
        self.second_function_mode = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create tabs (Calculator/Converter)
        self.tabs_frame = tk.Frame(self.root, bg=self.dark_bg)
        self.tabs_frame.pack(fill="x", padx=10, pady=10)
        
        self.calc_tab = tk.Label(self.tabs_frame, text="Calculator", font=("Arial", 16, "bold"),
                                bg=self.dark_bg, fg=self.text, padx=15, pady=5)
        self.calc_tab.pack(side="left")
        
        # Add an underline to the active tab
        self.calc_tab.config(font=("Arial", 16, "bold"), fg=self.text)
        tk.Frame(self.tabs_frame, height=2, width=100, bg=self.accent).place(x=10, y=36)
        
        self.conv_tab = tk.Label(self.tabs_frame, text="Converter", font=("Arial", 16),
                                bg=self.dark_bg, fg=self.text_secondary, padx=15, pady=5)
        self.conv_tab.pack(side="left")
        
        # Display frame
        self.display_frame = tk.Frame(self.root, bg=self.dark_bg, height=120)
        self.display_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # History display
        self.history_display = tk.Label(self.display_frame, text="", font=("Arial", 14),
                                      bg=self.dark_bg, fg=self.text_secondary, anchor="e")
        self.history_display.pack(fill="x", padx=10, pady=(10, 5))
        
        # Current display
        self.current_display = tk.Label(self.display_frame, text="0", font=("Arial", 36, "bold"),
                                      bg=self.dark_bg, fg=self.text, anchor="e")
        self.current_display.pack(fill="x", padx=10, pady=5)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=self.dark_bg)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons
        buttons = [
            ("2nd", self.second_function, 0, 0, "function"),
            ("deg", self.toggle_deg_rad, 0, 1, "function"),
            ("sin", lambda: self.calculate("sin"), 0, 2, "function"),
            ("cos", lambda: self.calculate("cos"), 0, 3, "function"),
            
            ("tan", lambda: self.calculate("tan"), 1, 0, "function"),
            ("xʸ", lambda: self.add_operator("^"), 1, 1, "function"),
            ("%", lambda: self.calculate("percent"), 1, 2, "function"),
            ("AC", self.clear_display, 1, 3, "accent"),
            
            ("7", lambda: self.add_to_display("7"), 2, 0, "normal"),
            ("8", lambda: self.add_to_display("8"), 2, 1, "normal"),
            ("9", lambda: self.add_to_display("9"), 2, 2, "normal"),
            ("/", lambda: self.add_operator("/"), 2, 3, "accent"),
            
            ("4", lambda: self.add_to_display("4"), 3, 0, "normal"),
            ("5", lambda: self.add_to_display("5"), 3, 1, "normal"),
            ("6", lambda: self.add_to_display("6"), 3, 2, "normal"),
            ("×", lambda: self.add_operator("*"), 3, 3, "accent"),
            
            ("1", lambda: self.add_to_display("1"), 4, 0, "normal"),
            ("2", lambda: self.add_to_display("2"), 4, 1, "normal"),
            ("3", lambda: self.add_to_display("3"), 4, 2, "normal"),
            ("-", lambda: self.add_operator("-"), 4, 3, "accent"),
            
            ("0", lambda: self.add_to_display("0"), 5, 0, "normal"),
            (".", lambda: self.add_to_display("."), 5, 1, "normal"),
            ("=", lambda: self.calculate("equals"), 5, 2, "accent"),
            ("+", lambda: self.add_operator("+"), 5, 3, "accent"),
        ]
        
        # Store references to the trig buttons to update their text when 2nd is pressed
        self.sin_button = None
        self.cos_button = None
        self.tan_button = None
        
        # Add buttons to the grid
        for (text, command, row, col, style) in buttons:
            # Create a frame for round buttons
            button_frame = tk.Frame(self.buttons_frame, bg=self.dark_bg, width=70, height=60)
            button_frame.grid(row=row, column=col, padx=5, pady=5)
            button_frame.grid_propagate(False)
            
            # Determine button color based on style
            bg_color = self.accent if style == "accent" else self.button_bg
            fg_color = self.text if style != "function" else self.text_secondary
            
            # Create round button
            button = tk.Button(button_frame, text=text, font=("Arial", 14),
                             bg=bg_color, fg=fg_color, bd=0, command=command)
            button.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Make buttons round
            button.config(borderwidth=0, relief="flat", highlightthickness=0)
            
            # Add hover effect
            button.bind("<Enter>", lambda e, b=button: self.on_hover(e, b))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
            
            # Store references to trig buttons
            if text == "sin":
                self.sin_button = button
            elif text == "cos":
                self.cos_button = button
            elif text == "tan":
                self.tan_button = button
    
    def on_hover(self, event, button):
        if button["bg"] == self.accent:
            button.config(bg="#e08700")  # Darker accent color
        else:
            button.config(bg=self.button_hover)
    
    def on_leave(self, event, button):
        if button["bg"] == "#e08700":
            button.config(bg=self.accent)
        else:
            button.config(bg=self.button_bg)
    
    def update_display(self):
        self.current_display.config(text=self.current_input)
    
    def add_to_display(self, value):
        if self.current_input == "0" or self.should_reset_display:
            self.current_input = value
            self.should_reset_display = False
        else:
            self.current_input += value
        self.update_display()
    
    def add_operator(self, operator):
        if self.current_operation is not None:
            self.calculate("equals")
        self.previous_input = self.current_input
        self.current_operation = operator
        self.history_display.config(text=f"{self.previous_input} {operator}")
        self.should_reset_display = True
    
    def clear_display(self):
        self.current_input = "0"
        self.current_operation = None
        self.previous_input = None
        self.history_display.config(text="")
        self.update_display()
    
    def toggle_deg_rad(self):
        self.degree_mode = not self.degree_mode
        button_text = "deg" if self.degree_mode else "rad"
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for b in widget.winfo_children():
                    if isinstance(b, tk.Button) and b["text"] in ["deg", "rad"]:
                        b.config(text=button_text)
    
    def second_function(self):
        self.second_function_mode = not self.second_function_mode
        
        if self.second_function_mode:
            self.sin_button.config(text="sin⁻¹")
            self.cos_button.config(text="cos⁻¹")
            self.tan_button.config(text="tan⁻¹")
        else:
            self.sin_button.config(text="sin")
            self.cos_button.config(text="cos")
            self.tan_button.config(text="tan")
    
    def to_radians(self, angle):
        return angle * (math.pi / 180) if self.degree_mode else angle
    
    def to_degrees(self, angle):
        return angle * (180 / math.pi) if self.degree_mode else angle
    
    def calculate(self, operation):
        try:
            num = float(self.current_input)
            
            if operation == "equals" and self.current_operation:
                prev = float(self.previous_input)
                
                if self.current_operation == "+":
                    self.result = prev + num
                elif self.current_operation == "-":
                    self.result = prev - num
                elif self.current_operation == "*":
                    self.result = prev * num
                elif self.current_operation == "/":
                    if num == 0:
                        self.result = "Error"
                    else:
                        self.result = prev / num
                elif self.current_operation == "^":
                    self.result = prev ** num
                
                self.history_display.config(text=f"{self.previous_input} {self.current_operation} {self.current_input} =")
                self.current_input = str(self.result) if self.result != "Error" else "Error"
                self.current_operation = None
                self.should_reset_display = True
                self.update_display()
                return
            
            if operation == "sin":
                if self.second_function_mode:
                    if num < -1 or num > 1:
                        self.result = "Error"
                    else:
                        self.result = self.to_degrees(math.asin(num))
                else:
                    self.result = math.sin(self.to_radians(num))
            
            elif operation == "cos":
                if self.second_function_mode:
                    if num < -1 or num > 1:
                        self.result = "Error"
                    else:
                        self.result = self.to_degrees(math.acos(num))
                else:
                    self.result = math.cos(self.to_radians(num))
            
            elif operation == "tan":
                if self.second_function_mode:
                    self.result = self.to_degrees(math.atan(num))
                else:
                    # Check for invalid tan input (90, 270, etc. degrees)
                    angle_rad = self.to_radians(num)
                    if self.degree_mode and (abs(num) % 180 == 90):
                        self.result = "Error"
                    else:
                        self.result = math.tan(angle_rad)
            
            elif operation == "percent":
                if self.current_operation and self.previous_input is not None:
                    prev = float(self.previous_input)
                    self.result = (prev * num) / 100
                else:
                    self.result = num / 100
            
            if str(self.result) == "Error":
                self.current_input = "Error"
            elif self.result is not None:
                self.history_display.config(text=f"{operation}({num})")
                self.current_input = str(self.result)
            
            self.should_reset_display = True
            self.update_display()
            
        except ValueError:
            self.current_input = "Error"
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleScientificCalculator(root)
    root.mainloop()