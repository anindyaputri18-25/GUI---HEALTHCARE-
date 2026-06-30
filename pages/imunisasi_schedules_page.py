import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_success

STATUS_OPTIONS = [("scheduled", "Terjadwal"), ("completed", "Selesai"), ("missed", "Terlewat")]
STATUS_COLOR = {"scheduled": "#2563eb", "completed": "#16a34a", "missed": "#dc2626"}

class ImunisasiSchedulesPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="imunisasi_schedules", title="Jadwal & Catatan Imunisasi")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self.filter_status = ""
        self._render()

    def _fields(self):
        child_opts = [(c["id"], c["name"]) for c in store.children]
        vaccine_opts = [(v["id"], v["name"]) for v in store.immunization_vaccines]
        return [
            {"key": "child_id", "label": "Anak", "type": "combobox", "options": child_opts},
            {"key": "vaccine_id", "label": "Vaksin", "type": "combobox", "options": vaccine_opts},
            {"key": "status", "label": "Status", "type": "radio", "options": STATUS_OPTIONS},
            {"key": "scheduled_date", "label": "Tanggal Terjadwal", "type": "date"},
            {"key": "administered_date", "label": "Tanggal Pelaksanaan (jika selesai)", "type": "date",
             "required": False},
            {"key": "batch_number", "label": "No. Batch Vaksin", "required": False},
            {"key": "notes", "label": "Catatan", "type": "textarea", "required": False},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add,
                          add_label="+ Tambah Jadwal")
        bar.pack(fill="x", pady=(0, 6))

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        for label, val in [("Semua", "")] + STATUS_OPTIONS:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_status == val else "#e2e8f0",
                      fg="white" if self.filter_status == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)

        columns = [("child", "Anak", 150), ("vaccine", "Vaksin", 120), ("scheduled_date", "Tgl Terjadwal", 100),
                   ("administered_date", "Tgl Pelaksanaan", 110), ("status", "Status", 90), ("batch", "No. Batch", 100)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        for s, c in STATUS_COLOR.items():
            self.tree.tag_configure(s, foreground=c)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="Edit Terpilih", command=self._open_edit, bg="#2563eb", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="Hapus Terpilih", command=self._delete_selected, bg="#dc2626", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))

        self._reload_table()

    def _on_search(self, term):
        self.search_term = term.lower()
        self._reload_table()

    def _set_filter(self, val):
        self.filter_status = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        records = sorted(store.immunization_records, key=lambda r: r["scheduled_date"])
        for r in records:
            child_name = store.lookup_name(store.children, r["child_id"])
            if self.search_term and self.search_term not in child_name.lower():
                continue
            if self.filter_status and r["status"] != self.filter_status:
                continue
            vaccine_name = store.lookup_name(store.immunization_vaccines, r["vaccine_id"])
            self.tree.insert("", "end", iid=r["id"], tags=(r["status"],), values=(
                child_name, vaccine_name, r["scheduled_date"], r.get("administered_date") or "-",
                dict(STATUS_OPTIONS)[r["status"]], r.get("batch_number") or "-"))

    def _open_add(self):
        if not store.children or not store.immunization_vaccines:
            messagebox.showwarning("Data Kosong", "Tambahkan data anak terlebih dahulu sebelum membuat jadwal imunisasi.")
            return
        FormDialog(self, "Tambah Jadwal/Catatan Imunisasi", self._fields(), on_submit=self._save_new, width=480)

    def _save_new(self, data):
        store.add_immunization_record(data)
        show_success(self, "Jadwal/catatan imunisasi berhasil disimpan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        rid = self._selected_id()
        if rid is None:
            return
        record = next(r for r in store.immunization_records if r["id"] == rid)
        FormDialog(self, "Edit Catatan Imunisasi", self._fields(), initial=record,
                   on_submit=lambda data: self._save_edit(rid, data), width=480)

    def _save_edit(self, rid, data):
        store.update_immunization_record(rid, data)
        show_success(self, "Catatan imunisasi berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        rid = self._selected_id()
        if rid is None:
            return
        if confirm_delete(self):
            store.delete_immunization_record(rid)
            show_success(self, "Catatan imunisasi berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()