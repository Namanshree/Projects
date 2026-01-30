import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'parking_db'
}

# --- Theme Setup ---
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

class ParkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("SmartSlot - Parking Management System")
        self.geometry("1100x600")
        
        # Database Connection
        self.conn = self.connect_db()
        self.cursor = self.conn.cursor()

        # UI Layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_parking_grid()
        
        # Initial Data Load
        self.refresh_grid()

    def connect_db(self):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Could not connect to database: {err}")
            exit()

    def create_sidebar(self):
        # Create Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🚗 SmartSlot", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs
        self.entry_name = ctk.CTkEntry(self.sidebar, placeholder_text="Owner Name")
        self.entry_name.grid(row=1, column=0, padx=20, pady=10)

        self.entry_vehicle = ctk.CTkEntry(self.sidebar, placeholder_text="Vehicle Number (e.g., AB-1234)")
        self.entry_vehicle.grid(row=2, column=0, padx=20, pady=10)

        # Park Button
        self.btn_park = ctk.CTkButton(self.sidebar, text="Park Vehicle", command=self.park_vehicle, fg_color="#2CC985", hover_color="#229A65")
        self.btn_park.grid(row=3, column=0, padx=20, pady=20)

        # Stats Label
        self.stats_label = ctk.CTkLabel(self.sidebar, text="Available: 50/50", font=ctk.CTkFont(size=16))
        self.stats_label.grid(row=4, column=0, padx=20, pady=20)

        # Instructions
        instruction_text = "Click a RED slot to\nview details or depart."
        self.lbl_instruct = ctk.CTkLabel(self.sidebar, text=instruction_text, text_color="gray")
        self.lbl_instruct.grid(row=5, column=0, padx=20, pady=(50, 10))

    def create_parking_grid(self):
        # Main Area Frame
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Live Parking Lot Status")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # We will create a list to store button references
        self.slot_buttons = {}

        # Create 50 buttons in a grid (5 columns x 10 rows)
        for i in range(1, 51):
            btn = ctk.CTkButton(
                self.main_frame,
                text=f"Slot {i}",
                width=100,
                height=60,
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            # Calculate grid position
            row = (i - 1) // 5
            col = (i - 1) % 5
            btn.grid(row=row, column=col, padx=10, pady=10)
            
            # Store button with ID for later updates
            self.slot_buttons[i] = btn

    def refresh_grid(self):
        """Fetches data from MySQL and updates the colors/commands of buttons."""
        self.cursor.execute("SELECT * FROM parking_slots")
        rows = self.cursor.fetchall()
        
        occupied_count = 0

        for row in rows:
            slot_id = row[0]
            status = row[1]
            owner = row[2]
            vehicle = row[3]

            btn = self.slot_buttons[slot_id]

            if status == 'Occupied':
                occupied_count += 1
                # Red color for occupied, click to show details
                btn.configure(
                    fg_color="#FF4757", 
                    hover_color="#C0392B", 
                    command=lambda s=slot_id, o=owner, v=vehicle: self.show_slot_details(s, o, v)
                )
            else:
                # Green color for available, click does nothing (or could auto-fill slot)
                btn.configure(
                    fg_color="#2ED573", 
                    hover_color="#26AF61",
                    command=lambda: None
                )
        
        # Update Dashboard Stats
        available = 50 - occupied_count
        self.stats_label.configure(text=f"Available: {available}/50")

    def park_vehicle(self):
        name = self.entry_name.get()
        vehicle = self.entry_vehicle.get()

        if not name or not vehicle:
            messagebox.showwarning("Input Error", "Please enter Name and Vehicle Number")
            return

        # Find first available slot
        self.cursor.execute("SELECT slot_id FROM parking_slots WHERE status='Available' LIMIT 1")
        result = self.cursor.fetchone()

        if result:
            slot_id = result[0]
            # Update DB
            query = "UPDATE parking_slots SET status='Occupied', owner_name=%s, vehicle_number=%s WHERE slot_id=%s"
            self.cursor.execute(query, (name, vehicle, slot_id))
            self.conn.commit()
            
            # Clear inputs and refresh UI
            self.entry_name.delete(0, 'end')
            self.entry_vehicle.delete(0, 'end')
            self.refresh_grid()
            messagebox.showinfo("Success", f"Vehicle Parked at Slot {slot_id}")
        else:
            messagebox.showerror("Full", "Sorry, Parking is Full!")

    def show_slot_details(self, slot_id, owner, vehicle):
        """Creates a popup with details and option to Unpark."""
        
        # Custom Dialog/Popup logic
        info_msg = f"Slot: {slot_id}\nOwner: {owner}\nVehicle: {vehicle}"
        
        # We ask if they want to unpark (Exit)
        response = messagebox.askyesno("Slot Details", f"{info_msg}\n\nDo you want to clear this slot (Departure)?")
        
        if response: # If User clicks 'Yes'
            self.depart_vehicle(slot_id)

    def depart_vehicle(self, slot_id):
        query = "UPDATE parking_slots SET status='Available', owner_name=NULL, vehicle_number=NULL WHERE slot_id=%s"
        self.cursor.execute(query, (slot_id,))
        self.conn.commit()
        self.refresh_grid()
        messagebox.showinfo("Departed", f"Slot {slot_id} is now free.")

if __name__ == "__main__":
    app = ParkingApp()
    app.mainloop()
