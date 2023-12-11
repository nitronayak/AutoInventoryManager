import sqlite3
import csv
from tkinter import Tk, filedialog, messagebox, Label, Entry, Button
from tkinter.ttk import Style

# Connect to the database
conn = sqlite3.connect('automotive_inventory.db')
c = conn.cursor()

# Create the inventory table
c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              make TEXT,
              model TEXT,
              year INTEGER,
              price REAL,
              VIN TEXT)''')

# Create the buyers table
c.execute('''CREATE TABLE IF NOT EXISTS buyers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              price REAL,
              credit_score INTEGER,
              payment_type TEXT,
              VIN TEXT)''')

# Create the repairs table
c.execute('''CREATE TABLE IF NOT EXISTS repairs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              ticket_id INTEGER,
              model TEXT,
              problem TEXT,
              repair_cost REAL,
              VIN TEXT)''')

# Function to add a car to the inventory
def add_car(make, model, year, price, vin):
    c.execute("INSERT INTO inventory (make, model, year, price, VIN) VALUES (?, ?, ?, ?,?)",
              (make, model, year, price, vin))
    conn.commit()
    messagebox.showinfo("Success", "Car added successfully.")

# Function to remove a car from the inventory
def remove_car(car_id):
    c.execute("DELETE FROM inventory WHERE id=?", (car_id,))
    conn.commit()
    messagebox.showinfo("Success", "Car removed successfully.")

# Function to display all cars in the inventory
def display_inventory():
    c.execute("SELECT * FROM inventory")
    cars = c.fetchall()
    if len(cars) == 0:
        messagebox.showinfo("Inventory", "Inventory is empty.")
    else:
        inventory_text = "ID\tMake\tModel\tYear\tPrice\tVIN\n"
        for car in cars:
            inventory_text += f"{car[0]}\t{car[1]}\t{car[2]}\t{car[3]}\t{car[4]}\t{car[5]}\n"
        messagebox.showinfo("Inventory", inventory_text)

# Function to add a buyer
def add_buyer(name, price, credit_score, payment_type, vin):
    c.execute("INSERT INTO buyers (name, price, credit_score, payment_type, VIN) VALUES (?, ?, ?, ?,?)",
              (name, price, credit_score, payment_type,vin))
    conn.commit()
    messagebox.showinfo("Success", "Buyer added successfully.")

# Function to remove a buyer
def remove_buyer(buyer_id):
    c.execute("DELETE FROM buyers WHERE id=?", (buyer_id,))
    conn.commit()
    messagebox.showinfo("Success", "Buyer removed successfully.")

# Function to display all buyers
def display_buyers():
    c.execute("SELECT * FROM buyers")
    buyers = c.fetchall()
    if len(buyers) == 0:
        messagebox.showinfo("Buyers", "No buyers found.")
    else:
        buyers_text = "ID\tName\tPrice\tCredit Score\tPayment Type\tVIN\n"
        for buyer in buyers:
            buyers_text += f"{buyer[0]}\t{buyer[1]}\t{buyer[2]}\t{buyer[3]}\t{buyer[4]}\t{buyer[5]}\n"
        messagebox.showinfo("Buyers", buyers_text)

# Function to add a repair
def add_repair(ticket_id, model, problem, repair_cost, vin):
    c.execute("INSERT INTO repairs (ticket_id, model, problem, repair_cost, VIN) VALUES (?, ?, ?, ?,?)",
              (ticket_id, model, problem, repair_cost,vin))
    conn.commit()
    messagebox.showinfo("Success", "Repair added successfully.")

# Function to remove a repair
def remove_repair(repair_id):
    c.execute("DELETE FROM repairs WHERE id=?", (repair_id,))
    conn.commit()
    messagebox.showinfo("Success", "Repair removed successfully.")

# Function to display all repairs
def display_repairs():
    c.execute("SELECT * FROM repairs")
    repairs = c.fetchall()
    if len(repairs) == 0:
        messagebox.showinfo("Repairs", "No repairs found.")
    else:
        repairs_text = "ID\tTicket ID\tModel\tProblem\tRepair Cost\n"
        for repair in repairs:
            repairs_text += f"{repair[0]}\t{repair[1]}\t{repair[2]}\t{repair[3]}\t{repair[4]}\t{repair[5]}\n"
        messagebox.showinfo("Repairs", repairs_text)

# Function to import cars from a CSV file
def import_csv():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(title="Select CSV file")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            make, model, year, price, vin = row
            add_car(make, model, int(year), float(price), vin)
    messagebox.showinfo("Success", "CSV file imported successfully.")

# VIN lookup function
def lookup_vin(vin):
    c.execute("SELECT * FROM inventory WHERE VIN = ?", (vin,))
    cars = c.fetchall()

    c.execute("SELECT * FROM buyers WHERE VIN = ?", (vin,))
    buyers = c.fetchall()

    c.execute("SELECT * FROM repairs WHERE VIN = ?", (vin,))
    repairs = c.fetchall()

    return cars, buyers, repairs

# Close the database connection
def close_connection():
    conn.close()
    messagebox.showinfo("Success", "Database connection closed.")

# Password verification function
def verify_password(password):
    # Replace 'password' with your desired password
    return password == 'password'

# Main program loop, with password verification and GUI setup
password = input("Enter the password: ")
if verify_password(password):
    root = Tk()
    root.title("Automotive Inventory")
    root.geometry("1000x800")  # Set window dimensions
    style = Style()
    style.configure("TButton", font=("Bahnschrift", 12), background="#333", foreground="#fff")
    style.configure("TLabel", font=("Bahnschrift", 12), background="#333", foreground="#fff")
    style.configure("TEntry", font=("Bahnschrift", 12), background="#555", foreground="#fff")

#Dialogs and their design
    def add_car_dialog():
        dialog = Tk()
        dialog.title("Add Car")
        dialog.geometry("300x300")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        make_label = Label(dialog, text="Make:", background="black", foreground="#fff")
        make_label.pack()
        make_entry = Entry(dialog, background="#555", foreground="#fff")
        make_entry.pack()

        model_label = Label(dialog, text="Model:", background="black", foreground="#fff")
        model_label.pack()
        model_entry = Entry(dialog, background="#555", foreground="#fff")
        model_entry.pack()

        year_label = Label(dialog, text="Year:", background="black", foreground="#fff")
        year_label.pack()
        year_entry = Entry(dialog, background="#555", foreground="#fff")
        year_entry.pack()

        price_label = Label(dialog, text="Price:", background="black", foreground="#fff")
        price_label.pack()
        price_entry = Entry(dialog, background="#555", foreground="#fff")
        price_entry.pack()

        vin_label = Label(dialog, text="VIN:", background="black", foreground="#fff")
        vin_label.pack()
        vin_entry = Entry(dialog, background="#555", foreground="#fff")
        vin_entry.pack()

        add_button = Button(dialog, text="Add", command=lambda: add_car(make_entry.get(), model_entry.get(), int(year_entry.get()), float(price_entry.get()), vin_entry.get()), background="#555", foreground="#fff")
        add_button.pack()

        dialog.mainloop()

    def remove_car_dialog():
        dialog = Tk()
        dialog.title("Remove Car")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        car_id_label = Label(dialog, text="Car ID:", background="black", foreground="#fff")
        car_id_label.pack()
        car_id_entry = Entry(dialog, background="#555", foreground="#fff")
        car_id_entry.pack()

        remove_button = Button(dialog, text="Remove", command=lambda: remove_car(int(car_id_entry.get())), background="#555", foreground="#fff")
        remove_button.pack()

        dialog.mainloop()

    def display_inventory_dialog():
        display_inventory()

    def import_csv_dialog():
        import_csv()

    def close_connection_dialog():
        close_connection()
        root.destroy()

    def add_buyer_dialog():
        dialog = Tk()
        dialog.title("Add Buyer")
        dialog.geometry("300x300")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        name_label = Label(dialog, text="Name:", background="black", foreground="#fff")
        name_label.pack()
        name_entry = Entry(dialog, background="#555", foreground="#fff")
        name_entry.pack()

        price_label = Label(dialog, text="Price:", background="black", foreground="#fff")
        price_label.pack()
        price_entry = Entry(dialog, background="#555", foreground="#fff")
        price_entry.pack()

        credit_score_label = Label(dialog, text="Credit Score:", background="black", foreground="#fff")
        credit_score_label.pack()
        credit_score_entry = Entry(dialog, background="#555", foreground="#fff")
        credit_score_entry.pack()

        payment_type_label = Label(dialog, text="Payment Type:", background="black", foreground="#fff")
        payment_type_label.pack()
        payment_type_entry = Entry(dialog, background="#555", foreground="#fff")
        payment_type_entry.pack()

        vin_label = Label(dialog, text="VIN:", background="black", foreground="#fff")
        vin_label.pack()
        vin_entry = Entry(dialog, background="#555", foreground="#fff")
        vin_entry.pack()

        add_button = Button(dialog, text="Add", command=lambda: add_buyer(name_entry.get(), float(price_entry.get()), int(credit_score_entry.get()), payment_type_entry.get(), vin_entry.get()), background="#555", foreground="#fff")
        add_button.pack()

        dialog.mainloop()

    def remove_buyer_dialog():
        dialog = Tk()
        dialog.title("Remove Buyer")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        buyer_id_label = Label(dialog, text="Buyer ID:", background="black", foreground="#fff")
        buyer_id_label.pack()
        buyer_id_entry = Entry(dialog, background="#555", foreground="#fff")
        buyer_id_entry.pack()

        remove_button = Button(dialog, text="Remove", command=lambda: remove_buyer(int(buyer_id_entry.get())), background="#555", foreground="#fff")
        remove_button.pack()

        dialog.mainloop()

    def display_buyers_dialog():
        display_buyers()

    def add_repair_dialog():
        dialog = Tk()
        dialog.title("Add Repair")
        dialog.geometry("300x300")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        ticket_id_label = Label(dialog, text="Ticket ID:", background="black", foreground="#fff")
        ticket_id_label.pack()
        ticket_id_entry = Entry(dialog, background="#555", foreground="#fff")
        ticket_id_entry.pack()

        model_label = Label(dialog, text="Model:", background="black", foreground="#fff")
        model_label.pack()
        model_entry = Entry(dialog, background="#555", foreground="#fff")
        model_entry.pack()

        problem_label = Label(dialog, text="Problem:", background="black", foreground="#fff")
        problem_label.pack()
        problem_entry = Entry(dialog, background="#555", foreground="#fff")
        problem_entry.pack()

        repair_cost_label = Label(dialog, text="Repair Cost:", background="black", foreground="#fff")
        repair_cost_label.pack()
        repair_cost_entry = Entry(dialog, background="#555", foreground="#fff")
        repair_cost_entry.pack()

        vin_label = Label(dialog, text="VIN:", background="black", foreground="#fff")
        vin_label.pack()
        vin_entry = Entry(dialog, background="#555", foreground="#fff")
        vin_entry.pack()

        add_button = Button(dialog, text="Add", command=lambda: add_repair(int(ticket_id_entry.get()), model_entry.get(), problem_entry.get(), float(repair_cost_entry.get()), vin_entry.get()), background="#555", foreground="#fff")
        add_button.pack()

        dialog.mainloop()

    def remove_repair_dialog():
        dialog = Tk()
        dialog.title("Remove Repair")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        repair_id_label = Label(dialog, text="Repair ID:", background="black", foreground="#fff")
        repair_id_label.pack()
        repair_id_entry = Entry(dialog, background="#555", foreground="#fff")
        repair_id_entry.pack()

        remove_button = Button(dialog, text="Remove", command=lambda: remove_repair(int(repair_id_entry.get())), background="#555", foreground="#fff")
        remove_button.pack()

        dialog.mainloop()

    def display_repairs_dialog():
        display_repairs()

    def vin_lookup_dialog():
        dialog = Tk()
        dialog.title("VIN Lookup")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(background="black")

        vin_label = Label(dialog, text="VIN:", background="black", foreground="#fff")
        vin_label.pack()
        vin_entry = Entry(dialog, background="#555", foreground="#fff")
        vin_entry.pack()

        def lookup_and_display():
            cars, buyers, repairs = lookup_vin(vin_entry.get())
            # Format and display the results
            result_text = "Cars:\n" + "\n".join(map(str, cars)) + "\n\nBuyers:\n" + "\n".join(map(str, buyers)) + "\n\nRepairs:\n" + "\n".join(map(str, repairs))
            messagebox.showinfo("VIN Lookup Results", result_text)

        lookup_button = Button(dialog, text="Lookup", command=lookup_and_display, background="#555", foreground="#fff")
        lookup_button.pack()

        dialog.mainloop()
    

#Buttons and their design
    add_car_button = Button(root, text="Add a car to the inventory", command=add_car_dialog, font=("Bahnschrift", 16))
    add_car_button.pack(pady=10)

    remove_car_button = Button(root, text="Remove a car from the inventory", command=remove_car_dialog, font=("Bahnschrift", 16))
    remove_car_button.pack(pady=10)

    display_inventory_button = Button(root, text="Display inventory", command=display_inventory_dialog, font=("Bahnschrift", 16))
    display_inventory_button.pack(pady=10)

    import_csv_button = Button(root, text="Import cars from CSV", command=import_csv_dialog, font=("Bahnschrift", 16))
    import_csv_button.pack(pady=10)

    add_buyer_button = Button(root, text="Add a buyer", command=add_buyer_dialog, font=("Bahnschrift", 16))
    add_buyer_button.pack(pady=10)

    remove_buyer_button = Button(root, text="Remove a buyer", command=remove_buyer_dialog, font=("Bahnschrift", 16))
    remove_buyer_button.pack(pady=10)

    display_buyers_button = Button(root, text="Display buyers", command=display_buyers_dialog, font=("Bahnschrift", 16))
    display_buyers_button.pack(pady=10)

    add_repair_button = Button(root, text="Add a repair", command=add_repair_dialog, font=("Bahnschrift", 16))
    add_repair_button.pack(pady=10)

    remove_repair_button = Button(root, text="Remove a repair", command=remove_repair_dialog, font=("Bahnschrift", 16))
    remove_repair_button.pack(pady=10)

    display_repairs_button = Button(root, text="Display repairs", command=display_repairs_dialog, font=("Bahnschrift", 16))
    display_repairs_button.pack(pady=10)

    vin_lookup_button = Button(root, text="VIN Lookup", command=vin_lookup_dialog, font=("Bahnschrift", 16))
    vin_lookup_button.pack(pady=10)

    exit_button = Button(root, text="Exit", command=close_connection_dialog, font=("Bahnschrift", 16))
    exit_button.pack(pady=10)

    root.configure(background="black")
    root.mainloop()
else:
    print("Invalid password. Please try again.")
