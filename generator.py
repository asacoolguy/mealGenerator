#!/user/bin/python
import json
import random

dishList = []


class Dish(object):
		def __init__(self, name, ingredients, tag):
			self.name = name
			self.ingredients = ingredients #list of strings
			self.tag = tag #list of strings

		def __str__(self):
			return "name: " + self.name + '\n' + "ingredients: " + \
				', '.join(self.ingredients) + '\n' + "tags: " + self.tag


# recursive decoder to turn read JSON unicode into python data
def DishDecode(data, ignore_dicts = False):
	# if unicode string, return as string
	if isinstance(data, unicode):
		return data.encode('utf-8')
	# if list, return list of decoded values using recursion
	if isinstance(data, list):
		return [DishDecode(item, ignore_dicts=True) for item in data]
	# if dict, return dict of decoded values using recursion
	if isinstance(data, dict) and not ignore_dicts:
		return {
			DishDecode(key, ignore_dicts=True) : DishDecode(value, ignore_dicts=True)
			for key, value in data.iteritems()
		}
	return data


def AddDish():
	# get the name of the dish
	name = raw_input("Name of the new dish: ").strip().lower()
	# get the ingredients of the dish
	ingredients_input = raw_input("Enter ingreidents used, separated with a comma.\n ---> ")
	ingredients = [x.strip().lower() for x in ingredients_input.split(',') if not x.isspace()]
	# get the tag of the dish
	while True:
		tag = raw_input("Is this a 'veggie', 'meat', or 'soup' dish? \n ---> ").strip().lower()
		if tag == 'veggie' or tag == 'meat' or tag == 'soup':
			break
		else:
			print "Invalid input: '" + tag + "'"
	
	# make the dish object
	newDish = Dish(name, ingredients, tag)
	print newDish
	# decide whether to save the dish
	while True:
		confirm = raw_input("Is this info correct? ").strip().lower()
		if confirm == "y" or confirm == "yes":
			print "Alrightie. Dish saved"
			dishList.append(newDish)
			break

		elif confirm == "n" or confirm == "no":
			print "Canceled. Returning to main menu."
			break
		else:
			print "Invalid input: '" + tag + "'"

# displays all dishes
def DisplayDishes():
	if len(dishList) > 0:
		print "Here is a list of all saved dishes:"
		for d in dishList:
			print str(dishList.index(d)+1) + ". " + d.name + "  (" + d.tag + ")"
	else:
		print "No dishes saved."

# displays the given dish
def DisplayDish(name):
	for d in dishList:
		if d.name == name:
			print d
			return
	print "Dish '" + name + "' not found. Returning to main menu"


def RemoveDish():
	name = raw_input("Name of the dish to be removed: ").strip().lower()
	for d in dishList:
		if d.name == name:
			dishList.remove(d)
			print "Dish '" + name + "' successfully removed. Returning to main menu."
			return
	print "Dish '" + name + "' not found. Returning to main menu"


# generates a given number of meals (default 1). Each meal has 1 meat + 1 veggie/soup. 
def GenerateMeals():
	num = raw_input("How many meals to generate?--->")

	if not num.isdigit() or int(num) < 1:
		print "Invalid number. Returning to main menu"
		return

	num = int(num)

	print "Generating Meal Plans for " + str(num) + " meals(s)..."

	# split the list into meat, veggie, and soup sublists.
	meatDishes = [d for d in dishList if d.tag == "meat"]
	veggieDishes = [d for d in dishList if d.tag == "veggie"]
	soupDishes = [d for d in dishList if d.tag == "soup"]
	generated = [] #a list of generated touples
	
	# for every meal, randomly remove 1 item from each list to be part of the meal.
	for n in range(num):
		# make sure there is enough meals left
		if len(meatDishes) < 1 or len(veggieDishes) < 1:
			print "Ran out of meals to use."
			break

		dishes = (random.choice(meatDishes), random.choice(veggieDishes))
		meatDishes.remove(dishes[0])
		veggieDishes.remove(dishes[1])
		generated.append(dishes)
		print "Meal #" + str(n+1)
		print "----->meat: " + dishes[0].name + ", veggie: " + dishes[1].name

	print str(n) + " meals generated.\n\n"

# load the dishes from the file
def LoadDishes():
	global dishList

	try:
		file = open("dishes.json", "r")
		data = DishDecode(json.load(file, object_hook=DishDecode))
		dishList = [Dish(d["name"], d["ingredients"], d["tag"]) for d in data]
		print "Dishes loaded."
	except IOError:
		file = open("dishes.json", "w")
		print "No dishes saved. New file created."

	file.close()


# save dishes into the file
def SaveDishes():
	with open("dishes.json", "w+") as file:
		json.dump([d.__dict__ for d in dishList], file, indent=4, separators=(',', ': ') ) 
		# 


# main method
#if __name__ == '__main__':

print "Welcome to Meal Generator"
LoadDishes()

# main loop
keepGoing = True
while (keepGoing):
	# print the main menu 
	print "*******************************************"
	command = raw_input("Enter 'add' or 'remove' to modify dishes." + \
		" Enter 'show' to show all currently saved dishes." + \
		" Enter 'show [name]' to show a specific dish." + \
		" Enter 'generate' to generate meals.\n--->").strip().lower()

	if command == 'add':
		AddDish()
		SaveDishes()
	elif command[0:4] == 'show':
		if len(command) == 4:
			DisplayDishes()
		else:
			DisplayDish(command[5:])
	elif command == 'remove':
		RemoveDish()
		SaveDishes()
	elif command == 'generate':
		GenerateMeals()
	else:
		print "Invalid input. Please try again. \n"
	
