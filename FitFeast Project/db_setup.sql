-- DATABASE SETUP FOR FITFEAST
-- Author: Naman
-- Description: Sets up the schema and seeds data for the Fitness Planner Application

-- 1. Create and Use Database
CREATE DATABASE IF NOT EXISTS fitbharat_db;
USE fitbharat_db;

-- 2. Clean up old tables if they exist (allows re-running the script)
DROP TABLE IF EXISTS food_items;
DROP TABLE IF EXISTS exercises;

-- 3. Create Tables
CREATE TABLE food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    calories INT,
    protein INT, -- in grams
    type ENUM('Veg', 'Non-Veg'),
    cost_level ENUM('Low', 'Medium', 'High'),
    meal_time ENUM('Breakfast', 'Lunch', 'Snack', 'Dinner')
);

CREATE TABLE exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    target_muscle VARCHAR(50),
    setup_type ENUM('Home', 'Gym'),
    difficulty ENUM('Beginner', 'Intermediate', 'Advanced')
);

-- 4. SEED DATA: Breakfast Options (Indian/Affordable)
INSERT INTO food_items (name, calories, protein, type, cost_level, meal_time) VALUES 
('Oats Upma with Peanuts', 300, 10, 'Veg', 'Low', 'Breakfast'),
('Poha with Soya Granules', 280, 12, 'Veg', 'Low', 'Breakfast'),
('Besan Chilla (2 pcs)', 220, 14, 'Veg', 'Low', 'Breakfast'),
('Paneer Paratha (1 pc) + Curd', 350, 12, 'Veg', 'Medium', 'Breakfast'),
('Boiled Eggs (3) + Toast', 240, 19, 'Non-Veg', 'Low', 'Breakfast'),
('Scrambled Eggs (3) + Roti', 280, 20, 'Non-Veg', 'Low', 'Breakfast'),
('Masala Omelette (2 eggs) + Bread', 300, 14, 'Non-Veg', 'Low', 'Breakfast');

-- 5. SEED DATA: Lunch Options
INSERT INTO food_items (name, calories, protein, type, cost_level, meal_time) VALUES 
('Dal Tadka + 2 Rotis + Salad', 450, 18, 'Veg', 'Low', 'Lunch'),
('Rajma Chawal (1 bowl)', 500, 16, 'Veg', 'Low', 'Lunch'),
('Chole + 2 Rotis', 480, 14, 'Veg', 'Low', 'Lunch'),
('Palak Paneer + 2 Rotis', 450, 18, 'Veg', 'Medium', 'Lunch'),
('Chicken Curry (Home style) + Rice', 550, 35, 'Non-Veg', 'Medium', 'Lunch'),
('Egg Curry (2 Eggs) + 2 Rotis', 400, 20, 'Non-Veg', 'Low', 'Lunch');

-- 6. SEED DATA: Snack Options
INSERT INTO food_items (name, calories, protein, type, cost_level, meal_time) VALUES 
('Roasted Chana (1 cup)', 150, 8, 'Veg', 'Low', 'Snack'),
('Peanut Salad', 200, 9, 'Veg', 'Low', 'Snack'),
('Sprouts Salad', 120, 10, 'Veg', 'Low', 'Snack'),
('Masala Buttermilk', 60, 4, 'Veg', 'Low', 'Snack'),
('Boiled Egg Whites (3)', 51, 11, 'Non-Veg', 'Low', 'Snack'),
('Chicken Salami Sandwich', 250, 15, 'Non-Veg', 'Medium', 'Snack');

-- 7. SEED DATA: Dinner Options
INSERT INTO food_items (name, calories, protein, type, cost_level, meal_time) VALUES 
('Soya Chunk Curry + 1 Roti', 300, 25, 'Veg', 'Low', 'Dinner'),
('Paneer Bhurji + 1 Roti', 350, 18, 'Veg', 'Medium', 'Dinner'),
('Mixed Dal + Rice', 350, 15, 'Veg', 'Low', 'Dinner'),
('Moong Dal Khichdi', 300, 12, 'Veg', 'Low', 'Dinner'),
('Grilled Chicken Salad', 250, 30, 'Non-Veg', 'Medium', 'Dinner'),
('Chicken Stir Fry + 1 Roti', 350, 28, 'Non-Veg', 'Medium', 'Dinner');

-- 8. SEED DATA: Exercises (Optional, if you expand the DB later)
INSERT INTO exercises (name, target_muscle, setup_type, difficulty) VALUES
('Push-ups', 'Chest', 'Home', 'Beginner'),
('Squats', 'Legs', 'Home', 'Beginner'),
('Bench Press', 'Chest', 'Gym', 'Intermediate'),
('Deadlift', 'Back', 'Gym', 'Advanced');