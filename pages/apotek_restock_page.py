import tkinter as tk

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, FormDialog, show_success

STATUS_LABEL = {"pending": "Menunggu Persetujuan", "approved": "Disetujui", "rejected": "Ditolak"}
STATUS_COLOR = {"pending": "#ea580c", "approved": "#16a34a", "rejected": "#dc2626"}

class ApotekRestockPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="apotek_restock", title="Pengajuan Restock Obat")
        self.shell.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        top_bar.pack(fill="x", pady=(0, 10))
        tk.Button(top_bar, text="+ Ajukan Restock Baru", font=("Segoe UI", 9, "bold"), bg="#0d9488",
                  fg="white", relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._open_add).pack(side="right")

        columns = [("medicine", "Obat", 180), ("quantity", "Jumlah Diajukan", 110), ("created_at", "Tgl Ajuan", 100),
                   ("status", "Status", 150)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        for s, c in STATUS_COLOR.items():
            self.tree.tag_configure(s, foreground=c)

        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(store.restock_requests):
            med_name = store.lookup_name(store.medicines, r["medicine_id"])
            self.tree.insert("", "end", iid=r["id"], tags=(r["status"],), values=(
                med_name, r["quantity"], r["created_at"], STATUS_LABEL.get(r["status"], r["status"])))

    def _open_add(self):
        med_opts = [(m["id"], m["name"]) for m in store.medicines]
        FormDialog(self, "Ajukan Permintaan Restock", [
            {"key": "medicine_id", "label": "Obat", "type": "combobox", "options": med_opts},
            {"key": "quantity", "label": "Jumlah yang Diajukan", "type": "number"},
        ], on_submit=self._save_new)

    def _save_new(self, data):
        store.add_restock_request(store.current_user["id"], data["medicine_id"], data["quantity"])
        show_success(self, "Permintaan restock berhasil diajukan, menunggu persetujuan admin.")
        self._reload_table()

    def on_show(self):
        self._render()