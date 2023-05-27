class User:
    def __init__(self, fname, mname, ltname, phone_no, encrypted_pass, dob, isAdmin):
        self._fname = fname
        self._mname = mname
        self._ltname = ltname
        self._phone_no = phone_no
        self._encrypted_pass = encrypted_pass
        self._dob = dob
        self._isAdmin = isAdmin

    # Getters
    def get_fname(self):
        return self._fname

    def get_mname(self):
        return self._mname

    def get_ltname(self):
        return self._ltname

    def get_phone_no(self):
        return self._phone_no

    def get_encrypted_pass(self):
        return self._encrypted_pass

    def get_dob(self):
        return self._dob

    def is_admin(self):
        return self._isAdmin

    # Setters
    def set_fname(self, fname):
        self._fname = fname

    def set_mname(self, mname):
        self._mname = mname

    def set_ltname(self, ltname):
        self._ltname = ltname

    def set_phone_no(self, phone_no):
        self._phone_no = phone_no

    def set_encrypted_pass(self, encrypted_pass):
        self._encrypted_pass = encrypted_pass

    def set_dob(self, dob):
        self._dob = dob

    def set_is_admin(self, isAdmin):
        self._isAdmin = isAdmin
        
    def update_profile(self):
        print("Enter new profile information (leave blank to keep existing values):")
        fname = input("First name: ")
        if fname:
            self._fname = fname

        mname = input("Middle name: ")
        if mname:
            self._mname = mname

        ltname = input("Last name: ")
        if ltname:
            self._ltname = ltname

        phone_no = input("Phone number: ")
        if phone_no:
            self._phone_no = phone_no

        
        encrypted_pass = input("Encrypted password: ")
        if encrypted_pass:
            self._encrypted_pass = encrypted_pass

        dob = input("Date of birth (YYYY-MM-DD): ")
        if dob:
            self._dob = dob

