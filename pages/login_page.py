import tkinter as tk
from tkinter import ttk, messagebox

from data.store import store

class LoginPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app  

        self.var_email = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_remember = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        card = tk.Frame(self, bg="white", bd=0, highlightbackground="#e2e8f0",
                         highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

        tk.Label(card, text="🏥", font=("Segoe UI Emoji", 32), bg="white").pack(pady=(30, 0))
        tk.Label(card, text="Sistem Posyandu Desa", font=("Segoe UI", 16, "bold"),
                 bg="white", fg="#1e293b").pack(pady=(5, 0))
        tk.Label(card, text="Masuk ke akun Anda", font=("Segoe UI", 10),
                 bg="white", fg="#64748b").pack(pady=(0, 20))

        form = tk.Frame(card, bg="white")
        form.pack(fill="x", padx=40)

        tk.Label(form, text="Email", font=("Segoe UI", 9, "bold"), bg="white",
                 fg="#334155", anchor="w").pack(fill="x")
        entry_email = ttk.Entry(form, textvariable=self.var_email, font=("Segoe UI", 10))
        entry_email.pack(fill="x", pady=(2, 12))

        tk.Label(form, text="Password", font=("Segoe UI", 9, "bold"), bg="white",
                 fg="#334155", anchor="w").pack(fill="x")
        entry_password = ttk.Entry(form, textvariable=self.var_password, show="*",
                                    font=("Segoe UI", 10))
        entry_password.pack(fill="x", pady=(2, 8))

        ttk.Checkbutton(form, text="Ingat saya", variable=self.var_remember).pack(
            anchor="w", pady=(0, 16))

        btn_login = tk.Button(form, text="Masuk", font=("Segoe UI", 10, "bold"),
                               bg="#2563eb", fg="white", activebackground="#1d4ed8",
                               relief="flat", height=2, cursor="hand2",
                               command=self.handle_login)
        btn_login.pack(fill="x")

        link_register = tk.Label(card, text="Belum punya akun? Daftar di sini",
                                  font=("Segoe UI", 9, "underline"), fg="#2563eb",
                                  bg="white", cursor="hand2")
        link_register.pack(pady=18)
        link_register.bind("<Button-1>", lambda e: self.app.show_page("register"))

        # Info kredensial demo 
        demo = tk.Label(
            card,
            text="Demo: admin@healthcare.test / admin123",
            font=("Segoe UI", 8), fg="#94a3b8", bg="white",
        )
        demo.pack(side="bottom", pady=10)

        entry_email.focus_set()
        entry_password.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        email = self.var_email.get().strip()
        password = self.var_password.get()

        if not email or not password:
            messagebox.showerror("Validasi", "Email dan password wajib diisi.")
            return

        user = store.authenticate(email, password)
        if user is None:
            messagebox.showerror("Login Gagal", "Email atau password yang Anda masukkan salah.")
            return

        store.current_user = user
        store.log("login", "User logged in successfully.", user["id"])

        # Reset form
        self.var_email.set("")
        self.var_password.set("")

        # redirect()->intended(route('dashboard'))
        self.app.go_to_dashboard()

    def on_show(self):
        pass