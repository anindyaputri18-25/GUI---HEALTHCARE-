import tkinter as tk
from tkinter import messagebox

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, toolbar, confirm_delete, show_success


class AdminLogsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="admin_logs", title="Log Aktivitas Sistem")
        self.shell.pack(fill="both", expand=True)
        self.search_term = ""
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        bar, _ = toolbar(self.shell.content, on_search=self._on_search, on_add=None)
        bar.pack(fill="x", pady=(0, 10))

        columns = [("created_at", "Waktu", 100), ("user", "User", 140), ("action", "Aksi", 160),
                   ("description", "Deskripsi", 320), ("ip_address", "IP Address", 100)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="Hapus Log Terpilih", command=self._delete_selected, bg="#dc2626",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")

        self._reload_table()

    def _on_search(self, term):
        self.search_term = term.lower()
        self._reload_table()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for log in reversed(store.activity_logs):
            user_name = store.lookup_name(store.users, log.get("user_id")) if log.get("user_id") else "System"
            blob = (log["description"] + log["action"] + log["ip_address"] + user_name).lower()
            if self.search_term and self.search_term not in blob:
                continue
            self.tree.insert("", "end", iid=log["id"], values=(
                log["created_at"], user_name, log["action"], log["description"], log["ip_address"]))

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Silakan pilih log yang ingin dihapus.")
            return
        if confirm_delete(self, "Hapus log aktivitas ini?"):
            store.delete_log(int(sel[0]))
            show_success(self, "Log aktivitas berhasil dihapus.")
            self._reload_table()

    def on_show(self):
        self._render()