import tkinter as tk
from tkinter import ttk, messagebox

def make_table(parent, columns):
    frame = tk.Frame(parent, bg="white")
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings", height=14)
    for key, label, width in columns:
        tree.heading(key, text=label)
        tree.column(key, width=width, anchor="w")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return frame, tree


def toolbar(parent, on_search=None, on_add=None, add_label="+ Tambah Data", search_placeholder="Cari..."):
    bar = tk.Frame(parent, bg="#f1f5f9")
    var_search = tk.StringVar()

    search_entry = ttk.Entry(bar, textvariable=var_search, width=30)
    search_entry.pack(side="left")
    search_entry.insert(0, "")
    if on_search:
        search_entry.bind("<KeyRelease>", lambda e: on_search(var_search.get()))

    tk.Label(bar, text="🔍", bg="#f1f5f9").pack(side="left", padx=(4, 12))

    if on_add:
        btn = tk.Button(bar, text=add_label, font=("Segoe UI", 9, "bold"), bg="#0d9488",
                         fg="white", relief="flat", padx=14, pady=6, cursor="hand2", command=on_add)
        btn.pack(side="right")
    return bar, var_search


class FormDialog(tk.Toplevel):
    def __init__(self, parent, title, fields, initial=None, on_submit=None, width=460):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{min(120 + len(fields) * 62, 720)}")
        self.configure(bg="white")
        self.resizable(False, True)
        self.transient(parent)
        self.grab_set()

        self.fields = fields
        self.initial = initial or {}
        self.on_submit = on_submit
        self.vars = {}

        self._build()

    def _build(self):
        canvas_outer = tk.Frame(self, bg="white")
        canvas_outer.pack(fill="both", expand=True, padx=24, pady=20)

        for f in self.fields:
            key = f["key"]
            ftype = f.get("type", "entry")
            label = f.get("label", key)

            tk.Label(canvas_outer, text=label, font=("Segoe UI", 9, "bold"), bg="white",
                     fg="#334155", anchor="w").pack(fill="x", pady=(6, 2))

            default_val = self.initial.get(key, f.get("default", ""))

            if ftype in ("entry", "number", "float", "date"):
                var = tk.StringVar(value="" if default_val is None else str(default_val))
                ttk.Entry(canvas_outer, textvariable=var).pack(fill="x")
                self.vars[key] = var
                if ftype == "date":
                    tk.Label(canvas_outer, text="format: YYYY-MM-DD", font=("Segoe UI", 7),
                             bg="white", fg="#94a3b8").pack(anchor="w")

            elif ftype == "password":
                var = tk.StringVar(value="")
                ttk.Entry(canvas_outer, textvariable=var, show="*").pack(fill="x")
                self.vars[key] = var

            elif ftype == "textarea":
                txt = tk.Text(canvas_outer, height=3, font=("Segoe UI", 9))
                txt.pack(fill="x")
                if default_val:
                    txt.insert("1.0", str(default_val))
                self.vars[key] = txt

            elif ftype == "combobox":
                options = f.get("options", [])
                display_map = {disp: val for val, disp in options}
                value_map = {val: disp for val, disp in options}
                var = tk.StringVar(value=value_map.get(default_val, ""))
                cb = ttk.Combobox(canvas_outer, textvariable=var, state="readonly",
                                   values=[disp for _, disp in options])
                cb.pack(fill="x")
                self.vars[key] = (var, display_map)

            elif ftype == "radio":
                options = f.get("options", [])
                var = tk.StringVar(value=default_val or (options[0][0] if options else ""))
                radio_frame = tk.Frame(canvas_outer, bg="white")
                radio_frame.pack(fill="x", anchor="w")
                for val, disp in options:
                    ttk.Radiobutton(radio_frame, text=disp, value=val, variable=var).pack(
                        side="left", padx=(0, 14))
                self.vars[key] = var

        btn_row = tk.Frame(canvas_outer, bg="white")
        btn_row.pack(fill="x", pady=(20, 0))
        tk.Button(btn_row, text="Batal", font=("Segoe UI", 9), bg="#e2e8f0", relief="flat",
                  padx=14, pady=8, cursor="hand2", command=self.destroy).pack(side="right", padx=(8, 0))
        tk.Button(btn_row, text="Simpan", font=("Segoe UI", 9, "bold"), bg="#0d9488", fg="white",
                  relief="flat", padx=14, pady=8, cursor="hand2", command=self._submit).pack(side="right")

    def _collect(self):
        data = {}
        for f in self.fields:
            key = f["key"]
            ftype = f.get("type", "entry")
            required = f.get("required", True)
            v = self.vars[key]

            if ftype == "textarea":
                value = v.get("1.0", "end").strip()
            elif ftype == "combobox":
                var, display_map = v
                value = display_map.get(var.get(), None)
            else:
                value = v.get().strip() if hasattr(v, "get") else v.get()
                if isinstance(value, str):
                    value = value.strip()

            if required and (value is None or value == ""):
                raise ValueError(f"{f.get('label', key)} wajib diisi.")

            if value not in (None, "") and ftype == "number":
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(f"{f.get('label', key)} harus berupa angka bulat.")
            elif value not in (None, "") and ftype == "float":
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"{f.get('label', key)} harus berupa angka.")

            if value == "":
                value = None

            data[key] = value
        return data

    def _submit(self):
        try:
            data = self._collect()
            if self.on_submit:
                self.on_submit(data)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Validasi", str(e), parent=self)


def confirm_delete(parent, message="Apakah Anda yakin ingin menghapus data ini?"):
    return messagebox.askyesno("Konfirmasi Hapus", message, parent=parent)


def show_success(parent, message):
    messagebox.showinfo("Sukses", message, parent=parent)


def show_error(parent, message):
    messagebox.showerror("Error", message, parent=parent)