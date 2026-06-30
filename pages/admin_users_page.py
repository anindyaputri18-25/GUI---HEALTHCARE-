import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_success

ROLE_OPTIONS = [("admin", "Admin"), ("apoteker", "Apoteker"),
                 ("petugas_medis", "Petugas Medis"), ("warga", "Warga")]
GENDER_OPTIONS = [("L", "Laki-laki"), ("P", "Perempuan")]


class AdminUsersPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="admin_users", title="Kelola User")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    def _fields(self, editing=False):
        return [
            {"key": "name", "label": "Nama Lengkap"},
            {"key": "email", "label": "Email"},
            {"key": "password", "label": "Password" + (" (kosongkan jika tidak diubah)" if editing else ""),
             "type": "password", "required": not editing},
            {"key": "role", "label": "Role", "type": "combobox", "options": ROLE_OPTIONS},
            {"key": "nik", "label": "NIK (16 digit)", "required": False},
            {"key": "phone_number", "label": "No. Telepon", "required": False},
            {"key": "address", "label": "Alamat", "required": False},
            {"key": "gender", "label": "Jenis Kelamin", "type": "radio", "options": GENDER_OPTIONS, "required": False},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, var_search = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add)
        bar.pack(fill="x", pady=(0, 10))

        columns = [("name", "Nama", 160), ("email", "Email", 200), ("role", "Role", 110),
                   ("nik", "NIK", 140), ("phone_number", "Telepon", 120)]
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
        for u in store.users:
            if self.search_term and self.search_term not in (u["name"] + u["email"] + (u.get("nik") or "")).lower():
                continue
            self.tree.insert("", "end", iid=u["id"], values=(
                u["name"], u["email"], u["role"], u.get("nik") or "-", u.get("phone_number") or "-"))

    def _open_add(self):
        FormDialog(self, "Tambah User Baru", self._fields(editing=False), on_submit=self._save_new)

    def _save_new(self, data):
        if any(u["email"].lower() == data["email"].lower() for u in store.users):
            raise ValueError("Email sudah terdaftar.")
        if data.get("nik") and any(u.get("nik") == data["nik"] for u in store.users):
            raise ValueError("NIK sudah terdaftar.")
        store.add_user(data)
        show_success(self, "User berhasil ditambahkan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        uid = self._selected_id()
        if uid is None:
            return
        user = next(u for u in store.users if u["id"] == uid)
        FormDialog(self, "Edit User", self._fields(editing=True), initial=user,
                   on_submit=lambda data: self._save_edit(uid, data))

    def _save_edit(self, uid, data):
        if not data.get("password"):
            data.pop("password", None)
        for u in store.users:
            if u["id"] != uid and u["email"].lower() == data["email"].lower():
                raise ValueError("Email sudah terdaftar.")
        store.update_user(uid, data)
        show_success(self, "User berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        uid = self._selected_id()
        if uid is None:
            return
        if confirm_delete(self):
            try:
                store.delete_user(uid)
                show_success(self, "User berhasil dihapus.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            self._reload_table()

    def on_show(self):
        self._render()