class Customer:
    
    # Define the parameterized constructor here
    def __init__(self, customer_id, name, email, phone):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__phone = phone

    # --- Setters (optional, if you need to modify fields later) ---
    def set_customer_id(self, value): self.__customer_id = value
    def set_name(self, value): self.__name = value
    def set_email(self, value): self.__email = value
    def set_phone(self, value): self.__phone = value

    # --- Getters (useful for insertion/printing) ---
    def get_customer_id(self): return self.__customer_id
    def get_name(self): return self.__name
    def get_email(self): return self.__email
    def get_phone(self): return self.__phone

    def __repr__(self):
        return (f"Customer(customer_id={self.__customer_id}, name='{self.__name}', "
                f"email='{self.__email}', phone='{self.__phone}')")