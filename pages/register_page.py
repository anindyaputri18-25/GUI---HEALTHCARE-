# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

from data.store import store

class RegisterPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f1f5f9")
        self.app = app

        self.var_name = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_password_confirm = tk.StringVar()
        self.var_nik = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_gender = tk.StringVar(value="L")

        self._build_ui()

    def _build_ui(self):
        canvas_card = tk.Frame(self, bg="white", highlightbackground="#e2e8f0",
                                highlightthickness=1)
        canvas_card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=620)

        tk.Label(canvas_card, text="Daftar Akun Warga", font=("Segoe UI", 16, "bold"),
                 bg="white", fg="#1e293b").pack(pady=(24, 4))
        tk.Label(canvas_card, text="Lengkapi data diri Anda di bawah ini",
                 font=("Segoe UI", 9), bg="white", fg="#64748b").pack(pady=(0, 16))

        form = tk.Frame(canvas_card, bg="white")
        form.pack(fill="both", expand=True, padx=40)

        def labeled_entry(label, var, show=None):
            tk.Label(form, text=label, font=("Segoe UI", 9, "bold"), bg="white",
                     fg="#334155", anchor="w").pack(fill="x")
            e = ttk.Entry(form, textvariable=var, show=show, font=("Segoe UI", 10))
            e.pack(fill="x", pady=(2, 10))
            return e

        labeled_entry("Nama Lengkap", self.var_name)
        labeled_entry("Email", self.var_email)
        labeled_entry("Password", self.var_password, show="*")
        labeled_entry("Konfirmasi Password", self.var_password_confirm, show="*")
        labeled_entry("NIK (16 digit)", self.var_nik)
        labeled_entry("No. Telepon", self.var_phone)
        labeled_entry("Alamat", self.var_address)

        tk.Label(form, text="Jenis Kelamin", font=("Segoe UI", 9, "bold"), bg="white",
                 fg="#334155", anchor="w").pack(fill="x")
        gender_frame = tk.Frame(form, bg="white")
        gender_frame.pack(fill="x", pady=(2, 14))
        ttk.Radiobutton(gender_frame, text="Laki-laki", value="L",
                         variable=self.var_gender).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(gender_frame, text="Perempuan", value="P",
                         variable=self.var_gender).pack(side="left")

        btn = tk.Button(form, text="Daftar", font=("Segoe UI", 10, "bold"),
                         bg="#16a34a", fg="white", relief="flat", height=2,
                         cursor="hand2", command=self.handle_register)
        btn.pack(fill="x", pady=(4, 0))

        link_login = tk.Label(canvas_card, text="Sudah punya akun? Masuk di sini",
                               font=("Segoe UI", 9, "underline"), fg="#2563eb",
                               bg="white", cursor="hand2")
        link_login.pack(pady=14)
        link_login.bind("<Button-1>", lambda e: self.app.show_page("login"))

    def handle_register(self):
        name = self.var_name.get().strip()
        email = self.var_email.get().strip()
        password = self.var_password.get()
        password_confirm = self.var_password_confirm.get()
        nik = self.var_nik.get().strip()
        phone = self.var_phone.get().strip()
        address = self.var_address.get().strip()
        gender = self.var_gender.get()

        # Validasi 
        if not all([name, email, password, nik, phone, address]):
            messagebox.showerror("Validasi", "Semua field wajib diisi.")
            return
        if password != password_confirm:
            messagebox.showerror("Validasi", "Konfirmasi password tidak cocok.")
            return
        if len(nik) != 16 or not nik.isdigit():
            messagebox.showerror("Validasi", "NIK harus tepat 16 digit.")
            return
        if len(phone) > 15:
            messagebox.showerror("Validasi", "No. Telepon maksimal 15 karakter.")
            return

        try:
            store.register_warga({
                "name": name, "email": email, "password": password,
                "nik": nik, "phone_number": phone, "address": address,
                "gender": gender,
            })
        except ValueError as e:
            # Jika akun sudah pernah terdaftar (email/NIK), arahkan ke halaman login
            # supaya pengguna tidak perlu mengisi ulang form
            if "sudah terdaftar" in str(e):
                messagebox.showinfo("Akun Sudah Terdaftar", f"{e}\nSilakan masuk menggunakan akun Anda.")
                self._clear_form()
                self.app.show_page("login")
            else:
                messagebox.showerror("Validasi", str(e))
            return

        messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan masuk.")
        self._clear_form()
        self.app.show_page("login")

    def _clear_form(self):
        for var in [self.var_name, self.var_email, self.var_password,
                    self.var_password_confirm, self.var_nik, self.var_phone,
                    self.var_address]:
            var.set("")
        self.var_gender.set("L")

    def on_show(self):
        pass