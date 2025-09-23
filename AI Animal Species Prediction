# AI Animal Species Prediction
# By: Your Name

def get_animal_details(animal_name):
    animal_info = {
        "lion": {
            "Species": "Panthera leo",
            "Habitat": "Grasslands, savannas, and open woodlands",
            "Diet": "Carnivore (feeds mainly on large herbivores)",
            "Lifespan": "10-14 years in the wild, up to 20 years in captivity",
            "Special": "Known as the 'King of the Jungle'"
        },
        "tiger": {
            "Species": "Panthera tigris",
            "Habitat": "Forests, grasslands, and wetlands",
            "Diet": "Carnivore (feeds on deer, wild boar, etc.)",
            "Lifespan": "8-10 years in the wild, up to 20-25 in captivity",
            "Special": "Largest wild cat species"
        },
        "elephant": {
            "Species": "Elephas maximus (Asian) / Loxodonta africana (African)",
            "Habitat": "Forests, grasslands, and savannas",
            "Diet": "Herbivore (feeds on grass, fruits, roots, bark)",
            "Lifespan": "60-70 years",
            "Special": "Largest land animal on Earth"
        },
        "giraffe": {
            "Species": "Giraffa camelopardalis",
            "Habitat": "African savannas and open woodlands",
            "Diet": "Herbivore (feeds mainly on leaves, especially acacia trees)",
            "Lifespan": "20-25 years in the wild",
            "Special": "Tallest land animal"
        },
        "zebra": {
            "Species": "Equus zebra",
            "Habitat": "Grasslands and savannas of Africa",
            "Diet": "Herbivore (feeds on grasses, leaves, bark, roots)",
            "Lifespan": "20-25 years",
            "Special": "Known for black and white striped body"
        }
    }

    # Convert user input to lowercase
    animal_name = animal_name.lower()

    if animal_name in animal_info:
        print(f"\nDetails of {animal_name.capitalize()}:")
        for key, value in animal_info[animal_name].items():
            print(f"{key}: {value}")
    else:
        print("\nSorry! Animal not found in the database. Try lion, tiger, elephant, giraffe, or zebra.")


# Main Program
print("🐾 AI Animal Species Prediction 🐾")
user_animal = input("Enter an animal name (lion, tiger, elephant, giraffe, zebra): ")
get_animal_details(user_animal)
