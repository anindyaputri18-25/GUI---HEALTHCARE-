import tkinter as tk

from data.store import store
from pages.sidebar import AppShell

SEVERITY_COLOR = {"ringan": "#16a34a", "sedang": "#ea580c", "berat": "#dc2626"}

class KesehatanMapPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="kesehatan_map", title="Peta Sebaran Kasus Penyakit")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _cases(self):
        return [r for r in store.disease_reports
                if r["status"] == "verified" and r.get("latitude") and r.get("longitude")]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        cases = self._cases()

        main = tk.Frame(self.shell.content, bg="#f1f5f9")
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=2)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        map_frame = tk.Frame(main, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        map_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(map_frame, text="Visualisasi Titik Kasus Terverifikasi", font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=14, pady=(12, 6))

        canvas = tk.Canvas(map_frame, bg="#e0f2fe", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        if cases:
            lats = [c["latitude"] for c in cases]
            lons = [c["longitude"] for c in cases]
            min_lat, max_lat = min(lats), max(lats)
            min_lon, max_lon = min(lons), max(lons)
            pad = 0.001

            def to_xy(lat, lon, w, h):
                x = ((lon - min_lon + pad) / (max_lon - min_lon + 2 * pad)) * (w - 60) + 30
                y = h - (((lat - min_lat + pad) / (max_lat - min_lat + 2 * pad)) * (h - 60) + 30)
                return x, y

            def draw_points(event=None):
                canvas.delete("all")
                w = canvas.winfo_width() or 600
                h = canvas.winfo_height() or 400
                for c in cases:
                    x, y = to_xy(c["latitude"], c["longitude"], w, h)
                    color = SEVERITY_COLOR.get(c["severity"], "#2563eb")
                    canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill=color, outline="white", width=2)
                    canvas.create_text(x, y - 14, text=c["patient_name"], font=("Segoe UI", 7), fill="#1e293b")

            canvas.bind("<Configure>", draw_points)
        else:
            tk.Label(canvas, text="Belum ada kasus terverifikasi dengan koordinat.",
                     bg="#e0f2fe", fg="#64748b").pack(pady=160)

        legend = tk.Frame(map_frame, bg="white")
        legend.pack(anchor="w", padx=14, pady=(0, 10))
        for sev, color in SEVERITY_COLOR.items():
            tk.Label(legend, text=f"● {sev.capitalize()}", fg=color, bg="white",
                     font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 14))

        # ---------------- DAFTAR KASUS ----------------
        list_frame = tk.Frame(main, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        list_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(list_frame, text="Daftar Kasus Terverifikasi", font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#1e293b").pack(anchor="w", padx=14, pady=(12, 6))

        if not cases:
            tk.Label(list_frame, text="Tidak ada data.", bg="white", fg="#94a3b8").pack(padx=14, pady=10)
        else:
            for c in cases:
                disease_name = store.lookup_name(store.disease_types, c["disease_type_id"])
                village_name = store.lookup_name(store.villages, c["village_id"])
                row = tk.Frame(list_frame, bg="white", highlightbackground="#f1f5f9", highlightthickness=1)
                row.pack(fill="x", padx=14, pady=4)
                color = SEVERITY_COLOR.get(c["severity"], "#2563eb")
                tk.Label(row, text=f"● {c['patient_name']}", fg=color, bg="white",
                         font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=6, pady=(4, 0))
                tk.Label(row, text=f"{disease_name} — {village_name}", bg="white", fg="#64748b",
                         font=("Segoe UI", 8)).pack(anchor="w", padx=6, pady=(0, 4))

    def on_show(self):
        self._render()