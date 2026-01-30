import mysql.connector
import random

class FitnessLogic:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user="root", password="root", database="fitfeast"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            raise Exception(f"Database Connection Failed: {err}")

    def calculate_bmr_calories(self, weight, height, age, gender, activity, goal, body_type):
        # 1. BMR Calculation (Mifflin-St Jeor)
        if gender == "Male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        # 2. Activity Multiplier
        multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
        tdee = bmr * multipliers.get(activity, 1.2)

        # 3. Body Type Adjustment (Metabolic Correction)
        # Skinny people often have higher NEAT (fidgeting/movement), Overweight often have lower.
        if body_type == "Skinny":
            tdee += 200  # fast metabolism buffer
        elif body_type == "Overweight":
            tdee -= 200  # slow metabolism adjustment

        # 4. Goal Adjustment
        if goal == "Lose Weight": 
            # Overweight people can handle a slightly larger deficit safely
            deficit = 500 if body_type == "Overweight" else 300
            return int(tdee - deficit)
        
        elif goal == "Gain Weight": 
            # Skinny people need a larger surplus to grow
            surplus = 500 if body_type == "Skinny" else 300
            return int(tdee + surplus)
            
        return int(tdee) # Maintain

    def generate_weekly_diet(self, diet_pref):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekly_plan = {}
        meals = ['Breakfast', 'Lunch', 'Snack', 'Dinner']

        for day in days:
            daily_meals = {}
            for meal in meals:
                query = f"SELECT name, calories, protein FROM food_items WHERE type = '{diet_pref}' AND meal_time = '{meal}' ORDER BY RAND() LIMIT 1"
                if diet_pref == "Both":
                     query = f"SELECT name, calories, protein FROM food_items WHERE meal_time = '{meal}' ORDER BY RAND() LIMIT 1"
                
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                daily_meals[meal] = result if result else ("Water", 0, 0) 
            weekly_plan[day] = daily_meals
            
        return weekly_plan

    def get_weekly_workout(self, location, goal, body_type):
        # Returns a dictionary for day-wise splits tailored to BODY TYPE
        
        # --- GYM WORKOUTS ---
        if location == "Gym":
            if body_type == "Skinny":
                # Skinny: Focus on Heavy Compounds, Low Cardio to conserve calories
                return {
                    "Mon": "Heavy Push (Bench Press 5x5, Overhead Press)",
                    "Tue": "Heavy Pull (Deadlifts 3x5, Rows)",
                    "Wed": "Rest (Eat Big!)",
                    "Thu": "Legs (Squats 5x5, Lunges)",
                    "Fri": "Upper Body Hypertrophy (Dumbbells)",
                    "Sat": "Rest",
                    "Sun": "Rest"
                }
            elif body_type == "Overweight":
                # Overweight: Focus on Metabolic Conditioning & Fat Burn
                return {
                    "Mon": "Circuit Training (Weights + Cardio)",
                    "Tue": "Steady Cardio (Treadmill 30m) + Abs",
                    "Wed": "Full Body Weights (High Reps 3x15)",
                    "Thu": "HIIT Cardio (20 mins intense)",
                    "Fri": "Legs & Shoulders (High Volume)",
                    "Sat": "Active Recovery (Long Walk/Swim)",
                    "Sun": "Rest"
                }
            else: # Average
                return {
                    "Mon": "Push (Chest/Triceps)",
                    "Tue": "Pull (Back/Biceps)",
                    "Wed": "Legs (Squats/Calves)",
                    "Thu": "Rest",
                    "Fri": "Upper Body",
                    "Sat": "Lower Body",
                    "Sun": "Rest"
                }

        # --- HOME WORKOUTS ---
        else: 
            if body_type == "Skinny":
                return {
                    "Mon": "Push-ups (Weighted if possible) 3xFailure",
                    "Tue": "Bodyweight Squats & Lunges (Slow Tempo)",
                    "Wed": "Rest",
                    "Thu": "Pull-ups / Door Rows & Dips",
                    "Fri": "Full Body Calisthenics",
                    "Sat": "Rest",
                    "Sun": "Rest"
                }
            elif body_type == "Overweight":
                 return {
                    "Mon": "HIIT (Burpees, Jumping Jacks) 20m",
                    "Tue": "Power Yoga / Mobility Flow",
                    "Wed": "Bodyweight Circuit (Non-stop 15m)",
                    "Thu": "Shadow Boxing / Skipping",
                    "Fri": "Lower Body Bodyweight (High Reps)",
                    "Sat": "Long Walk (45 mins)",
                    "Sun": "Rest"
                }
            else: # Average
                return {
                    "Mon": "Full Body Strength",
                    "Tue": "Cardio & Core",
                    "Wed": "Lower Body Focus",
                    "Thu": "Rest",
                    "Fri": "Upper Body Focus",
                    "Sat": "Endurance/Run",
                    "Sun": "Rest"
                }
