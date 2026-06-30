import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_success


class AdminDiseaseTypesPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="admin_disease_types", title="Kelola Jenis Penyakit")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    FIELDS = [
        {"key": "code", "label": "Kode (maks 10 karakter)"},
        {"key": "name", "label": "Nama Penyakit"},
        {"key": "description", "label": "Deskripsi", "type": "textarea", "required": False},
    ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add)
        bar.pack(fill="x", pady=(0, 10))

        columns = [("code", "Kode", 80), ("name", "Nama Penyakit", 220), ("description", "Deskripsi", 320)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

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

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for dt in store.disease_types:
            blob = (dt["name"] + dt["code"] + (dt.get("description") or "")).lower()
            if self.search_term and self.search_term not in blob:
                continue
            self.tree.insert("", "end", iid=dt["id"], values=(
                dt["code"], dt["name"], (dt.get("description") or "-")[:80]))

    def _open_add(self):
        FormDialog(self, "Tambah Jenis Penyakit", self.FIELDS, on_submit=self._save_new)

    def _save_new(self, data):
        if any(dt["code"].upper() == data["code"].upper() for dt in store.disease_types):
            raise ValueError("Kode jenis penyakit sudah digunakan.")
        store.add_disease_type(data)
        show_success(self, "Jenis penyakit berhasil ditambahkan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        did = self._selected_id()
        if did is None:
            return
        dt = next(d for d in store.disease_types if d["id"] == did)
        FormDialog(self, "Edit Jenis Penyakit", self.FIELDS, initial=dt,
                   on_submit=lambda data: self._save_edit(did, data))

    def _save_edit(self, did, data):
        if any(d["id"] != did and d["code"].upper() == data["code"].upper() for d in store.disease_types):
            raise ValueError("Kode jenis penyakit sudah digunakan.")
        store.update_disease_type(did, data)
        show_success(self, "Jenis penyakit berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        did = self._selected_id()
        if did is None:
            return
        if confirm_delete(self):
            try:
                store.delete_disease_type(did)
                show_success(self, "Jenis penyakit berhasil dihapus.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            self._reload_table()

    def on_show(self):
        self._render()