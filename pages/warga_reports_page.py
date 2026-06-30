import tkinter as tk
from datetime import date

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, FormDialog, confirm_delete, show_error, show_success

SEVERITY_OPTIONS = [("ringan", "Ringan"), ("sedang", "Sedang"), ("berat", "Berat")]
GENDER_OPTIONS = [("L", "Laki-laki"), ("P", "Perempuan")]
STATUS_LABEL = {"pending": "Menunggu Verifikasi", "verified": "Terverifikasi", "rejected": "Ditolak"}
STATUS_COLOR = {"pending": "#ea580c", "verified": "#16a34a", "rejected": "#dc2626"}

class WargaReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="warga_reports", title="Laporan Penyakit Saya")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _my_reports(self):
        uid = store.current_user["id"]
        return [r for r in store.disease_reports if r["reporter_id"] == uid]

    def _fields(self):
        disease_opts = [(d["id"], d["name"]) for d in store.disease_types]
        village_opts = [(v["id"], v["name"]) for v in store.villages]
        return [
            {"key": "patient_name", "label": "Nama Pasien"},
            {"key": "patient_nik", "label": "NIK Pasien (16 digit)"},
            {"key": "patient_age", "label": "Usia", "type": "number"},
            {"key": "patient_gender", "label": "Jenis Kelamin", "type": "radio", "options": GENDER_OPTIONS},
            {"key": "patient_address", "label": "Alamat Pasien", "type": "textarea"},
            {"key": "disease_type_id", "label": "Jenis Penyakit", "type": "combobox", "options": disease_opts},
            {"key": "symptoms", "label": "Gejala yang Dirasakan", "type": "textarea"},
            {"key": "severity", "label": "Tingkat Keparahan", "type": "radio", "options": SEVERITY_OPTIONS},
            {"key": "report_date", "label": "Tanggal Lapor", "type": "date", "default": date.today().isoformat()},
            {"key": "village_id", "label": "Desa", "type": "combobox", "options": village_opts},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        top_bar.pack(fill="x", pady=(0, 10))
        tk.Label(top_bar, text="Daftar laporan penyakit yang pernah Anda buat.", bg="#f1f5f9",
                 fg="#64748b", font=("Segoe UI", 9)).pack(side="left")
        tk.Button(top_bar, text="+ Lapor Penyakit Baru", font=("Segoe UI", 9, "bold"), bg="#0d9488",
                  fg="white", relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._open_add).pack(side="right")

        columns = [("patient_name", "Pasien", 150), ("disease", "Penyakit", 150), ("severity", "Keparahan", 90),
                   ("report_date", "Tgl Lapor", 100), ("status", "Status", 150)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        for s, c in STATUS_COLOR.items():
            self.tree.tag_configure(s, foreground=c)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="Lihat Detail / Hasil Verifikasi", command=self._view_detail, bg="#2563eb",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="Hapus Laporan (jika belum diverifikasi)", command=self._delete_selected,
                  bg="#dc2626", fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))

        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(self._my_reports()):
            disease_name = store.lookup_name(store.disease_types, r["disease_type_id"])
            self.tree.insert("", "end", iid=r["id"], tags=(r["status"],), values=(
                r["patient_name"], disease_name, r["severity"].capitalize(), r["report_date"],
                STATUS_LABEL.get(r["status"], r["status"])))

    def _open_add(self):
        if not store.disease_types or not store.villages:
            show_error(self, "Data jenis penyakit/desa belum tersedia. Hubungi admin.")
            return
        FormDialog(self, "Lapor Penyakit Baru", self._fields(), on_submit=self._save_new, width=480)

    def _save_new(self, data):
        store.add_disease_report(data, "warga")
        show_success(self, "Laporan berhasil dikirim dan menunggu verifikasi petugas medis.")
        self._reload_table()

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih laporan terlebih dahulu.")
            return None
        rid = int(sel[0])
        return next(r for r in store.disease_reports if r["id"] == rid)

    def _view_detail(self):
        r = self._selected()
        if r is None:
            return
        disease_name = store.lookup_name(store.disease_types, r["disease_type_id"])
        msg = (
            f"Pasien: {r['patient_name']}\nPenyakit: {disease_name}\nGejala: {r['symptoms']}\n"
            f"Status: {STATUS_LABEL.get(r['status'])}\n"
            f"Catatan Verifikasi: {r.get('verification_notes') or '-'}\n"
            f"Rekomendasi Penanganan: {r.get('treatment_recommendation') or 'Belum ada'}"
        )
        tk.messagebox.showinfo(f"Detail Laporan #{r['id']}", msg)

    def _delete_selected(self):
        r = self._selected()
        if r is None:
            return
        if r["status"] != "pending":
            show_error(self, "Laporan yang sudah diverifikasi/ditolak tidak dapat dihapus.")
            return
        if confirm_delete(self):
            store.delete_disease_report(r["id"])
            show_success(self, "Laporan berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()