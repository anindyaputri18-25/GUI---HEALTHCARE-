import tkinter as tk
from datetime import date

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_error, show_success

SEVERITY_OPTIONS = [("ringan", "Ringan"), ("sedang", "Sedang"), ("berat", "Berat")]
GENDER_OPTIONS = [("L", "Laki-laki"), ("P", "Perempuan")]
STATUS_LABEL = {"pending": "Pending", "verified": "Terverifikasi", "rejected": "Ditolak"}

class KesehatanReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="kesehatan_reports", title="Laporan Kasus Penyakit")
        self.shell.pack(fill="both", expand=True)
        self.filter_status = ""
        self._render()

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
            {"key": "symptoms", "label": "Gejala", "type": "textarea"},
            {"key": "severity", "label": "Tingkat Keparahan", "type": "radio", "options": SEVERITY_OPTIONS},
            {"key": "report_date", "label": "Tanggal Lapor", "type": "date", "default": date.today().isoformat()},
            {"key": "village_id", "label": "Desa", "type": "combobox", "options": village_opts},
            {"key": "latitude", "label": "Latitude", "type": "float", "required": False},
            {"key": "longitude", "label": "Longitude", "type": "float", "required": False},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        for label, val in [("Semua", ""), ("Pending", "pending"), ("Terverifikasi", "verified"), ("Ditolak", "rejected")]:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_status == val else "#e2e8f0",
                      fg="white" if self.filter_status == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)
        tk.Button(filter_bar, text="+ Lapor Kasus Baru", font=("Segoe UI", 9, "bold"), bg="#0d9488",
                  fg="white", relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._open_add).pack(side="right")

        columns = [("patient_name", "Pasien", 140), ("disease", "Penyakit", 130), ("severity", "Keparahan", 80),
                   ("village", "Desa", 110), ("report_date", "Tgl Lapor", 95), ("status", "Status", 100)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        self.tree.tag_configure("pending", foreground="#ea580c")
        self.tree.tag_configure("verified", foreground="#16a34a")
        self.tree.tag_configure("rejected", foreground="#dc2626")

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="✅ Verifikasi", command=lambda: self._process("verify"), bg="#16a34a",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="❌ Tolak", command=lambda: self._process("reject"), bg="#dc2626",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))
        tk.Button(action_bar, text="Hapus Terpilih", command=self._delete_selected, bg="#64748b",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))

        self._reload_table()

    def _set_filter(self, val):
        self.filter_status = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(store.disease_reports):
            if self.filter_status and r["status"] != self.filter_status:
                continue
            disease_name = store.lookup_name(store.disease_types, r["disease_type_id"])
            village_name = store.lookup_name(store.villages, r["village_id"])
            self.tree.insert("", "end", iid=r["id"], tags=(r["status"],), values=(
                r["patient_name"], disease_name, r["severity"].capitalize(), village_name,
                r["report_date"], STATUS_LABEL.get(r["status"], r["status"])))

    def _open_add(self):
        if not store.disease_types or not store.villages:
            show_error(self, "Tambahkan minimal 1 Jenis Penyakit dan 1 Wilayah/Desa terlebih dahulu.")
            return
        FormDialog(self, "Laporkan Kasus Penyakit", self._fields(), on_submit=self._save_new, width=480)

    def _save_new(self, data):
        role = store.current_user["role"] if store.current_user else "warga"
        store.add_disease_report(data, role)
        show_success(self, "Laporan penyakit berhasil disimpan.")
        self._reload_table()

    def _process(self, action):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih laporan terlebih dahulu.")
            return
        rid = int(sel[0])

        def _confirm_with_notes(notes):
            try:
                store.process_verification(rid, action, notes["notes"])
                show_success(self, "Laporan berhasil diverifikasi." if action == "verify" else "Laporan ditolak.")
            except ValueError as e:
                show_error(self, str(e))
            self._reload_table()

        FormDialog(self, "Catatan Verifikasi", [
            {"key": "notes", "label": "Catatan Verifikasi", "type": "textarea"}
        ], on_submit=_confirm_with_notes, width=420)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih laporan terlebih dahulu.")
            return
        if confirm_delete(self):
            store.delete_disease_report(int(sel[0]))
            show_success(self, "Laporan penyakit berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()