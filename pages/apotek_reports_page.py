import tkinter as tk
from datetime import date

from data.store import store
from pages.sidebar import AppShell, stat_card
from pages.widgets import make_table

class ApotekReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="apotek_reports", title="Laporan Stok Obat")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        today = date.today().isoformat()
        low = sum(1 for m in store.medicines if m["stock"] <= m["min_stock"])
        expired = sum(1 for m in store.medicines if m["expiration_date"] < today)
        total_value = sum(m["stock"] * m["purchase_price"] for m in store.medicines)

        grid = tk.Frame(self.shell.content, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)
        cards = [
            ("Total Jenis Obat", len(store.medicines), "#2563eb", "💊"),
            ("Stok Menipis", low, "#dc2626", "⚠️"),
            ("Sudah Kadaluarsa", expired, "#ea580c", "⏳"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            c = stat_card(grid, title, value, color, icon)
            c.grid(row=0, column=idx, sticky="nsew", padx=8, pady=8)

        tk.Label(self.shell.content, text=f"Estimasi nilai total stok (harga beli): Rp{total_value:,.0f}",
                 font=("Segoe UI", 9, "bold"), bg="#f1f5f9", fg="#334155").pack(anchor="w", pady=(10, 8))

        columns = [("name", "Nama Obat", 180), ("category", "Kategori", 120), ("stock", "Stok", 70),
                   ("min_stock", "Min.", 60), ("expired", "Kadaluarsa", 100), ("status", "Status", 130)]
        table_frame, tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        tree.tag_configure("low", foreground="#dc2626")
        tree.tag_configure("expired", foreground="#b91c1c", background="#fee2e2")

        for m in sorted(store.medicines, key=lambda x: x["stock"]):
            cat_name = store.lookup_name(store.medicine_categories, m["category_id"])
            status = "Aman"
            tag = ()
            if m["expiration_date"] < today:
                status = "Kadaluarsa"
                tag = ("expired",)
            elif m["stock"] <= m["min_stock"]:
                status = "Stok Menipis"
                tag = ("low",)
            tree.insert("", "end", tags=tag, values=(
                m["name"], cat_name, m["stock"], m["min_stock"], m["expiration_date"], status))

    def on_show(self):
        self._render()