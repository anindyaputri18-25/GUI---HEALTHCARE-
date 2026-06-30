import tkinter as tk

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, FormDialog, show_error, show_success

class DokterConsultationsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="dokter_consultations", title="Rekomendasi Penanganan Dokter")
        self.shell.pack(fill="both", expand=True)
        self.filter_mode = ""
        self._render()

    def _verified_reports(self):
        reports = [r for r in store.disease_reports if r["status"] == "verified"]
        if self.filter_mode == "pending_treatment":
            reports = [r for r in reports if not r.get("treatment_recommendation")]
        elif self.filter_mode == "treated":
            reports = [r for r in reports if r.get("treatment_recommendation")]
        return reports

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        for label, val in [("Semua Terverifikasi", ""), ("Belum Ditangani", "pending_treatment"),
                            ("Sudah Ditangani", "treated")]:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_mode == val else "#e2e8f0",
                      fg="white" if self.filter_mode == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)

        columns = [("patient_name", "Pasien", 140), ("disease", "Penyakit", 140), ("symptoms", "Gejala", 220),
                   ("severity", "Keparahan", 80), ("treatment", "Rekomendasi", 220)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="💊 Beri Rekomendasi Penanganan", command=self._open_recommend,
                  bg="#0d9488", fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")

        self._reload_table()

    def _set_filter(self, val):
        self.filter_mode = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(self._verified_reports()):
            disease_name = store.lookup_name(store.disease_types, r["disease_type_id"])
            self.tree.insert("", "end", iid=r["id"], values=(
                r["patient_name"], disease_name, r["symptoms"][:60], r["severity"].capitalize(),
                (r.get("treatment_recommendation") or "Belum diberikan")[:60]))

    def _open_recommend(self):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih laporan pasien terlebih dahulu.")
            return
        rid = int(sel[0])
        report = next(r for r in store.disease_reports if r["id"] == rid)

        def _save(data):
            try:
                store.add_treatment_recommendation(rid, data["treatment_recommendation"])
                show_success(self, "Rekomendasi penanganan medis berhasil disimpan.")
            except ValueError as e:
                show_error(self, str(e))
            self._reload_table()

        FormDialog(self, f"Rekomendasi untuk {report['patient_name']}", [
            {"key": "treatment_recommendation", "label": "Rekomendasi Penanganan", "type": "textarea",
             "default": report.get("treatment_recommendation") or ""}
        ], on_submit=_save, width=460)

    def on_show(self):
        self._render()