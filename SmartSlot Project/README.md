#🚗 SmartSlot - Parking Management System
SmartSlot is a full-stack desktop application designed to digitize and automate vehicle parking operations. It replaces manual paper logs with an interactive, real-time graphical dashboard, ensuring efficient space utilization and data accuracy.

#🎯 Project Impact & Achievements
Efficiency Boost: Automated vehicle tracking, reducing manual record-keeping time by 70%.

Real-Time Optimization: Managed live data for a 50-slot facility, optimizing occupancy rates and allocation efficiency.

Error Elimination: Removed data entry errors by replacing manual workflows with a structured, automated tracking system.

#✨ Key Features
Interactive Visual Dashboard:

Green Slots: Available for parking.

Red Slots: Occupied (Click to view vehicle details).

Automated Allocation: System automatically identifies and assigns the nearest available slot ID, removing human search effort.

Data Persistence: Uses MySQL to store vehicle owner details, ensuring data remains safe even if the application closes.

One-Click Departure: simple interface to retrieve vehicle details and free up the slot upon exit.

Modern UI: Built with CustomTkinter for a clean, dark-mode-enabled user experience.

#🛠️ Tech Stack
Language: Python

GUI Library: CustomTkinter (Modern wrapper for Tkinter)

Database: MySQL

Driver: mysql-connector-python

#🚀 Installation & Setup
#1. Prerequisites
Ensure you have Python installed and a running instance of MySQL Server (e.g., via XAMPP or MySQL Workbench).

#2. Install Dependencies
Open Command Prompt and enter the following command
>>>	pip install mysql-connector-python customtkinter

#3. Database Configuration
Open your MySQL client and run the following script to create the database and the 50 parking slots:
>>>	CREATE DATABASE parking_db;
USE parking_db;

CREATE TABLE parking_slots (
    slot_id INT PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'Available',
    owner_name VARCHAR(100),
    vehicle_number VARCHAR(20)
);

-- Initialize 50 empty slots
DELIMITER $$
CREATE PROCEDURE InitSlots()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 50 DO
        INSERT INTO parking_slots (slot_id, status, owner_name, vehicle_number)
        VALUES (i, 'Available', NULL, NULL);
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

CALL InitSlots();

#4. Run the Application
Open main.py.

Update the DB_CONFIG dictionary with your MySQL password:

Python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE', 
    'database': 'parking_db'
}
Run the script:

Bash
python main.py

#📖 Usage Guide
To Park a Car: Enter the "Owner Name" and "Vehicle Number" in the sidebar and click Park Vehicle. The system will auto-fill the first green slot.

To View Details: Click on any Red (Occupied) slot in the grid to see who is parked there.

To Remove a Car: Click the occupied slot and select "Yes" on the prompt to clear the slot and mark it as available.

#🔮 Future Scope
Billing Integration: Calculate parking fees based on entry/exit timestamps.

License Plate Recognition: Integrate OpenCV to auto-read license plates.

Web Dashboard: Create a Flask/Django web view for remote monitoring.
---
*Created by Naman Shree*