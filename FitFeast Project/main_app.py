import customtkinter as ctk
from tkinter import messagebox
try:
    from backend import FitnessLogic
except ImportError:
    FitnessLogic = None
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FitFeast(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Window UI Setup
        self.title("FitFeast - Smart Planner")
        self.geometry("1100x850")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Connect to Database
        self.logic = None
        if FitnessLogic:
            try:
                self.logic = FitnessLogic()
            except Exception as e:
                messagebox.showerror("Database Connection Error", 
                                     f"Could not connect to MySQL.\n\nCheck your password in 'backend.py'.\n\nError details: {str(e)}")
        else:
             messagebox.showerror("Module Error", "Could not import backend.py")

        # 3. Build UI
        self.create_input_frame()

    def create_input_frame(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title
        ctk.CTkLabel(self.input_frame, text="FitFeast: Smart Planner", font=("Roboto", 28, "bold")).pack(pady=15)
        ctk.CTkLabel(self.input_frame, text="Customize your Diet & Workout", font=("Roboto", 14), text_color="gray").pack(pady=(0, 20))

        # --- NUMERIC INPUTS ---
        input_grid = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_grid.pack(pady=10)
        
        # Weight
        self.weight_entry = ctk.CTkEntry(input_grid, placeholder_text="Weight (kg)", width=140)
        self.weight_entry.grid(row=0, column=0, padx=10, pady=10)
        
        # Height
        self.height_entry = ctk.CTkEntry(input_grid, placeholder_text="Height (cm)", width=140)
        self.height_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Age
        self.age_entry = ctk.CTkEntry(input_grid, placeholder_text="Age (Years)", width=140)
        self.age_entry.grid(row=0, column=2, padx=10, pady=10)

        # --- BUTTON SELECTIONS ---
        
        # Gender
        ctk.CTkLabel(self.input_frame, text="Select Gender:", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        self.gender_var = ctk.CTkSegmentedButton(self.input_frame, values=["Male", "Female"], width=200)
        self.gender_var.set("Male")
        self.gender_var.pack(pady=5)

        # Body Type
        ctk.CTkLabel(self.input_frame, text="Select Body Type:", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.body_type_var = ctk.CTkSegmentedButton(self.input_frame, values=["Skinny", "Average", "Overweight"], 
                                                    selected_color="#10b981", selected_hover_color="#059669")
        self.body_type_var.set("Average")
        self.body_type_var.pack(pady=5)

        # Goal
        ctk.CTkLabel(self.input_frame, text="Select Your Goal:", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.goal_var = ctk.CTkSegmentedButton(self.input_frame, values=["Lose Weight", "Gain Weight", "Maintain"],
                                               selected_color="#3b82f6", selected_hover_color="#2563eb")
        self.goal_var.set("Maintain")
        self.goal_var.pack(pady=5)

        # Diet Preference
        ctk.CTkLabel(self.input_frame, text="Diet Preference:", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.diet_pref_var = ctk.CTkSegmentedButton(self.input_frame, values=["Veg", "Non-Veg", "Both"],
                                                    selected_color="#f59e0b", selected_hover_color="#d97706")
        self.diet_pref_var.set("Veg")
        self.diet_pref_var.pack(pady=5)

        # Workout Location
        ctk.CTkLabel(self.input_frame, text="Workout Setup:", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.workout_loc_var = ctk.CTkSegmentedButton(self.input_frame, values=["Home Workout", "Gym Workout"])
        self.workout_loc_var.set("Home Workout")
        self.workout_loc_var.pack(pady=5)

        # Generate Button
        ctk.CTkButton(self.input_frame, text="GENERATE MY PLAN", command=self.generate_plan, 
                      height=50, width=300, font=("Roboto", 18, "bold"), fg_color="#ef4444", hover_color="#dc2626").pack(pady=30)

    def generate_plan(self):
        # 1. CONNECTION CHECK
        if self.logic is None:
            messagebox.showerror("Connection Error", "Database is not connected.\nPlease check the password in backend.py and restart.")
            return

        # 2. ERROR HANDLING: Input Validation with LIMITATIONS
        try:
            w_val = self.weight_entry.get()
            h_val = self.height_entry.get()
            a_val = self.age_entry.get()

            # Check for empty strings
            if not w_val or not h_val or not a_val:
                raise ValueError("All fields (Weight, Height, Age) are required.")

            w = float(w_val)
            h = float(h_val)
            a = int(a_val)
            
            # --- Input Limits ---
            if not (13 <= a <= 100):
                raise ValueError("Age must be between 13 and 100 years.")
            
            if not (50 <= h <= 250):
                raise ValueError("Height must be between 50 cm and 250 cm.")
                
            if not (20 <= w <= 300):
                raise ValueError("Weight must be between 20 kg and 300 kg.")
            # ----------------------------------

        except ValueError as e:
            if "must be between" in str(e) or "required" in str(e):
                messagebox.showerror("Input Error", str(e))
            else:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        # 3. LOGIC EXECUTION
        goal = self.goal_var.get()
        loc = self.workout_loc_var.get()
        pref = self.diet_pref_var.get()
        gender = self.gender_var.get()
        body_type = self.body_type_var.get()

        try:
            calories = self.logic.calculate_bmr_calories(w, h, a, gender, "Moderately Active", goal, body_type)
            weekly_diet = self.logic.generate_weekly_diet(pref)
            weekly_workout = self.logic.get_weekly_workout(loc.split()[0], goal, body_type)

            self.input_frame.destroy()
            self.show_results(calories, weekly_diet, weekly_workout, body_type)
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred while generating: {e}")

    def show_results(self, calories, diet, workout, body_type):
        self.res_frame = ctk.CTkFrame(self)
        self.res_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Top Bar
        top_frame = ctk.CTkFrame(self.res_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"Plan: {body_type} Body • Target: {calories} kcal/day"
        ctk.CTkLabel(top_frame, text=info_text, font=("Roboto", 20, "bold"), text_color="#4ade80").pack(side="left")
        ctk.CTkButton(top_frame, text="Reset", command=self.reset_app, width=100, fg_color="#ef4444").pack(side="right")

        # Tabs
        self.tab_view = ctk.CTkTabview(self.res_frame, width=1000, height=600)
        self.tab_view.pack(padx=20, pady=10, fill="both", expand=True)
        
        tab_diet = self.tab_view.add("Weekly Diet")
        tab_work = self.tab_view.add("Weekly Workout")
        tab_stats = self.tab_view.add("Macro Stats")

        # --- TAB 1: DIET ---
        scroll_diet = ctk.CTkScrollableFrame(tab_diet, width=900, height=500)
        scroll_diet.pack(fill="both", expand=True)
        
        for day, meals in diet.items():
            day_frame = ctk.CTkFrame(scroll_diet)
            day_frame.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(day_frame, text=day, font=("Roboto", 16, "bold"), text_color="#60a5fa").pack(anchor="w", padx=10, pady=5)
            
            day_text = ""
            for m_name, m_data in meals.items():
                day_text += f"  {m_name}: {m_data[0]} ({m_data[1]} kcal, {m_data[2]}g pro)\n"
            
            ctk.CTkLabel(day_frame, text=day_text, justify="left", font=("Consolas", 12)).pack(anchor="w", padx=10)

        # --- TAB 2: WORKOUT ---
        scroll_work = ctk.CTkScrollableFrame(tab_work, width=900, height=500)
        scroll_work.pack(fill="both", expand=True)
        
        for day, exercise in workout.items():
            row = ctk.CTkFrame(scroll_work)
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=f"{day}:", font=("Roboto", 16, "bold"), width=50, text_color="#fbbf24").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=exercise, font=("Roboto", 14)).pack(side="left", padx=10)

        # --- TAB 3: VISUALIZATION ---
        sample_day = diet["Monday"]
        total_pro = sum([m[2] for m in sample_day.values()])
        total_cals = sum([m[1] for m in sample_day.values()])
        
        if body_type == "Skinny":
            carb_ratio, fat_ratio = 0.55, 0.45
        elif body_type == "Overweight":
            carb_ratio, fat_ratio = 0.40, 0.60
        else:
            carb_ratio, fat_ratio = 0.50, 0.50

        remaining_cals = total_cals - (total_pro * 4)
        approx_carbs = max(0, (remaining_cals * carb_ratio) / 4)
        approx_fats = max(0, (remaining_cals * fat_ratio) / 9)

        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2b2b2b')
        ax.pie([total_pro, approx_carbs, approx_fats], labels=['Protein', 'Carbs', 'Fats'], 
               autopct='%1.1f%%', colors=['#4ade80', '#60a5fa', '#f87171'], textprops={'color':"white"})
        ax.set_title(f"Approx Macro Split for {body_type} Body", color='white')

        canvas = FigureCanvasTkAgg(fig, master=tab_stats)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def reset_app(self):
        self.res_frame.destroy()
        self.create_input_frame()

if __name__ == "__main__":
    app = FitFeast()
    app.mainloop()
