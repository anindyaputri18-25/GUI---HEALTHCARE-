import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, show_success, show_error

STATUS_COLOR = {"pending": "#ea580c", "approved": "#16a34a", "rejected": "#dc2626"}


class AdminRestockPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="admin_restock", title="Approval Pengajuan Restock")
        self.shell.pack(fill="both", expand=True)
        self.filter_status = ""
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        tk.Label(filter_bar, text="Filter status:", bg="#f1f5f9", font=("Segoe UI", 9)).pack(side="left")
        for label, val in [("Semua", ""), ("Pending", "pending"), ("Disetujui", "approved"), ("Ditolak", "rejected")]:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_status == val else "#e2e8f0",
                      fg="white" if self.filter_status == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)

        columns = [("id", "No.", 50), ("medicine", "Obat", 180), ("user", "Diajukan Oleh", 160),
                   ("quantity", "Jumlah", 80), ("created_at", "Tgl Pengajuan", 110), ("status", "Status", 100)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="✅ Setujui", command=lambda: self._process("approve"), bg="#16a34a",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(action_bar, text="❌ Tolak", command=lambda: self._process("reject"), bg="#dc2626",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=(8, 0))
        tk.Label(action_bar, text="Hanya permintaan berstatus 'pending' yang dapat diproses.",
                 bg="#f1f5f9", fg="#94a3b8", font=("Segoe UI", 8)).pack(side="left", padx=14)

        self._reload_table()

    def _set_filter(self, val):
        self.filter_status = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(store.restock_requests):
            if self.filter_status and r["status"] != self.filter_status:
                continue
            med_name = store.lookup_name(store.medicines, r["medicine_id"])
            user_name = store.lookup_name(store.users, r["user_id"])
            self.tree.insert("", "end", iid=r["id"], values=(
                r["id"], med_name, user_name, r["quantity"], r["created_at"], r["status"]))

    def _process(self, action):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih permintaan restock terlebih dahulu.")
            return
        rid = int(sel[0])
        try:
            store.process_restock(rid, action)
            msg = ("Permintaan restock disetujui, stok obat otomatis ditambahkan."
                   if action == "approve" else "Permintaan restock ditolak.")
            show_success(self, msg)
        except ValueError as e:
            show_error(self, str(e))
        self._reload_table()

    def on_show(self):
        self._render()