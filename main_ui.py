import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_utils import get_menu_items, save_order
from calculator import calculate_totals

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Billing Software")
        self.items = []
        self.menu_data = get_menu_items()
        self.menu_lookup = {item[0]: (item[3], item[4]) for item in self.menu_data}

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Order Type:").grid(row=0, column=0, padx=5, pady=5)
        self.order_type = ttk.Combobox(self.root, values=["Dine-in", "Takeaway"], state="readonly")
        self.order_type.grid(row=0, column=1)
        self.order_type.set("Dine-in")

        ttk.Label(self.root, text="Select Item:").grid(row=1, column=0, padx=5, pady=5)
        self.menu_combobox = ttk.Combobox(self.root, values=[f"{item[0]} - {item[1]}" for item in self.menu_data], state="readonly")
        self.menu_combobox.grid(row=1, column=1)

        ttk.Label(self.root, text="Quantity:").grid(row=1, column=2, padx=5, pady=5)
        self.qty_entry = ttk.Entry(self.root, width=5)
        self.qty_entry.grid(row=1, column=3)

        self.add_button = ttk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=1, column=4)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Qty"), show="headings")
        self.tree.heading("ID", text="Item ID")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Qty", text="Quantity")
        self.tree.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

        ttk.Label(self.root, text="Payment Method:").grid(row=3, column=0, padx=5, pady=5)
        self.payment_method = ttk.Combobox(self.root, values=["Cash", "Card", "UPI"], state="readonly")
        self.payment_method.grid(row=3, column=1)
        self.payment_method.set("Cash")

        ttk.Label(self.root, text="Discount:").grid(row=3, column=2, padx=5, pady=5)
        self.discount_entry = ttk.Entry(self.root, width=10)
        self.discount_entry.grid(row=3, column=3)
        self.discount_entry.insert(0, "0")

        self.generate_button = ttk.Button(self.root, text="Generate Bill", command=self.generate_bill)
        self.generate_button.grid(row=3, column=4, padx=5, pady=5)

    def add_item(self):
        item_str = self.menu_combobox.get()
        qty = self.qty_entry.get()
        if item_str and qty.isdigit():
            item_id = int(item_str.split(" - ")[0])
            item_name = item_str.split(" - ")[1]
            self.items.append((item_id, int(qty)))
            self.tree.insert("", tk.END, values=(item_id, item_name, qty))
            self.menu_combobox.set("")
            self.qty_entry.delete(0, tk.END)

    def generate_bill(self):
        if not self.items:
            messagebox.showwarning("No items", "Please add items to the order.")
            return
        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid discount", "Discount must be a number.")
            return

        subtotal, gst, total = calculate_totals(self.items, self.menu_lookup, discount)
        bill = f"Subtotal: ₹{subtotal}\nGST: ₹{gst}\nDiscount: ₹{discount}\nTotal: ₹{total}"
        messagebox.showinfo("Bill Summary", bill)

        order_data = {
            'order_type': self.order_type.get(),
            'total_amount': total,
            'gst_amount': gst,
            'discount': discount,
            'payment_method': self.payment_method.get(),
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_order(order_data, self.items)
        self.items.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
