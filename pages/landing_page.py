import tkinter as tk

BG_DARK = "#0b1220"
CARD_BG = "#141d2e"
ACCENT = "#2dd4bf"
TEXT_MUTED = "#94a3b8"

class LandingPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self._build_topbar()
        self._build_hero()
        self._build_feature_cards()

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=BG_DARK, height=70)
        topbar.pack(fill="x", padx=40, pady=(20, 0))

        logo_frame = tk.Frame(topbar, bg=BG_DARK)
        logo_frame.pack(side="left")
        tk.Label(logo_frame, text="💚", font=("Segoe UI Emoji", 16), bg=BG_DARK).pack(side="left")
        tk.Label(logo_frame, text=" HealthCare", font=("Segoe UI", 14, "bold"),
                 bg=BG_DARK, fg="white").pack(side="left")

        btn_frame = tk.Frame(topbar, bg=BG_DARK)
        btn_frame.pack(side="right")

        btn_register = tk.Button(btn_frame, text="Registrasi Warga", font=("Segoe UI", 9, "bold"),
                                  bg=ACCENT, fg="#022c22", relief="flat", padx=18, pady=8,
                                  cursor="hand2", command=lambda: self.app.show_page("register"))
        btn_register.pack(side="right")

        btn_login = tk.Button(btn_frame, text="Masuk", font=("Segoe UI", 9, "bold"),
                               bg=BG_DARK, fg="white", relief="flat", padx=18, pady=8,
                               highlightbackground="#334155", highlightthickness=1,
                               cursor="hand2", command=lambda: self.app.show_page("login"))
        btn_login.pack(side="right", padx=(0, 12))

    def _build_hero(self):
        hero = tk.Frame(self, bg=BG_DARK)
        hero.pack(fill="x", pady=(50, 30))

        badge = tk.Label(hero, text="LAYANAN KESEHATAN DIGITAL", font=("Segoe UI", 8, "bold"),
                          bg="#0f2e2a", fg=ACCENT, padx=14, pady=6)
        badge.pack()

        title1 = tk.Label(hero, text="Solusi Terintegrasi untuk", font=("Segoe UI", 26, "bold"),
                           bg=BG_DARK, fg="white")
        title1.pack(pady=(18, 0))
        title2 = tk.Label(hero, text="Puskesmas & Warga", font=("Segoe UI", 26, "bold"),
                           bg=BG_DARK, fg=ACCENT)
        title2.pack()

        desc = tk.Label(
            hero,
            text=("Membantu pengelolaan ketersediaan obat, pelaporan cepat persebaran wabah\n"
                  "penyakit, serta pengingat jadwal imunisasi anak secara otomatis."),
            font=("Segoe UI", 10), bg=BG_DARK, fg=TEXT_MUTED, justify="center",
        )
        desc.pack(pady=(16, 0))

    def _build_feature_cards(self):
        wrapper = tk.Frame(self, bg=BG_DARK)
        wrapper.pack(pady=(10, 40))

        features = [
            ("💊", "Monitoring Obat",
             "Mengelola ketersediaan stok obat secara real-time,\nmendeteksi obat kadaluarsa, serta mengirimkan\nnotifikasi restock otomatis."),
            ("🦠", "Laporan Kasus Penyakit",
             "Pemantauan dini persebaran penyakit berbasis\nwilayah secara real-time untuk mempercepat\nverifikasi kasus medis."),
            ("🔔", "Reminder Imunisasi",
             "Jadwal imunisasi berkala yang teratur dengan\nsistem reminder dashboard dan email untuk\nmencegah kelalaian imunisasi anak."),
        ]

        for icon, title, desc in features:
            card = tk.Frame(wrapper, bg=CARD_BG, highlightbackground="#1e293b",
                             highlightthickness=1, width=330, height=260)
            card.pack(side="left", padx=12)
            card.pack_propagate(False)

            icon_box = tk.Label(card, text=icon, font=("Segoe UI Emoji", 18), bg="#0f2e2a",
                                 fg=ACCENT, width=3, height=1)
            icon_box.pack(anchor="w", padx=24, pady=(24, 12))

            tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=CARD_BG,
                     fg="white", anchor="w", justify="left").pack(anchor="w", padx=24)

            tk.Label(card, text=desc, font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_MUTED,
                     anchor="w", justify="left").pack(anchor="w", padx=24, pady=(10, 0))

    def on_show(self):
        pass