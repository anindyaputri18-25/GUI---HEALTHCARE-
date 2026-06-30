import tkinter as tk

from data.store import store
from pages.sidebar import AppShell, stat_card

class DashboardWargaPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="dashboard",
                               title="Dashboard Warga")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        user = store.current_user or {}
        stats = store.warga_stats(user.get("id"))

        welcome = tk.Label(self.shell.content,
                            text=f"Selamat datang, {user.get('name', '-')}!",
                            font=("Segoe UI", 13, "bold"), bg="#f1f5f9", fg="#1e293b")
        welcome.pack(anchor="w", pady=(0, 12))

        grid = tk.Frame(self.shell.content, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(2):
            grid.grid_columnconfigure(i, weight=1)

        cards = [
            ("Laporan Saya", stats["total_reports"], "#2563eb", "🦠"),
            ("Anak Terdaftar", stats["total_children"], "#16a34a", "🧒"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            r, c = divmod(idx, 2)
            card = stat_card(grid, title, value, color, icon)
            card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

        list_frame = tk.Frame(self.shell.content, bg="white", highlightbackground="#e2e8f0",
                               highlightthickness=1)
        list_frame.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(list_frame, text="Laporan Penyakit Terbaru Saya", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=18, pady=(14, 8))

        if not stats["recent_reports"]:
            tk.Label(list_frame, text="Anda belum membuat laporan penyakit.", bg="white",
                      fg="#94a3b8", font=("Segoe UI", 9)).pack(padx=18, pady=(0, 14))
        else:
            for rep in stats["recent_reports"]:
                row = tk.Frame(list_frame, bg="white")
                row.pack(fill="x", padx=18, pady=4)
                tk.Label(row, text=f"• {rep.get('disease_name', '-')}", bg="white",
                         font=("Segoe UI", 9), fg="#334155", anchor="w").pack(side="left")
                tk.Label(row, text=rep.get("status", "-"), bg="white", font=("Segoe UI", 8),
                         fg="#94a3b8").pack(side="right")
            tk.Frame(list_frame, bg="white", height=10).pack()

    def on_show(self):
        self._render()