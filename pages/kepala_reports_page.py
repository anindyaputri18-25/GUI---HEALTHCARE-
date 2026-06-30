import tkinter as tk
from datetime import date

from data.store import store
from pages.sidebar import AppShell, stat_card
from pages.widgets import show_success

class KepalaReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="kepala_reports", title="Laporan Eksekutif")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        today = date.today().isoformat()
        canvas_outer = tk.Frame(self.shell.content, bg="#f1f5f9")
        canvas_outer.pack(fill="both", expand=True)

        tk.Label(canvas_outer, text=f"Ringkasan Data Posyandu Desa per {today}",
                 font=("Segoe UI", 11, "bold"), bg="#f1f5f9", fg="#1e293b").pack(anchor="w", pady=(0, 10))

        grid = tk.Frame(canvas_outer, bg="#f1f5f9")
        grid.pack(fill="x")
        for i in range(4):
            grid.grid_columnconfigure(i, weight=1)

        verified_reports = sum(1 for r in store.disease_reports if r["status"] == "verified")
        completed_immun = sum(1 for r in store.immunization_records if r["status"] == "completed")
        low_stock = sum(1 for m in store.medicines if m["stock"] <= m["min_stock"])

        cards = [
            ("Total Warga Terdaftar", sum(1 for u in store.users if u["role"] == "warga"), "#2563eb", "👤"),
            ("Total Kasus Terverifikasi", verified_reports, "#16a34a", "🦠"),
            ("Total Anak Imunisasi Lengkap", completed_immun, "#0891b2", "👶"),
            ("Obat dengan Stok Menipis", low_stock, "#dc2626", "💊"),
        ]
        for idx, (title, value, color, icon) in enumerate(cards):
            c = stat_card(grid, title, value, color, icon)
            c.grid(row=0, column=idx, sticky="nsew", padx=8, pady=8)

        # Ringkasan per desa
        village_frame = tk.Frame(canvas_outer, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        village_frame.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(village_frame, text="Ringkasan Kasus Penyakit per Desa", font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=16, pady=(14, 8))

        if not store.villages:
            tk.Label(village_frame, text="Belum ada data desa.", bg="white", fg="#94a3b8").pack(padx=16, pady=10)
        else:
            for v in store.villages:
                count = sum(1 for r in store.disease_reports if r["village_id"] == v["id"])
                row = tk.Frame(village_frame, bg="white")
                row.pack(fill="x", padx=16, pady=4)
                tk.Label(row, text=f"• {v['name']} ({v['kecamatan']})", bg="white", fg="#334155",
                         font=("Segoe UI", 9)).pack(side="left")
                tk.Label(row, text=f"{count} kasus", bg="white", fg="#64748b",
                         font=("Segoe UI", 9, "bold")).pack(side="right")
            tk.Frame(village_frame, bg="white", height=8).pack()

        tk.Button(canvas_outer, text="🖨️ Cetak / Ekspor Laporan (.txt)", font=("Segoe UI", 9, "bold"),
                  bg="#0d9488", fg="white", relief="flat", padx=16, pady=10, cursor="hand2",
                  command=self._export_report).pack(anchor="w", pady=(16, 0))

    def _export_report(self):
        import os
        today = date.today().isoformat()
        lines = [f"LAPORAN EKSEKUTIF HEALTHCARE - {today}", "=" * 50, ""]
        lines.append(f"Total Warga Terdaftar     : {sum(1 for u in store.users if u['role'] == 'warga')}")
        lines.append(f"Total Kasus Terverifikasi : {sum(1 for r in store.disease_reports if r['status'] == 'verified')}")
        lines.append(f"Total Imunisasi Lengkap   : {sum(1 for r in store.immunization_records if r['status'] == 'completed')}")
        lines.append(f"Obat Stok Menipis         : {sum(1 for m in store.medicines if m['stock'] <= m['min_stock'])}")
        lines.append("")
        lines.append("Rincian Kasus per Desa:")
        for v in store.villages:
            count = sum(1 for r in store.disease_reports if r["village_id"] == v["id"])
            lines.append(f"  - {v['name']} ({v['kecamatan']}): {count} kasus")

        out_dir = os.path.join(os.path.expanduser("~"), "Documents")
        if not os.path.isdir(out_dir):
            out_dir = os.path.expanduser("~")
        out_path = os.path.join(out_dir, f"laporan_healthcare_{today}.txt")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            store.log("export_report", f"Mengekspor laporan eksekutif ke {out_path}", store.current_user["id"])
            show_success(self, f"Laporan berhasil diekspor ke:\n{out_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Gagal mengekspor laporan: {e}")

    def on_show(self):
        self._render()