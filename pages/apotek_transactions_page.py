import tkinter as tk
from datetime import date

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, FormDialog, show_error, show_success

TYPE_OPTIONS = [("in", "Masuk"), ("out", "Keluar")]

class ApotekTransactionsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="apotek_transactions", title="Transaksi Stok Obat")
        self.shell.pack(fill="both", expand=True)
        self.filter_type = ""
        self._render()

    def _fields(self):
        med_opts = [(m["id"], m["name"]) for m in store.medicines]
        supplier_opts = [(s["id"], s["name"]) for s in store.suppliers]
        return [
            {"key": "medicine_id", "label": "Obat", "type": "combobox", "options": med_opts},
            {"key": "type", "label": "Jenis Transaksi", "type": "radio", "options": TYPE_OPTIONS},
            {"key": "quantity", "label": "Jumlah", "type": "number"},
            {"key": "transaction_date", "label": "Tanggal Transaksi", "type": "date",
             "default": date.today().isoformat()},
            {"key": "supplier_id", "label": "Supplier (untuk transaksi masuk)", "type": "combobox",
             "options": supplier_opts, "required": False},
            {"key": "notes", "label": "Catatan", "type": "textarea", "required": False},
        ]

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        for label, val in [("Semua", ""), ("Masuk", "in"), ("Keluar", "out")]:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_type == val else "#e2e8f0",
                      fg="white" if self.filter_type == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)

        tk.Button(filter_bar, text="+ Catat Transaksi", font=("Segoe UI", 9, "bold"), bg="#0d9488",
                  fg="white", relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._open_add).pack(side="right")

        columns = [("medicine", "Obat", 170), ("type", "Jenis", 70), ("quantity", "Jumlah", 70),
                   ("supplier", "Supplier", 150), ("date", "Tanggal", 100), ("notes", "Catatan", 200)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        self.tree.tag_configure("in", foreground="#16a34a")
        self.tree.tag_configure("out", foreground="#dc2626")

        self._reload_table()

    def _set_filter(self, val):
        self.filter_type = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for t in reversed(store.transactions):
            if self.filter_type and t["type"] != self.filter_type:
                continue
            med_name = store.lookup_name(store.medicines, t["medicine_id"])
            supplier_name = store.lookup_name(store.suppliers, t.get("supplier_id"), default="-") if t.get("supplier_id") else "-"
            self.tree.insert("", "end", iid=t["id"], tags=(t["type"],), values=(
                med_name, "Masuk" if t["type"] == "in" else "Keluar", t["quantity"],
                supplier_name, t["transaction_date"], t.get("notes") or "-"))

    def _open_add(self):
        FormDialog(self, "Catat Transaksi Obat", self._fields(), on_submit=self._save_new, width=480)

    def _save_new(self, data):
        if data["type"] == "in" and not data.get("supplier_id"):
            raise ValueError("Supplier wajib diisi untuk transaksi masuk.")
        if data["type"] == "out":
            data["supplier_id"] = None
        try:
            store.add_transaction(data)
        except ValueError as e:
            show_error(self, str(e))
            return
        show_success(self, "Transaksi stok berhasil disimpan.")
        self._reload_table()

    def on_show(self):
        self._render()