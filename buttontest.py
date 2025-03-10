import tkinter as tk
from tkinter import messagebox, ttk

class ModelCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Model Counter Dashboard")
        
        # Model costs
        self.model_costs = {'Model1': 3, 'Model2': 5, 'Model3': 6}
        
        # Counters for each model
        self.model_counts = {'Model1': 0, 'Model2': 0, 'Model3': 0}
        
        # Total cost
        self.total_cost = 0   
        
        # Create buttons
        self.create_buttons()
        
        # Create dashboard button
        self.dashboard_button = ttk.Button(root, text="Show Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(pady=10)
    
    def create_buttons(self):
        for model in self.model_costs:
            button = ttk.Button(self.root, text=model, command=lambda m=model: self.update_count(m))
            button.pack(pady=5)
    
    def update_count(self, model):
        self.model_counts[model] += 1
        self.total_cost += self.model_costs[model]
        messagebox.showinfo("Update", f"Added {model}. Total {model} count: {self.model_counts[model]}")
    
    def show_dashboard(self):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard")

        title_label = ttk.Label(dashboard_window, text="Model Counter Dashboard", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)

        tree = ttk.Treeview(dashboard_window, columns=("Count", "Total Cost"), show='headings')
        tree.heading("Count", text="Count")
        tree.heading("Total Cost", text="Total Cost (Rs)")
        
        for model, count in self.model_counts.items():
            tree.insert("", "end", values=(model, count, count * self.model_costs[model]))
        
        tree.pack(pady=10)

        total_cost_label = ttk.Label(dashboard_window, text=f"Total Cost of all models: {self.total_cost} Rs", font=('Helvetica', 12))
        total_cost_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModelCounterApp(root)
    root.mainloop()
