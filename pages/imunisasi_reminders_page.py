import tkinter as tk

from data.store import store
from pages.sidebar import AppShell
from pages.widgets import make_table, show_error, show_success

STATUS_COLOR = {"pending": "#ea580c", "sent": "#16a34a"}
CHANNEL_LABEL = {"whatsapp": "WhatsApp", "sms": "SMS", "email": "Email"}

class ImunisasiRemindersPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app
        self.shell = AppShell(self, app, active_key="imunisasi_reminders", title="Reminder Imunisasi")
        self.shell.pack(fill="both", expand=True)
        self.filter_status = ""
        self._render()

    def _render(self):
        for w in self.shell.content.winfo_children():
            w.destroy()

        filter_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        filter_bar.pack(fill="x", pady=(0, 10))
        for label, val in [("Semua", ""), ("Pending", "pending"), ("Terkirim", "sent")]:
            tk.Button(filter_bar, text=label, font=("Segoe UI", 8),
                      bg="#2563eb" if self.filter_status == val else "#e2e8f0",
                      fg="white" if self.filter_status == val else "#334155",
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=lambda v=val: self._set_filter(v)).pack(side="left", padx=4)

        columns = [("child", "Anak", 140), ("vaccine", "Vaksin", 120), ("parent", "Orang Tua", 140),
                   ("channel", "Channel", 90), ("scheduled_date", "Tgl Jadwal", 100), ("status", "Status", 90)]
        table_frame, self.tree = make_table(self.shell.content, columns)
        table_frame.pack(fill="both", expand=True)
        for s, c in STATUS_COLOR.items():
            self.tree.tag_configure(s, foreground=c)

        action_bar = tk.Frame(self.shell.content, bg="#f1f5f9")
        action_bar.pack(fill="x", pady=(8, 0))
        tk.Button(action_bar, text="🔔 Kirim Reminder", command=self._send_selected, bg="#0d9488",
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Label(action_bar, text="(Simulasi pengiriman via WhatsApp/SMS/Email)", bg="#f1f5f9",
                 fg="#94a3b8", font=("Segoe UI", 8)).pack(side="left", padx=10)

        self._reload_table()

    def _set_filter(self, val):
        self.filter_status = val
        self._render()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in reversed(store.immunization_reminders):
            if self.filter_status and r["status"] != self.filter_status:
                continue
            record = next((rec for rec in store.immunization_records if rec["id"] == r["record_id"]), None)
            child_name = store.lookup_name(store.children, record["child_id"]) if record else "-"
            vaccine_name = store.lookup_name(store.immunization_vaccines, record["vaccine_id"]) if record else "-"
            sched_date = record["scheduled_date"] if record else "-"
            parent_name = store.lookup_name(store.users, r["parent_id"])
            self.tree.insert("", "end", iid=r["id"], tags=(r["status"],), values=(
                child_name, vaccine_name, parent_name, CHANNEL_LABEL.get(r["channel"], r["channel"]),
                sched_date, "Terkirim" if r["status"] == "sent" else "Pending"))

    def _send_selected(self):
        sel = self.tree.selection()
        if not sel:
            show_error(self, "Silakan pilih reminder terlebih dahulu.")
            return
        rid = int(sel[0])
        try:
            store.send_reminder(rid)
            show_success(self, "Reminder berhasil dikirim.")
        except ValueError as e:
            show_error(self, str(e))
        self._reload_table()

    def on_show(self):
        self._render()