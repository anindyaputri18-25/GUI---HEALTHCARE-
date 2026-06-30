import tkinter as tk

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, FormDialog, confirm_delete, show_success

GENDER_OPTIONS = [("L", "Laki-laki"), ("P", "Perempuan")]
STATUS_LABEL = {"scheduled": "Terjadwal", "completed": "Selesai", "missed": "Terlewat"}
STATUS_COLOR = {"scheduled": "#2563eb", "completed": "#16a34a", "missed": "#dc2626"}

class WargaChildrenPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="warga_children", title="Data Anak Saya")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _my_children(self):
        uid = store.current_user["id"]
        return [c for c in store.children if c["parent_id"] == uid]

    FIELDS = [
        {"key": "name", "label": "Nama Anak"},
        {"key": "nik", "label": "NIK Anak (16 digit)", "required": False},
        {"key": "gender", "label": "Jenis Kelamin", "type": "radio", "options": GENDER_OPTIONS},
        {"key": "date_of_birth", "label": "Tanggal Lahir", "type": "date"},
        {"key": "place_of_birth", "label": "Tempat Lahir", "required": False},
        {"key": "birth_weight", "label": "Berat Lahir (kg)", "type": "float", "required": False},
    ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        top_bar.pack(fill="x", pady=(0, 10))
        tk.Label(top_bar, text="Daftar anak yang terdaftar atas nama Anda.", bg="#f1f5f9",
                 fg="#64748b", font=("Segoe UI", 9)).pack(side="left")
        tk.Button(top_bar, text="+ Tambah Data Anak", font=("Segoe UI", 9, "bold"), bg="#0d9488",
                  fg="white", relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._open_add).pack(side="right")

        columns = [("name", "Nama Anak", 150), ("gender", "Gender", 60), ("date_of_birth", "Tgl Lahir", 100),
                   ("nik", "NIK", 140)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="Edit Terpilih", command=self._open_edit, bg="#2563eb", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="Hapus Terpilih", command=self._delete_selected, bg="#dc2626", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))
        tk.Button(action_bar, text="📋 Riwayat Imunisasi", command=self._view_history, bg="#0891b2",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))

        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for c in self._my_children():
            self.tree.insert("", "end", iid=c["id"], values=(
                c["name"], c["gender"], c["date_of_birth"], c.get("nik") or "-"))

    def _open_add(self):
        FormDialog(self, "Tambah Data Anak", self.FIELDS, on_submit=self._save_new)

    def _save_new(self, data):
        if data.get("nik") and any(c.get("nik") == data["nik"] for c in store.children):
            raise ValueError("NIK anak sudah terdaftar.")
        data["parent_id"] = store.current_user["id"]
        store.add_child(data)
        show_success(self, "Data anak berhasil ditambahkan.")
        self._reload_table()

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            tk.messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        cid = int(sel[0])
        return next(c for c in store.children if c["id"] == cid)

    def _open_edit(self):
        c = self._selected()
        if c is None:
            return
        FormDialog(self, "Edit Data Anak", self.FIELDS, initial=c,
                   on_submit=lambda data: self._save_edit(c["id"], data))

    def _save_edit(self, cid, data):
        if data.get("nik") and any(c["id"] != cid and c.get("nik") == data["nik"] for c in store.children):
            raise ValueError("NIK anak sudah terdaftar.")
        data["parent_id"] = store.current_user["id"]
        store.update_child(cid, data)
        show_success(self, "Data anak berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        c = self._selected()
        if c is None:
            return
        if confirm_delete(self):
            store.delete_child(c["id"])
            show_success(self, "Data anak berhasil dihapus.")
            self._reload_table()

    def _view_history(self):
        c = self._selected()
        if c is None:
            return
        records = [r for r in store.immunization_records if r["child_id"] == c["id"]]
        if not records:
            tk.messagebox.showinfo("Riwayat Imunisasi", f"Belum ada riwayat imunisasi untuk {c['name']}.")
            return
        lines = [f"Riwayat Imunisasi - {c['name']}", "-" * 30]
        for r in sorted(records, key=lambda x: x["scheduled_date"]):
            vaccine_name = store.lookup_name(store.immunization_vaccines, r["vaccine_id"])
            lines.append(f"{vaccine_name}: {STATUS_LABEL.get(r['status'])} (Jadwal: {r['scheduled_date']})")
        tk.messagebox.showinfo("Riwayat Imunisasi", "\n".join(lines))

    def on_show(self):
        self._render()