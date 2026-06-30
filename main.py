import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.dashboard_admin_page import DashboardAdminPage
from pages.dashboard_apoteker_page import DashboardApotekerPage
from pages.dashboard_petugas_medis_page import DashboardPetugasMedisPage
from pages.dashboard_warga_page import DashboardWargaPage

from pages.admin_users_page import AdminUsersPage
from pages.admin_villages_page import AdminVillagesPage
from pages.admin_disease_types_page import AdminDiseaseTypesPage
from pages.admin_restock_page import AdminRestockPage
from pages.admin_logs_page import AdminLogsPage

from pages.apotek_medicines_page import ApotekMedicinesPage
from pages.apotek_transactions_page import ApotekTransactionsPage
from pages.apotek_restock_page import ApotekRestockPage
from pages.apotek_reports_page import ApotekReportsPage

from pages.kesehatan_reports_page import KesehatanReportsPage
from pages.kesehatan_verification_page import KesehatanVerificationPage
from pages.kesehatan_map_page import KesehatanMapPage
from pages.dokter_consultations_page import DokterConsultationsPage

from pages.imunisasi_children_page import ImunisasiChildrenPage
from pages.imunisasi_schedules_page import ImunisasiSchedulesPage
from pages.imunisasi_reminders_page import ImunisasiRemindersPage

from pages.kepala_reports_page import KepalaReportsPage

from pages.warga_reports_page import WargaReportsPage
from pages.warga_children_page import WargaChildrenPage


WINDOW_TITLE = "HealthCare - Desktop App"
WINDOW_SIZE = "1200x720"


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(1000, 650)
        self.configure(bg="#f1f5f9")

        self.container = tk.Frame(self, bg="#f1f5f9")
        self.container.pack(fill="both", expand=True)

        self._page_classes = {
            "landing": LandingPage,
            "login": LoginPage,
            "register": RegisterPage,
            "dashboard_admin": DashboardAdminPage,
            "dashboard_apoteker": DashboardApotekerPage,
            "dashboard_petugas_medis": DashboardPetugasMedisPage,
            "dashboard_warga": DashboardWargaPage,

            "admin_users": AdminUsersPage,
            "admin_villages": AdminVillagesPage,
            "admin_disease_types": AdminDiseaseTypesPage,
            "admin_restock": AdminRestockPage,
            "admin_logs": AdminLogsPage,

            "apotek_medicines": ApotekMedicinesPage,
            "apotek_transactions": ApotekTransactionsPage,
            "apotek_restock": ApotekRestockPage,
            "apotek_reports": ApotekReportsPage,

            "kesehatan_reports": KesehatanReportsPage,
            "kesehatan_verification": KesehatanVerificationPage,
            "kesehatan_map": KesehatanMapPage,
            "dokter_consultations": DokterConsultationsPage,

            "imunisasi_children": ImunisasiChildrenPage,
            "imunisasi_schedules": ImunisasiSchedulesPage,
            "imunisasi_reminders": ImunisasiRemindersPage,

            "kepala_reports": KepalaReportsPage,

            "warga_reports": WargaReportsPage,
            "warga_children": WargaChildrenPage,
        }

        self._current_page = None
        self.show_page("landing")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def show_page(self, key):
        if key == "dashboard":
            self.go_to_dashboard()
            return

        protected_pages = {
            "dashboard_admin", "dashboard_apoteker",
            "dashboard_petugas_medis", "dashboard_warga",
        }

        if key not in ("landing", "login", "register") and store.current_user is None:
            messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
            key = "login"

        page_class = self._page_classes.get(key)

        if self._current_page is not None:
            self._current_page.destroy()

        if page_class is None:
            self._current_page = self._build_placeholder(key)
        else:
            self._current_page = page_class(self.container, self)

        self._current_page.pack(fill="both", expand=True)

        if hasattr(self._current_page, "on_show"):
            self._current_page.on_show()

    def _build_placeholder(self, key):
        frame = tk.Frame(self.container, bg="#f1f5f9")
        tk.Label(frame, text="🚧", font=("Segoe UI Emoji", 40), bg="#f1f5f9").pack(
            pady=(120, 10))
        tk.Label(frame, text=f"Modul '{key}' segera hadir",
                 font=("Segoe UI", 14, "bold"), bg="#f1f5f9", fg="#334155").pack()
        tk.Label(frame, text="Halaman ini akan ditambahkan pada tahap pengembangan berikutnya.",
                 font=("Segoe UI", 9), bg="#f1f5f9", fg="#64748b").pack(pady=(6, 20))
        btn = tk.Button(frame, text="Kembali ke Dashboard", font=("Segoe UI", 9, "bold"),
                         bg="#2563eb", fg="white", relief="flat", padx=16, pady=8,
                         cursor="hand2", command=self.go_to_dashboard)
        btn.pack()
        return frame

    def go_to_dashboard(self):
        user = store.current_user
        if user is None:
            self.show_page("login")
            return

        role_to_page = {
            "admin": "dashboard_admin",
            "apoteker": "dashboard_apoteker",
            "petugas_medis": "dashboard_petugas_medis",
            "warga": "dashboard_warga",
        }
        page_key = role_to_page.get(user["role"])
        if page_key is None:
            messagebox.showerror("Error", "Role tidak dikenali.")
            store.current_user = None
            self.show_page("login")
            return

        self.show_page(page_key)

    def _on_close(self):
        if messagebox.askokcancel("Keluar", "Tutup aplikasi?"):
            self.destroy()

def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()