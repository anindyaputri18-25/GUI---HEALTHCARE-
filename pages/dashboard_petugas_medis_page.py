import tkinter as tk

from data.store import store
from pages.sidebar import AppShell, stat_card


class DashboardPetugasMedisPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="dashboard",
                               title="Dashboard Petugas Medis")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        stats = store.petugas_medis_stats()
        grid = tk.Frame(self.shell.content, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        cards = [
            ("Total Laporan", stats["total_reports"], "#2563eb", "🦠"),
            ("Pending Verifikasi", stats["pending_reports"], "#ea580c", "⏳"),
            ("Terverifikasi", stats["verified_reports"], "#16a34a", "✅"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            r, c = divmod(idx, 3)
            card = stat_card(grid, title, value, color, icon)
            card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

        sev = stats["severity_stats"]
        sev_frame = tk.Frame(self.shell.content, bg="white", highlightbackground="#e2e8f0",
                              highlightthickness=1)
        sev_frame.pack(fill="x", pady=(16, 0))
        tk.Label(sev_frame, text="Statistik Tingkat Keparahan (Bulan ini)",
                 font=("Segoe UI", 11, "bold"), bg="white", fg="#1e293b").pack(
            anchor="w", padx=18, pady=(14, 8))
        sev_row = tk.Frame(sev_frame, bg="white")
        sev_row.pack(fill="x", padx=18, pady=(0, 14))
        for label, color in [("ringan", "#16a34a"), ("sedang", "#ea580c"), ("berat", "#dc2626")]:
            tk.Label(sev_row, text=f"{label.capitalize()}: {sev[label]}",
                     font=("Segoe UI", 9, "bold"), fg=color, bg="white").pack(
                side="left", padx=(0, 24))

        list_frame = tk.Frame(self.shell.content, bg="white", highlightbackground="#e2e8f0",
                               highlightthickness=1)
        list_frame.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(list_frame, text="Laporan Penyakit Terbaru", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=18, pady=(14, 8))

        if not stats["recent_reports"]:
            tk.Label(list_frame, text="Belum ada laporan penyakit.", bg="white",
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