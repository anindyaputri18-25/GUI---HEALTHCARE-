import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_error, show_success

GENDER_OPTIONS = [("L", "Laki-laki"), ("P", "Perempuan")]

class ImunisasiChildrenPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="imunisasi_children", title="Data Anak (Imunisasi)")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    def _fields(self):
        parent_opts = [(u["id"], u["name"]) for u in store.users if u["role"] == "warga"]
        return [
            {"key": "name", "label": "Nama Anak"},
            {"key": "nik", "label": "NIK Anak (16 digit)", "required": False},
            {"key": "gender", "label": "Jenis Kelamin", "type": "radio", "options": GENDER_OPTIONS},
            {"key": "date_of_birth", "label": "Tanggal Lahir", "type": "date"},
            {"key": "place_of_birth", "label": "Tempat Lahir", "required": False},
            {"key": "birth_weight", "label": "Berat Lahir (kg)", "type": "float", "required": False},
            {"key": "parent_id", "label": "Orang Tua (Warga)", "type": "combobox", "options": parent_opts},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add,
                          add_label="+ Tambah Data Anak")
        bar.pack(fill="x", pady=(0, 10))

        columns = [("name", "Nama Anak", 150), ("gender", "Gender", 60), ("date_of_birth", "Tgl Lahir", 100),
                   ("parent", "Orang Tua", 150), ("nik", "NIK", 140)]
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
        for c in store.children:
            blob = (c["name"] + (c.get("nik") or "")).lower()
            if self.search_term and self.search_term not in blob:
                continue
            parent_name = store.lookup_name(store.users, c["parent_id"])
            self.tree.insert("", "end", iid=c["id"], values=(
                c["name"], c["gender"], c["date_of_birth"], parent_name, c.get("nik") or "-"))

    def _open_add(self):
        if not any(u["role"] == "warga" for u in store.users):
            show_error(self, "Belum ada akun warga yang dapat dijadikan orang tua. Tambahkan user warga terlebih dahulu.")
            return
        FormDialog(self, "Tambah Data Anak", self._fields(), on_submit=self._save_new)

    def _save_new(self, data):
        if data.get("nik") and any(c.get("nik") == data["nik"] for c in store.children):
            raise ValueError("NIK anak sudah terdaftar.")
        store.add_child(data)
        show_success(self, "Data anak berhasil ditambahkan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        cid = self._selected_id()
        if cid is None:
            return
        child = next(c for c in store.children if c["id"] == cid)
        FormDialog(self, "Edit Data Anak", self._fields(), initial=child,
                   on_submit=lambda data: self._save_edit(cid, data))

    def _save_edit(self, cid, data):
        if data.get("nik") and any(c["id"] != cid and c.get("nik") == data["nik"] for c in store.children):
            raise ValueError("NIK anak sudah terdaftar.")
        store.update_child(cid, data)
        show_success(self, "Data anak berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        cid = self._selected_id()
        if cid is None:
            return
        if confirm_delete(self):
            store.delete_child(cid)
            show_success(self, "Data anak berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()