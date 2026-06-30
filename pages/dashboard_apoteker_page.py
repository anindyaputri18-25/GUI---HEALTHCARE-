import tkinter as tk

from data.store import store
from pages.sidebar import AppShell, stat_card

class DashboardApotekerPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="dashboard",
                               title="Dashboard Apoteker")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        stats = store.apoteker_stats()
        grid = tk.Frame(self.shell.content, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        cards = [
            ("Total Obat", stats["total_medicines"], "#2563eb", "💊"),
            ("Total Kategori", stats["total_categories"], "#16a34a", "🗂️"),
            ("Stok Menipis", stats["low_stock_count"], "#dc2626", "⚠️"),
            ("Obat Kadaluarsa", stats["expired_count"], "#ea580c", "⏳"),
            ("Restock Pending", stats["pending_restock_requests"], "#9333ea", "📦"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            r, c = divmod(idx, 3)
            card = stat_card(grid, title, value, color, icon)
            card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

        list_frame = tk.Frame(self.shell.content, bg="white", highlightbackground="#e2e8f0",
                               highlightthickness=1)
        list_frame.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(list_frame, text="Obat Terbaru Ditambahkan", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=18, pady=(14, 8))

        if not stats["recent_medicines"]:
            tk.Label(list_frame, text="Belum ada data obat.", bg="white",
                      fg="#94a3b8", font=("Segoe UI", 9)).pack(padx=18, pady=(0, 14))
        else:
            for med in stats["recent_medicines"]:
                row = tk.Frame(list_frame, bg="white")
                row.pack(fill="x", padx=18, pady=4)
                tk.Label(row, text=f"• {med.get('name', '-')}", bg="white",
                         font=("Segoe UI", 9), fg="#334155", anchor="w").pack(side="left")
                tk.Label(row, text=f"Stok: {med.get('stock', 0)}", bg="white",
                         font=("Segoe UI", 8), fg="#94a3b8").pack(side="right")
            tk.Frame(list_frame, bg="white", height=10).pack()

    def on_show(self):
        self._render()