# AI Diet Planner 🥗
# - No external libraries. Runs in the console.
# - Inputs: age, weight (kg), goal (loss/maintain/gain), diet type (veg/vegan/non-veg)
# - Output: Day plan with meal calories and scaled portion guidance + hydration target.
# NOTE: This is an educational tool, not medical advice.

def ask_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"  Please enter a value >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  Please enter a value <= {max_val}.")
                continue
            return val
        except ValueError:
            print("  Please enter a valid integer.")

def ask_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"  Please enter a value >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  Please enter a value <= {max_val}.")
                continue
            return val
        except ValueError:
            print("  Please enter a valid number.")

def ask_choice(prompt, choices, default=None):
    choices_lower = [c.lower() for c in choices]
    while True:
        raw = input(prompt).strip().lower()
        if not raw and default:
            return default.lower()
        if raw in choices_lower:
            return raw
        print(f"  Please choose from: {', '.join(choices)}")

def maintenance_calories(age, weight_kg):
    """Simple age-based factor (kcal/kg/day)."""
    if age < 18:
        factor = 35
    elif age <= 30:
        factor = 32
    elif age <= 50:
        factor = 30
    else:
        factor = 28
    return factor * weight_kg

def target_calories(maint, goal):
    if goal in ("loss", "lose", "weight loss", "reduce"):
        tgt = maint - 500
        return max(tgt, 1200)  # avoid going too low
    elif goal in ("gain", "weight gain", "bulk"):
        return maint + 300
    else:
        return maint

def protein_target(weight_kg, goal):
    # simple heuristic
    if goal in ("gain", "weight gain", "bulk"):
        g_per_kg = 1.6
    elif goal in ("loss", "lose", "weight loss", "reduce"):
        g_per_kg = 1.2
    else:
        g_per_kg = 1.0
    return round(g_per_kg * weight_kg)

def water_target_liters(weight_kg):
    # 30–35 ml per kg → ~0.033 L/kg
    return round(weight_kg * 0.033, 1)

MEAL_SPLIT = {
    "Breakfast": 0.25,
    "AM Snack":  0.10,
    "Lunch":     0.30,
    "PM Snack":  0.10,
    "Dinner":    0.25
}

# Base meal templates with approximate kcal and a base portion description.
# We'll scale the portion relative to the user's target for that meal.
TEMPLATES = {
    "veg": {
        "Breakfast": (350, "Oats porridge with milk + 1 banana + 10 nuts"),
        "AM Snack":  (150, "1 apple + 8 almonds"),
        "Lunch":     (600, "Brown rice + dal + mixed veg + curd + salad"),
        "PM Snack":  (150, "Greek yogurt (unsweetened) + 1 tsp honey"),
        "Dinner":    (500, "2 chapatis + paneer curry + salad")
    },
    "vegan": {
        "Breakfast": (350, "Oats porridge with soy milk + 1 banana + 10 nuts"),
        "AM Snack":  (150, "1 orange + 8 almonds"),
        "Lunch":     (600, "Brown rice + chickpea curry + mixed veg + salad"),
        "PM Snack":  (150, "Roasted chana (30g) + green tea"),
        "Dinner":    (500, "2 chapatis + tofu curry + salad")
    },
    "non-veg": {
        "Breakfast": (350, "2-egg omelette + 2 toast + 1 fruit"),
        "AM Snack":  (150, "Buttermilk (250ml) + 1 small fruit"),
        "Lunch":     (650, "Rice + chicken curry + dal + salad"),
        "PM Snack":  (150, "Boiled eggs (2) or yogurt (150g)"),
        "Dinner":    (550, "2 chapatis + fish curry or grilled chicken + salad")
    }
}

def scale_note(base_kcal, target_kcal):
    ratio = target_kcal / base_kcal if base_kcal > 0 else 1.0
    # Clamp ratio to a nice display range
    return f"(~×{ratio:.1f} of the base portion)"

def plan_day(total_kcal, diet_type):
    base = TEMPLATES[diet_type]
    plan = []
    for meal, fraction in MEAL_SPLIT.items():
        meal_kcal = round(total_kcal * fraction)
        base_kcal, desc = base[meal]
        note = scale_note(base_kcal, meal_kcal)
        plan.append((meal, meal_kcal, desc, note))
    return plan

def main():
    print("\n🟢 AI Diet Planner 🥗 (Console)")
    print("This tool gives a simple day plan from age, weight and goal.\n")

    age = ask_int("Enter your age (years): ", min_val=10, max_val=100)
    weight = ask_float("Enter your weight (kg): ", min_val=25, max_val=250)

    goal = ask_choice(
        "Goal (loss / maintain / gain): ",
        ["loss", "maintain", "gain"]
    )
    diet = ask_choice(
        "Diet type (veg / vegan / non-veg) [default: veg]: ",
        ["veg", "vegan", "non-veg"],
        default="veg"
    )

    maint = maintenance_calories(age, weight)
    target = round(target_calories(maint, goal))
    protein_g = protein_target(weight, goal)
    water_l = water_target_liters(weight)

    print("\n==========================================")
    print("             YOUR DAILY TARGET            ")
    print("==========================================")
    print(f"Estimated maintenance: ~{round(maint)} kcal/day")
    print(f"Target for goal ({goal}): {target} kcal/day")
    print(f"Protein target: ~{protein_g} g/day")
    print(f"Hydration goal: ~{water_l} L/day")
    print("Diet type:", diet)
    print("==========================================\n")

    day_plan = plan_day(target, diet)

    for meal, kcal, desc, note in day_plan:
        print(f"🍽️  {meal}  →  ~{kcal} kcal")
        print(f"    • {desc}  {note}\n")

    print("✅ Tips:")
    print(" - Try to hit the meal calories within ±10%.")
    print(" - Prefer whole foods, lean proteins, and fiber-rich veggies.")
    print(" - Adjust salt/sugar to taste; avoid sugary drinks.")
    print(" - Walk 20–30 minutes if possible.\n")
    print("⚠️ Disclaimer: This is a simplified planning tool and not medical advice.")
    print("   Consult a professional for personalized nutrition guidance.\n")

if __name__ == "__main__":
    main()
