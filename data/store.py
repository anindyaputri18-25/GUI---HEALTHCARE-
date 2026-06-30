from datetime import date, timedelta

def _today():
    return date.today().isoformat()

def _days(delta):
    return (date.today() + timedelta(days=delta)).isoformat()

class DataStore:
    def __init__(self):
        self.users = [
            {"id": 1, "name": "Admin Sistem", "email": "admin@healthcare.test",
             "password": "admin123", "role": "admin", "nik": "1111111111111111",
             "phone_number": "081200000001", "address": "Kantor Desa", "gender": "L"},
            {"id": 2, "name": "Apoteker Siti", "email": "apoteker@healthcare.test",
             "password": "apoteker123", "role": "apoteker", "nik": "2222222222222222",
             "phone_number": "081200000002", "address": "Apotek Desa", "gender": "P"},
            {"id": 3, "name": "Petugas Medis Budi", "email": "medis@healthcare.test",
             "password": "medis123", "role": "petugas_medis", "nik": "3333333333333333",
             "phone_number": "081200000003", "address": "Puskesmas Desa", "gender": "L"},
            {"id": 4, "name": "Warga Ani", "email": "warga@healthcare.test",
             "password": "warga123", "role": "warga", "nik": "4444444444444444",
             "phone_number": "081200000004", "address": "Dusun Melati", "gender": "P"},
            {"id": 5, "name": "Warga Joko", "email": "joko@healthcare.test",
             "password": "warga123", "role": "warga", "nik": "5555555555555555",
             "phone_number": "081200000005", "address": "Dusun Kenanga", "gender": "L"},
        ]
        self._next_user_id = 6

        # ====================== VILLAGES ======================
        self.villages = [
            {"id": 1, "name": "Desa Sukamaju", "kecamatan": "Cibinong", "kabupaten": "Bogor",
             "latitude": -6.4825, "longitude": 106.8508},
            {"id": 2, "name": "Desa Mekarsari", "kecamatan": "Citeureup", "kabupaten": "Bogor",
             "latitude": -6.4900, "longitude": 106.8700},
        ]
        self._next_village_id = 3

        # ====================== DISEASE TYPES ======================
        self.disease_types = [
            {"id": 1, "code": "DBD", "name": "Demam Berdarah Dengue",
             "description": "Penyakit yang disebabkan oleh virus dengue melalui gigitan nyamuk Aedes aegypti."},
            {"id": 2, "code": "ISPA", "name": "Infeksi Saluran Pernapasan Akut",
             "description": "Infeksi akut yang menyerang saluran pernapasan."},
            {"id": 3, "code": "DIARE", "name": "Diare", "description": "Gangguan pencernaan dengan frekuensi BAB meningkat."},
        ]
        self._next_disease_type_id = 4

        # ====================== MEDICINE CATEGORIES / UNITS ======================
        self.medicine_categories = [
            {"id": 1, "name": "Analgesik"},
            {"id": 2, "name": "Antibiotik"},
            {"id": 3, "name": "Vitamin"},
        ]
        self._next_medicine_category_id = 4

        self.medicine_units = [
            {"id": 1, "name": "Tablet"},
            {"id": 2, "name": "Botol"},
            {"id": 3, "name": "Strip"},
        ]
        self._next_medicine_unit_id = 4

        # ====================== MEDICINES ======================
        self.medicines = [
            {"id": 1, "code": "MED-001", "name": "Paracetamol 500mg", "category_id": 1, "unit_id": 1,
             "stock": 120, "min_stock": 30, "purchase_price": 200, "selling_price": 500,
             "expiration_date": _days(300), "description": "Obat penurun panas dan pereda nyeri."},
            {"id": 2, "code": "MED-002", "name": "Amoxicillin 500mg", "category_id": 2, "unit_id": 1,
             "stock": 15, "min_stock": 20, "purchase_price": 500, "selling_price": 1200,
             "expiration_date": _days(120), "description": "Antibiotik spektrum luas."},
            {"id": 3, "code": "MED-003", "name": "Vitamin C 100mg", "category_id": 3, "unit_id": 3,
             "stock": 80, "min_stock": 25, "purchase_price": 150, "selling_price": 400,
             "expiration_date": _days(-5), "description": "Suplemen daya tahan tubuh."},
        ]
        self._next_medicine_id = 4

        # ====================== SUPPLIERS ======================
        self.suppliers = [
            {"id": 1, "name": "PT Kimia Farma Trading"},
            {"id": 2, "name": "PT Anugerah Sehat"},
        ]
        self._next_supplier_id = 3

        # ====================== RESTOCK REQUESTS ======================
        self.restock_requests = [
            {"id": 1, "user_id": 2, "medicine_id": 2, "quantity": 50, "status": "pending",
             "approved_by": None, "approved_at": None, "created_at": _today()},
        ]
        self._next_restock_id = 2

        # ====================== TRANSACTIONS ======================
        self.transactions = [
            {"id": 1, "medicine_id": 1, "supplier_id": 1, "type": "in", "quantity": 100,
             "notes": "Pembelian awal stok.", "transaction_date": _days(-10), "user_id": 2},
            {"id": 2, "medicine_id": 1, "supplier_id": None, "type": "out", "quantity": 10,
             "notes": "Pemakaian Posyandu.", "transaction_date": _days(-2), "user_id": 2},
        ]
        self._next_transaction_id = 3

        # ====================== DISEASE REPORTS ======================
        self.disease_reports = [
            {"id": 1, "patient_name": "Budi Santoso", "patient_nik": "3201010101010001",
             "patient_age": 34, "patient_gender": "L", "patient_address": "Dusun Melati No. 5",
             "disease_type_id": 1, "symptoms": "Demam tinggi, bintik merah, nyeri sendi.",
             "severity": "sedang", "report_date": _days(-3), "latitude": -6.4830, "longitude": 106.8510,
             "village_id": 1, "reporter_id": 4, "status": "pending", "verified_by": None,
             "verification_notes": None, "treatment_recommendation": None},
            {"id": 2, "patient_name": "Siti Aminah", "patient_nik": "3201010101010002",
             "patient_age": 8, "patient_gender": "P", "patient_address": "Dusun Kenanga No. 12",
             "disease_type_id": 2, "symptoms": "Batuk, pilek, demam ringan.",
             "severity": "ringan", "report_date": _days(-1), "latitude": -6.4910, "longitude": 106.8720,
             "village_id": 2, "reporter_id": 3, "status": "verified", "verified_by": 3,
             "verification_notes": "Laporan diinput langsung oleh Petugas Kesehatan.",
             "treatment_recommendation": None},
        ]
        self._next_report_id = 3

        # ====================== CHILDREN ======================
        self.children = [
            {"id": 1, "name": "Putri Lestari", "nik": "3201010101020001", "gender": "P",
             "date_of_birth": "2023-02-10", "place_of_birth": "Bogor", "birth_weight": 3.1,
             "parent_id": 4},
            {"id": 2, "name": "Rizky Pratama", "nik": "3201010101020002", "gender": "L",
             "date_of_birth": "2022-11-05", "place_of_birth": "Bogor", "birth_weight": 3.4,
             "parent_id": 5},
        ]
        self._next_child_id = 3

        # ====================== IMMUNIZATION VACCINES ======================
        self.immunization_vaccines = [
            {"id": 1, "name": "BCG", "target_age_months": 1},
            {"id": 2, "name": "Polio", "target_age_months": 2},
            {"id": 3, "name": "DPT-HB-Hib", "target_age_months": 3},
            {"id": 4, "name": "Campak", "target_age_months": 9},
        ]
        self._next_vaccine_id = 5

        # ====================== IMMUNIZATION RECORDS ======================
        self.immunization_records = [
            {"id": 1, "child_id": 1, "vaccine_id": 1, "status": "completed",
             "scheduled_date": _days(-30), "administered_date": _days(-30),
             "batch_number": "BCG-2025-01", "notes": "Tidak ada reaksi.", "officer_id": 3},
            {"id": 2, "child_id": 2, "vaccine_id": 2, "status": "scheduled",
             "scheduled_date": _days(5), "administered_date": None,
             "batch_number": None, "notes": None, "officer_id": None},
        ]
        self._next_record_id = 3

        # ====================== IMMUNIZATION REMINDERS ======================
        self.immunization_reminders = [
            {"id": 1, "record_id": 2, "parent_id": 5, "channel": "whatsapp",
             "status": "pending", "created_at": _today()},
        ]
        self._next_reminder_id = 2

        # ====================== ACTIVITY LOGS ======================
        self.activity_logs = []

        # User yang sedang login (mirip Auth::user())
        self.current_user = None

        self.log("system", "Aplikasi HealthCare Desktop dimulai.", None)

    # AUTH
    def authenticate(self, email, password):
        for u in self.users:
            if u["email"].strip().lower() == email.strip().lower() and u["password"] == password:
                return u
        return None

    def register_warga(self, data):
        for u in self.users:
            if u["email"].strip().lower() == data["email"].strip().lower():
                raise ValueError("Email sudah terdaftar.")
            if u["nik"] == data["nik"]:
                raise ValueError("NIK sudah terdaftar.")

        new_user = {
            "id": self._next_user_id, "name": data["name"], "email": data["email"],
            "password": data["password"], "role": "warga", "nik": data["nik"],
            "phone_number": data["phone_number"], "address": data["address"],
            "gender": data["gender"],
        }
        self.users.append(new_user)
        self._next_user_id += 1
        self.log("register", f"User baru mendaftar: {new_user['name']}", new_user["id"])
        return new_user

    def log(self, action, description, user_id=None):
        self.activity_logs.append({
            "id": len(self.activity_logs) + 1, "action": action, "description": description,
            "user_id": user_id, "ip_address": "127.0.0.1", "created_at": _today(),
        })

    # GENERIC HELPERS
    @staticmethod
    def _find(items, item_id):
        for it in items:
            if it["id"] == item_id:
                return it
        return None

    def lookup_name(self, items, item_id, field="name", default="-"):
        item = self._find(items, item_id)
        return item.get(field, default) if item else default

    # USERS (admin.users)
    def add_user(self, data):
        data["id"] = self._next_user_id
        self._next_user_id += 1
        self.users.append(data)
        self.log("create_user", f"Created user {data['name']} ({data['role']})", self._uid())
        return data

    def update_user(self, user_id, data):
        user = self._find(self.users, user_id)
        if not user:
            raise ValueError("User tidak ditemukan.")
        user.update(data)
        self.log("update_user", f"Updated user {user['name']} ({user['role']})", self._uid())

    def delete_user(self, user_id):
        if self.current_user and self.current_user["id"] == user_id:
            raise ValueError("Anda tidak dapat menghapus akun Anda sendiri.")
        user = self._find(self.users, user_id)
        if user:
            self.users.remove(user)
            self.log("delete_user", f"Deleted user {user['name']} ({user['role']})", self._uid())

    # VILLAGES (admin.villages)
    def add_village(self, data):
        data["id"] = self._next_village_id
        self._next_village_id += 1
        self.villages.append(data)
        self.log("create_village", f"Added village: {data['name']}", self._uid())
        return data

    def update_village(self, village_id, data):
        v = self._find(self.villages, village_id)
        if not v:
            raise ValueError("Desa tidak ditemukan.")
        v.update(data)
        self.log("update_village", f"Updated village data: {v['name']}", self._uid())

    def delete_village(self, village_id):
        v = self._find(self.villages, village_id)
        if v:
            self.villages.remove(v)
            self.log("delete_village", f"Deleted village: {v['name']}", self._uid())

    # DISEASE TYPES (admin.disease_types)
    def add_disease_type(self, data):
        data["id"] = self._next_disease_type_id
        data["code"] = data["code"].upper()
        self._next_disease_type_id += 1
        self.disease_types.append(data)
        self.log("create_disease_type", f"Created disease type: {data['name']} ({data['code']})", self._uid())
        return data

    def update_disease_type(self, dt_id, data):
        dt = self._find(self.disease_types, dt_id)
        if not dt:
            raise ValueError("Jenis penyakit tidak ditemukan.")
        data["code"] = data["code"].upper()
        dt.update(data)
        self.log("update_disease_type", f"Updated disease type: {dt['name']} ({dt['code']})", self._uid())

    def delete_disease_type(self, dt_id):
        if any(r["disease_type_id"] == dt_id for r in self.disease_reports):
            raise ValueError("Tidak dapat menghapus jenis penyakit yang sedang digunakan dalam laporan kasus.")
        dt = self._find(self.disease_types, dt_id)
        if dt:
            self.disease_types.remove(dt)
            self.log("delete_disease_type", f"Deleted disease type: {dt['name']} ({dt['code']})", self._uid())

    # RESTOCK APPROVAL (admin.restock) & REQUEST (apotek.restock)
    def add_restock_request(self, user_id, medicine_id, quantity):
        req = {"id": self._next_restock_id, "user_id": user_id, "medicine_id": medicine_id,
               "quantity": quantity, "status": "pending", "approved_by": None,
               "approved_at": None, "created_at": _today()}
        self._next_restock_id += 1
        self.restock_requests.append(req)
        med_name = self.lookup_name(self.medicines, medicine_id)
        self.log("request_restock", f"Requested restock #{req['id']} for {med_name} (Qty: {quantity})", user_id)
        return req

    def process_restock(self, restock_id, action):
        restock = self._find(self.restock_requests, restock_id)
        if not restock:
            raise ValueError("Permintaan tidak ditemukan.")
        if restock["status"] != "pending":
            raise ValueError("Permintaan ini sudah diproses sebelumnya.")

        medicine = self._find(self.medicines, restock["medicine_id"])
        if action == "approve":
            restock["status"] = "approved"
            restock["approved_by"] = self._uid()
            restock["approved_at"] = _today()
            medicine["stock"] += restock["quantity"]
            self.add_transaction({
                "medicine_id": medicine["id"], "supplier_id": None, "type": "in",
                "quantity": restock["quantity"],
                "notes": f"Restock disetujui Admin. No Pengajuan: #{restock['id']}",
                "transaction_date": _today(), "user_id": self._uid(),
            }, _log=False)
            self.log("approve_restock",
                     f"Approved restock request #{restock['id']} for {medicine['name']} (Qty: {restock['quantity']})",
                     self._uid())
        elif action == "reject":
            restock["status"] = "rejected"
            restock["approved_by"] = self._uid()
            restock["approved_at"] = _today()
            self.log("reject_restock", f"Rejected restock request #{restock['id']} for {medicine['name']}", self._uid())
        else:
            raise ValueError("Aksi tidak valid.")

    # MEDICINES (apotek.medicines)
    def add_medicine(self, data):
        data["id"] = self._next_medicine_id
        self._next_medicine_id += 1
        self.medicines.append(data)
        self.log("create_medicine", f"Added new medicine: {data['name']} (#{data['code']})", self._uid())
        return data

    def update_medicine(self, medicine_id, data):
        m = self._find(self.medicines, medicine_id)
        if not m:
            raise ValueError("Obat tidak ditemukan.")
        m.update(data)
        self.log("update_medicine", f"Updated medicine: {m['name']} (#{m['code']})", self._uid())

    def delete_medicine(self, medicine_id):
        m = self._find(self.medicines, medicine_id)
        if m:
            self.medicines.remove(m)
            self.log("delete_medicine", f"Deleted medicine: {m['name']} (#{m['code']})", self._uid())

    # TRANSACTIONS (apotek.transactions)
    def add_transaction(self, data, _log=True):
        medicine = self._find(self.medicines, data["medicine_id"])
        if not medicine:
            raise ValueError("Obat tidak ditemukan.")
        if data["type"] == "out" and medicine["stock"] < data["quantity"]:
            raise ValueError("Stok obat tidak mencukupi untuk transaksi keluar ini.")

        data["id"] = self._next_transaction_id
        self._next_transaction_id += 1
        data.setdefault("user_id", self._uid())
        self.transactions.append(data)

        if data["type"] == "in":
            medicine["stock"] += data["quantity"]
        else:
            medicine["stock"] -= data["quantity"]

        if _log:
            self.log("medicine_transaction",
                     f"Recorded transaction ({data['type']}) for {medicine['name']} (Qty: {data['quantity']})",
                     data["user_id"])
        return data

    # DISEASE REPORTS (kesehatan.reports / warga.reports)
    def add_disease_report(self, data, reporter_role):
        data["id"] = self._next_report_id
        self._next_report_id += 1
        data["reporter_id"] = self._uid()
        if reporter_role == "petugas_medis":
            data["status"] = "verified"
            data["verified_by"] = self._uid()
            data["verification_notes"] = "Laporan diinput langsung oleh Petugas Kesehatan."
        else:
            data["status"] = "pending"
            data["verified_by"] = None
            data["verification_notes"] = None
        data["treatment_recommendation"] = None
        self.disease_reports.append(data)
        disease_name = self.lookup_name(self.disease_types, data["disease_type_id"])
        action = "create_disease_report" if reporter_role == "petugas_medis" else "create_disease_report_warga"
        self.log(action, f"Reported disease case: {data['patient_name']} - {disease_name}", self._uid())
        return data

    def delete_disease_report(self, report_id):
        r = self._find(self.disease_reports, report_id)
        if r:
            self.disease_reports.remove(r)
            self.log("delete_disease_report", f"Deleted disease report for {r['patient_name']}", self._uid())

    def process_verification(self, report_id, action, notes):
        report = self._find(self.disease_reports, report_id)
        if not report:
            raise ValueError("Laporan tidak ditemukan.")
        if report["status"] != "pending":
            raise ValueError("Laporan ini sudah diverifikasi sebelumnya.")

        if action == "verify":
            report["status"] = "verified"
            report["verified_by"] = self._uid()
            report["verification_notes"] = notes
            self.log("verify_disease_report",
                     f"Verified disease report #{report['id']} for patient {report['patient_name']}", self._uid())
        elif action == "reject":
            report["status"] = "rejected"
            report["verified_by"] = self._uid()
            report["verification_notes"] = notes
            self.log("reject_disease_report",
                     f"Rejected disease report #{report['id']} for patient {report['patient_name']}", self._uid())
        else:
            raise ValueError("Aksi tidak valid.")

    def add_treatment_recommendation(self, report_id, recommendation):
        report = self._find(self.disease_reports, report_id)
        if not report:
            raise ValueError("Laporan tidak ditemukan.")
        if report["status"] != "verified":
            raise ValueError("Rekomendasi penanganan hanya dapat diberikan pada laporan yang sudah terverifikasi.")
        report["treatment_recommendation"] = recommendation
        self.log("add_treatment_recommendation",
                 f"Added medical treatment recommendation for patient {report['patient_name']} (Report #{report['id']})",
                 self._uid())

    # CHILDREN (imunisasi.children)
    def add_child(self, data):
        data["id"] = self._next_child_id
        self._next_child_id += 1
        self.children.append(data)
        parent_name = self.lookup_name(self.users, data["parent_id"])
        self.log("create_child", f"Registered child: {data['name']} under parent {parent_name}", self._uid())
        return data

    def update_child(self, child_id, data):
        c = self._find(self.children, child_id)
        if not c:
            raise ValueError("Data anak tidak ditemukan.")
        c.update(data)
        self.log("update_child", f"Updated child data: {c['name']}", self._uid())

    def delete_child(self, child_id):
        c = self._find(self.children, child_id)
        if c:
            self.children.remove(c)
            self.log("delete_child", f"Deleted child data for {c['name']}", self._uid())

    # IMMUNIZATION RECORDS (imunisasi.schedules)
    def add_immunization_record(self, data):
        data["id"] = self._next_record_id
        self._next_record_id += 1
        if data["status"] != "completed":
            data["administered_date"] = None
            data["officer_id"] = None
        else:
            data["officer_id"] = self._uid()
        self.immunization_records.append(data)
        child_name = self.lookup_name(self.children, data["child_id"])
        vaccine_name = self.lookup_name(self.immunization_vaccines, data["vaccine_id"])
        self.log("schedule_immunization",
                 f"Scheduled/recorded immunization for {child_name} ({vaccine_name}) - Status: {data['status']}",
                 self._uid())
        return data

    def update_immunization_record(self, record_id, data):
        r = self._find(self.immunization_records, record_id)
        if not r:
            raise ValueError("Catatan tidak ditemukan.")
        if data["status"] == "completed":
            data["officer_id"] = self._uid()
        else:
            data["administered_date"] = None
        r.update(data)
        child_name = self.lookup_name(self.children, r["child_id"])
        self.log("update_immunization_record", f"Updated immunization record #{r['id']} for {child_name}", self._uid())

    def delete_immunization_record(self, record_id):
        r = self._find(self.immunization_records, record_id)
        if r:
            self.immunization_records.remove(r)
            child_name = self.lookup_name(self.children, r["child_id"])
            self.log("delete_immunization_record", f"Deleted immunization record #{record_id} for {child_name}", self._uid())

    # IMMUNIZATION REMINDERS (imunisasi.reminders)
    def send_reminder(self, reminder_id):
        reminder = self._find(self.immunization_reminders, reminder_id)
        if not reminder:
            raise ValueError("Reminder tidak ditemukan.")
        if reminder["status"] == "sent":
            raise ValueError("Reminder ini sudah terkirim sebelumnya.")
        reminder["status"] = "sent"
        record = self._find(self.immunization_records, reminder["record_id"])
        child_name = self.lookup_name(self.children, record["child_id"]) if record else "-"
        vaccine_name = self.lookup_name(self.immunization_vaccines, record["vaccine_id"]) if record else "-"
        self.log("send_reminder",
                 f"Sent immunization reminder (#{reminder['id']}) for {child_name} ({vaccine_name}) via {reminder['channel']}",
                 self._uid())

    # ACTIVITY LOG (admin.logs)
    def delete_log(self, log_id):
        log_item = self._find(self.activity_logs, log_id)
        if log_item:
            description = log_item["description"]
            self.activity_logs.remove(log_item)
            self.log("delete_log", f"Menghapus log aktivitas: {description}", self._uid())

    # STATISTIK DASHBOARD
    def _uid(self):
        return self.current_user["id"] if self.current_user else None

    def admin_stats(self):
        return {
            "total_users": len(self.users),
            "total_medicines": len(self.medicines),
            "low_stock_count": sum(1 for m in self.medicines if m.get("stock", 0) <= m.get("min_stock", 0)),
            "total_disease_reports": len(self.disease_reports),
            "total_children": len(self.children),
            "pending_restocks": sum(1 for r in self.restock_requests if r.get("status") == "pending"),
            "recent_logs": list(reversed(self.activity_logs))[:5],
        }

    def apoteker_stats(self):
        today = _today()
        return {
            "total_medicines": len(self.medicines),
            "total_categories": len(self.medicine_categories),
            "low_stock_count": sum(1 for m in self.medicines if m.get("stock", 0) <= m.get("min_stock", 0)),
            "expired_count": sum(1 for m in self.medicines if m.get("expiration_date", "9999-99-99") < today),
            "pending_restock_requests": sum(1 for r in self.restock_requests if r.get("status") == "pending"),
            "recent_medicines": list(reversed(self.medicines))[:5],
        }

    def petugas_medis_stats(self):
        return {
            "total_reports": len(self.disease_reports),
            "pending_reports": sum(1 for r in self.disease_reports if r.get("status") == "pending"),
            "verified_reports": sum(1 for r in self.disease_reports if r.get("status") == "verified"),
            "recent_reports": list(reversed(self.disease_reports))[:5],
            "severity_stats": {
                "ringan": sum(1 for r in self.disease_reports if r.get("severity") == "ringan"),
                "sedang": sum(1 for r in self.disease_reports if r.get("severity") == "sedang"),
                "berat": sum(1 for r in self.disease_reports if r.get("severity") == "berat"),
            },
        }

    def warga_stats(self, user_id):
        my_reports = [r for r in self.disease_reports if r.get("reporter_id") == user_id]
        my_children = [c for c in self.children if c.get("parent_id") == user_id]
        return {
            "total_reports": len(my_reports),
            "total_children": len(my_children),
            "recent_reports": list(reversed(my_reports))[:5],
        }

store = DataStore()