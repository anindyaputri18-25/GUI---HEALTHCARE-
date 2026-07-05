import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_success

class AdminVillagesPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="admin_villages", title="Kelola Wilayah / Desa")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    FIELDS = [
        {"key": "name", "label": "Nama Desa"},
        {"key": "kecamatan", "label": "Kecamatan"},
        {"key": "kabupaten", "label": "Kabupaten"},
        {"key": "latitude", "label": "Latitude", "type": "float"},
        {"key": "longitude", "label": "Longitude", "type": "float"},
    ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add)
        bar.pack(fill="x", pady=(0, 10))

        columns = [("name", "Nama Desa", 160), ("kecamatan", "Kecamatan", 140),
                   ("kabupaten", "Kabupaten", 140), ("latitude", "Latitude", 100),
                   ("longitude", "Longitude", 100)]
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
        for v in store.villages:
            blob = (v["name"] + v["kecamatan"] + v["kabupaten"]).lower()
            if self.search_term and self.search_term not in blob:
                continue
            self.tree.insert("", "end", iid=v["id"], values=(
                v["name"], v["kecamatan"], v["kabupaten"], v["latitude"], v["longitude"]))

    def _open_add(self):
        FormDialog(self, "Tambah Wilayah/Desa", self.FIELDS, on_submit=self._save_new)

    def _save_new(self, data):
        store.add_village(data)
        show_success(self, "Data wilayah/desa berhasil ditambahkan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        vid = self._selected_id()
        if vid is None:
            return
        village = next(v for v in store.villages if v["id"] == vid)
        FormDialog(self, "Edit Wilayah/Desa", self.FIELDS, initial=village,
                   on_submit=lambda data: self._save_edit(vid, data))

    def _save_edit(self, vid, data):
        store.update_village(vid, data)
        show_success(self, "Data wilayah/desa berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        vid = self._selected_id()
        if vid is None:
            return
        if confirm_delete(self):
            store.delete_village(vid)
            show_success(self, "Data wilayah/desa berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()