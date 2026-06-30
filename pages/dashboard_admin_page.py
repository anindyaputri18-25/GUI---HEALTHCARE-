import tkinter as tk

from data.store import store
from pages.sidebar import AppShell, stat_card


class DashboardAdminPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="dashboard",
                               title="Dashboard Administrator")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        stats = store.admin_stats()
        grid = tk.Frame(self.shell.content, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        cards = [
            ("Total Pengguna", stats["total_users"], "#2563eb", "👥"),
            ("Total Obat", stats["total_medicines"], "#16a34a", "💊"),
            ("Stok Menipis", stats["low_stock_count"], "#dc2626", "⚠️"),
            ("Laporan Penyakit", stats["total_disease_reports"], "#9333ea", "🦠"),
            ("Data Anak", stats["total_children"], "#0891b2", "🧒"),
            ("Restock Pending", stats["pending_restocks"], "#ea580c", "📦"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            r, c = divmod(idx, 3)
            card = stat_card(grid, title, value, color, icon)
            card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

        # Log aktivitas terbaru
        log_frame = tk.Frame(self.shell.content, bg="white", highlightbackground="#e2e8f0",
                              highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(log_frame, text="Log Aktivitas Terbaru", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=18, pady=(14, 8))

        if not stats["recent_logs"]:
            tk.Label(log_frame, text="Belum ada aktivitas tercatat.", bg="white",
                      fg="#94a3b8", font=("Segoe UI", 9)).pack(padx=18, pady=(0, 14))
        else:
            for log in stats["recent_logs"]:
                row = tk.Frame(log_frame, bg="white")
                row.pack(fill="x", padx=18, pady=4)
                tk.Label(row, text=f"• {log['description']}", bg="white",
                         font=("Segoe UI", 9), fg="#334155", anchor="w").pack(side="left")
                tk.Label(row, text=log["created_at"], bg="white", font=("Segoe UI", 8),
                         fg="#94a3b8").pack(side="right")
            tk.Frame(log_frame, bg="white", height=10).pack()

    def on_show(self):
        self._render()