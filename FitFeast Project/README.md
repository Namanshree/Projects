# FitFeast: The Smart Indian Fitness Planner 🏋️‍♂️🍛

**FitFeast** is a full-stack desktop application designed to generate personalized, affordable diet plans and workout routines tailored specifically for the Indian lifestyle. Unlike generic fitness apps, FitFeast accounts for local dietary habits, affordability, and specific body types.

## 🚀 Key Features

### 🧠 Smart Logic & Personalization
* **Body Type Adaptation:** The algorithm adjusts TDEE (Total Daily Energy Expenditure) based on metabolism estimates for **Skinny** (Fast Metabolism) vs. **Overweight** (Slow Metabolism) body types.
* **Custom BMR Calculation:** Uses the **Mifflin-St Jeor Equation**, widely considered the most accurate standard for caloric estimation.
* **Dynamic Goal Setting:** Supports Weight Loss, Muscle Gain, and Maintenance, automatically adjusting caloric surplus or deficit.

### 🍛 Indian & Affordable Diet
* **Context-Aware Database:** The SQL database is populated with affordable Indian meals (Poha, Dal Tadka, Soya Chunks) rather than expensive western ingredients.
* **Dietary Preferences:** Filters for **Veg**, **Non-Veg**, or **Both**.

### 🛡️ Robustness & UX
* **Input Validation:** Strictly checks for realistic inputs (Age: 13-100, Height: 50-250cm, Weight: 20-300kg) to prevent calculation errors.
* **Smart Error Handling:** Instead of crashing, the app provides helpful popup alerts if the database connection fails or inputs are invalid.
* **Visual Analytics:** Generates an interactive Pie Chart using `Matplotlib` to visualize the Protein/Carb/Fat breakdown.

## 🛠 Tech Stack
* **Frontend:** Python (`CustomTkinter`) - *Chosen for a modern, high-DPI aware dark-mode UI.*
* **Backend:** Python - *Handles metabolic math, logic branching, and error handling.*
* **Database:** MySQL - *Stores nutritional data and exercise libraries.*
* **Visualization:** Matplotlib - *Renders real-time macro analytics.*

## ⚙️ How It Works (The Logic)
1.  **User Input:** The user selects Age, Weight, Height, Gender, Goal, and **Body Type**.
2.  **Caloric Calculation:**
    * Calculates Base BMR.
    * Applies Activity Multiplier.
    * **Metabolic Correction:** Adds a calorie buffer for "Skinny" users (high NEAT) or a slight reduction for "Overweight" users.
3.  **Plan Generation:**
    * **Diet:** Queries the MySQL database to build a randomized 7-day meal plan matching the calorie target.
    * **Workout:** Generates a split based on location (Gym/Home) and Body Type (e.g., "Skinny" users get Heavy Compound movements; "Overweight" users get Metabolic Conditioning).
4.  **Visualization:** Renders the macro-nutrient split on the "Stats" tab.

## 📂 Project Structure
```text
FitFeast/
│
├── main_app.py        # The GUI (CustomTkinter) & Main Loop
├── backend.py         # The Logic Class & Database Connectivity
├── db_setup.sql       # SQL Script to seed Food & Exercise data
└── README.md          # Project Documentation

## 🔧 Setup Instructions
1.  Install dependencies: `pip install customtkinter mysql-connector-python matplotlib`
2.  Import `db_setup.sql` into your local MySQL server.
3.  Update `backend.py` with your MySQL root password.
4.  Run `python main_app.py`.

---
*Created by Naman Shree*