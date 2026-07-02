import tkinter as tk
from tkinter import messagebox

from data.store import store

SIDEBAR_BG = "#1e293b"
SIDEBAR_HOVER = "#334155"
SIDEBAR_ACTIVE = "#2563eb"
SIDEBAR_FG = "#e2e8f0"

MENUS = {
    "admin": [
        ("Dashboard", "dashboard", "🏠"),
        ("Kelola User", "admin_users", "👤"),
        ("Kelola Wilayah", "admin_villages", "📍"),
        ("Kelola Penyakit", "admin_disease_types", "🦠"),
        ("Approval Restock", "admin_restock", "📋"),
        ("Log Aktivitas", "admin_logs", "🕒"),
        ("__section__", "APOTEK"),
        ("Stok Obat", "apotek_medicines", "💊"),
        ("Transaksi Obat", "apotek_transactions", "🧾"),
        ("Laporan Stok", "apotek_reports", "📄"),
        ("__section__", "PELAPORAN PENYAKIT"),
        ("Kasus Penyakit", "kesehatan_reports", "🦠"),
        ("Peta Sebaran", "kesehatan_map", "📍"),
        ("__section__", "MEDIS"),
        ("Rekomendasi Dokter", "dokter_consultations", "⚕️"),
        ("__section__", "IMUNISASI"),
        ("Data Anak", "imunisasi_children", "👶"),
        ("Jadwal & Catat", "imunisasi_schedules", "🗓️"),
        ("Reminder Imunisasi", "imunisasi_reminders", "🔔"),
        ("__section__", "LAPORAN EKSEKUTIF"),
        ("Cetak Laporan", "kepala_reports", "🖨️"),
    ],
    "apoteker": [
        ("Dashboard", "dashboard", "🏠"),
        ("Stok Obat", "apotek_medicines", "💊"),
        ("Transaksi Obat", "apotek_transactions", "🧾"),
        ("Pengajuan Restock", "apotek_restock", "📦"),
        ("Laporan Stok", "apotek_reports", "📄"),
    ],
    "petugas_medis": [
        ("Dashboard", "dashboard", "🏠"),
        ("Kasus Penyakit", "kesehatan_reports", "🦠"),
        ("Verifikasi Laporan", "kesehatan_verification", "✅"),
        ("Peta Sebaran", "kesehatan_map", "📍"),
        ("Rekomendasi Dokter", "dokter_consultations", "⚕️"),
        ("Data Anak", "imunisasi_children", "👶"),
        ("Jadwal & Catat", "imunisasi_schedules", "🗓️"),
        ("Reminder Imunisasi", "imunisasi_reminders", "🔔"),
    ],
    "warga": [
        ("Dashboard", "dashboard", "🏠"),
        ("Lapor Penyakit", "warga_reports", "🦠"),
        ("Data Anak Saya", "warga_children", "👶"),
    ],
}

ROLE_LABELS = {
    "admin": "Administrator",
    "apoteker": "Apoteker",
    "petugas_medis": "Petugas Medis",
    "warga": "Warga",
}

class AppShell(tk.Frame):
    def __init__(self, parent, app, active_key, title):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.active_key = active_key

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main(title)

    def _build_sidebar(self):
        sidebar_container = tk.Frame(self, bg=SIDEBAR_BG, width=230)
        sidebar_container.grid(row=0, column=0, sticky="ns")
        sidebar_container.grid_propagate(False)
        sidebar_container.grid_rowconfigure(1, weight=1)
        sidebar_container.grid_columnconfigure(0, weight=1)

        # ---- Header logo ----
        tk.Label(sidebar_container, text="💚 HealthCare", font=("Segoe UI", 13, "bold"),
                 bg=SIDEBAR_BG, fg="white", pady=20).grid(row=0, column=0, columnspan=2, sticky="ew")

        # ---- Area menu yang bisa di-scroll ----
        canvas = tk.Canvas(sidebar_container, bg=SIDEBAR_BG, highlightthickness=0, bd=0)
        canvas.grid(row=1, column=0, sticky="nsew")

        vsb = tk.Scrollbar(sidebar_container, orient="vertical", command=canvas.yview,
                            width=10, troughcolor=SIDEBAR_BG, bg=SIDEBAR_HOVER,
                            activebackground=SIDEBAR_HOVER, bd=0, highlightthickness=0)
        vsb.grid(row=1, column=1, sticky="ns")
        canvas.configure(yscrollcommand=vsb.set)

        menu_frame = tk.Frame(canvas, bg=SIDEBAR_BG)
        menu_window = canvas.create_window((0, 0), window=menu_frame, anchor="nw")

        def _on_menu_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            canvas.itemconfig(menu_window, width=event.width)

        menu_frame.bind("<Configure>", _on_menu_configure)
        canvas.bind("<Configure>", _on_canvas_configure)

        # Scroll dengan mouse wheel 
        def _on_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            canvas.yview_scroll(-1 * int(delta / 120) if abs(delta) >= 120 else (-1 if delta > 0 else 1), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)

        user = store.current_user or {}
        role = user.get("role", "")
        menu_items = MENUS.get(role, [])

        for entry in menu_items:
            if entry[0] == "__section__":
                tk.Label(menu_frame, text=entry[1], font=("Segoe UI", 8, "bold"),
                         bg=SIDEBAR_BG, fg="#64748b", anchor="w", padx=20).pack(fill="x", pady=(14, 4))
            else:
                label, key, icon = entry
                self._menu_button(menu_frame, label, key, icon)

        # ---- Tombol Keluar ----
        logout_btn = tk.Label(sidebar_container, text="🚪  Keluar", font=("Segoe UI", 10),
                               bg=SIDEBAR_BG, fg="#fca5a5", anchor="w", padx=20, pady=12,
                               cursor="hand2")
        logout_btn.grid(row=2, column=0, columnspan=2, sticky="ew")
        logout_btn.bind("<Button-1>", lambda e: self._logout())
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg=SIDEBAR_HOVER))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg=SIDEBAR_BG))

    def _menu_button(self, parent, label, key, icon):
        is_active = key == self.active_key
        bg = SIDEBAR_ACTIVE if is_active else SIDEBAR_BG
        lbl = tk.Label(parent, text=f"{icon}  {label}", font=("Segoe UI", 10),
                        bg=bg, fg="white", anchor="w", padx=20, pady=12, cursor="hand2")
        lbl.pack(fill="x")
        lbl.bind("<Button-1>", lambda e, k=key: self.app.show_page(k))
        if not is_active:
            lbl.bind("<Enter>", lambda e: lbl.config(bg=SIDEBAR_HOVER))
            lbl.bind("<Leave>", lambda e: lbl.config(bg=SIDEBAR_BG))

    def _build_main(self, title):
        main = tk.Frame(self, bg="#f1f5f9")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        topbar = tk.Frame(main, bg="white", height=60, highlightbackground="#e2e8f0",
                           highlightthickness=1)
        topbar.grid(row=0, column=0, sticky="ew")
        tk.Label(topbar, text=title, font=("Segoe UI", 13, "bold"), bg="white",
                 fg="#1e293b").pack(side="left", padx=24, pady=14)

        user = store.current_user or {}
        user_text = f"{user.get('name', '-')}  ({ROLE_LABELS.get(user.get('role'), '-')})"

        tk.Label(topbar, text=user_text, font=("Segoe UI", 9), bg="white",
                 fg="#64748b").pack(side="right", padx=24)

        # content: frame kosong yang akan diisi oleh halaman pemanggil
        self.content = tk.Frame(main, bg="#f1f5f9")
        self.content.grid(row=1, column=0, sticky="nsew", padx=24, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    def _logout(self):
        if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar?"):
            if store.current_user:
                store.log("logout", "User logged out.", store.current_user["id"])
            store.current_user = None
            self.app.show_page("landing")


def stat_card(parent, title, value, color="#2563eb", icon="📊"):
    card = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0",
                     highlightthickness=1)
    inner = tk.Frame(card, bg="white")
    inner.pack(fill="both", expand=True, padx=18, pady=16)

    top = tk.Frame(inner, bg="white")
    top.pack(fill="x")
    tk.Label(top, text=icon, font=("Segoe UI Emoji", 18), bg="white").pack(side="left")
    tk.Label(inner, text=str(value), font=("Segoe UI", 22, "bold"), bg="white",
             fg=color).pack(anchor="w", pady=(8, 0))
    tk.Label(inner, text=title, font=("Segoe UI", 9), bg="white",
             fg="#64748b").pack(anchor="w")
    return card