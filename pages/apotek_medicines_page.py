import tkinter as tk
from datetime import date
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, confirm_delete, show_success

class ApotekMedicinesPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="apotek_medicines", title="Data Stok Obat")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    def _fields(self):
        cat_opts = [(c["id"], c["name"]) for c in store.medicine_categories]
        unit_opts = [(u["id"], u["name"]) for u in store.medicine_units]
        return [
            {"key": "code", "label": "Kode Obat"},
            {"key": "name", "label": "Nama Obat"},
            {"key": "category_id", "label": "Kategori", "type": "combobox", "options": cat_opts},
            {"key": "unit_id", "label": "Satuan", "type": "combobox", "options": unit_opts},
            {"key": "stock", "label": "Stok", "type": "number"},
            {"key": "min_stock", "label": "Stok Minimum", "type": "number"},
            {"key": "purchase_price", "label": "Harga Beli", "type": "float"},
            {"key": "selling_price", "label": "Harga Jual", "type": "float"},
            {"key": "expiration_date", "label": "Tanggal Kadaluarsa", "type": "date"},
            {"key": "description", "label": "Deskripsi", "type": "textarea", "required": False},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=self._open_add,
                          add_label="+ Tambah Obat")
        bar.pack(fill="x", pady=(0, 10))

        columns = [("code", "Kode", 70), ("name", "Nama Obat", 160), ("category", "Kategori", 110),
                   ("unit", "Satuan", 80), ("stock", "Stok", 60), ("min_stock", "Min.", 50),
                   ("price", "Harga Jual", 90), ("expired", "Kadaluarsa", 100)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        self.tree.tag_configure("low", foreground="#dc2626")
        self.tree.tag_configure("expired", foreground="#b91c1c", background="#fee2e2")

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="Edit Terpilih", command=self._open_edit, bg="#2563eb", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="Hapus Terpilih", command=self._delete_selected, bg="#dc2626", fg="white",
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))
        tk.Label(action_bar, text="🔴 Stok ≤ minimum   🟥 Sudah kadaluarsa", bg="#f1f5f9",
                 fg="#94a3b8", font=("Segoe UI", 8)).pack(side="left", padx=14)

        self._reload_table()

    def _on_search(self, term):
        self.search_term = term.lower()
        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        today = date.today().isoformat()
        for m in store.medicines:
            blob = (m["name"] + m["code"]).lower()
            if self.search_term and self.search_term not in blob:
                continue
            cat_name = store.lookup_name(store.medicine_categories, m["category_id"])
            unit_name = store.lookup_name(store.medicine_units, m["unit_id"])
            tag = ()
            if m["expiration_date"] < today:
                tag = ("expired",)
            elif m["stock"] <= m["min_stock"]:
                tag = ("low",)
            self.tree.insert("", "end", iid=m["id"], tags=tag, values=(
                m["code"], m["name"], cat_name, unit_name, m["stock"], m["min_stock"],
                f"Rp{m['selling_price']:,.0f}", m["expiration_date"]))

    def _open_add(self):
        FormDialog(self, "Tambah Data Obat", self._fields(), on_submit=self._save_new, width=480)

    def _save_new(self, data):
        if any(m["code"].lower() == data["code"].lower() for m in store.medicines):
            raise ValueError("Kode obat sudah digunakan.")
        store.add_medicine(data)
        show_success(self, "Obat berhasil ditambahkan.")
        self._reload_table()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris data terlebih dahulu.")
            return None
        return int(sel[0])

    def _open_edit(self):
        mid = self._selected_id()
        if mid is None:
            return
        med = next(m for m in store.medicines if m["id"] == mid)
        FormDialog(self, "Edit Data Obat", self._fields(), initial=med,
                   on_submit=lambda data: self._save_edit(mid, data), width=480)

    def _save_edit(self, mid, data):
        if any(m["id"] != mid and m["code"].lower() == data["code"].lower() for m in store.medicines):
            raise ValueError("Kode obat sudah digunakan.")
        store.update_medicine(mid, data)
        show_success(self, "Obat berhasil diperbarui.")
        self._reload_table()

    def _delete_selected(self):
        mid = self._selected_id()
        if mid is None:
            return
        if confirm_delete(self):
            store.delete_medicine(mid)
            show_success(self, "Obat berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()