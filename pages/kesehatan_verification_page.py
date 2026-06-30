import tkinter as tk

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, FormDialog, show_error, show_success

class KesehatanVerificationPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="kesehatan_verification", title="Verifikasi Laporan Penyakit")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _pending_reports(self):
        return [r for r in store.disease_reports if r["status"] == "pending"]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        tk.Label(self.shell.content,
                 text="Daftar laporan dari warga yang menunggu verifikasi Anda.",
                 font=("Segoe UI", 9), bg="#f1f5f9", fg="#64748b").pack(anchor="w", pady=(0, 10))

        columns = [("patient_name", "Pasien", 150), ("disease", "Penyakit", 150), ("symptoms", "Gejala", 250),
                   ("severity", "Keparahan", 90), ("report_date", "Tgl Lapor", 100), ("reporter", "Pelapor", 130)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="✅ Verifikasi Laporan", command=lambda: self._process("verify"),
                  bg="#16a34a", fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="❌ Tolak Laporan", command=lambda: self._process("reject"),
                  bg="#dc2626", fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))

        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(self._pending_reports()):
            disease_name = store.lookup_name(store.disease_types, r["disease_type_id"])
            reporter_name = store.lookup_name(store.users, r["reporter_id"])
            self.tree.insert("", "end", iid=r["id"], values=(
                r["patient_name"], disease_name, r["symptoms"][:60], r["severity"].capitalize(),
                r["report_date"], reporter_name))

    def _process(self, action):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih laporan terlebih dahulu.")
            return
        rid = int(sel[0])

        def _save(data):
            try:
                store.process_verification(rid, action, data["notes"])
                show_success(self, "Laporan berhasil diverifikasi." if action == "verify" else "Laporan ditolak.")
            except ValueError as e:
                show_error(self, str(e))
            self._reload_table()

        FormDialog(self, "Catatan Verifikasi", [
            {"key": "notes", "label": "Catatan Verifikasi", "type": "textarea"}
        ], on_submit=_save, width=420)

    def on_show(self):
        self._render()