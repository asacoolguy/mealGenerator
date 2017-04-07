#!/user/bin/python
import json
import random

dishList = []


class Dish(object):
		def __init__(self, name, ingredients, tag):
			self.name = name
			self.ingredients = ingredients # list of strings
			self.tag = tag # single string
			self.freq = 1 # how many times has this dish showed up? default is 1

		def __str__(self):
			return "name: " + self.name + '\n' + "ingredients: " + \
				', '.join(self.ingredients) + '\n' + "tag: " + self.tag + \
				'\nfrequency: ' + str(self.freq)


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
	# sort the dishList by name first
	dishList.sort(key = lambda d: d.name)

	if len(dishList) > 0:
		print "Here is a list of all saved dishes:"
		for d in dishList:
			print str(dishList.index(d)+1) + ". " + d.name + "  (" + d.tag[0:1] + ")"
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

	# split the list into meat, veggie, and soup sublists.
	meatDishes = [d for d in dishList if d.tag == "meat"]
	veggieDishes = [d for d in dishList if d.tag == "veggie"]
	soupDishes = [d for d in dishList if d.tag == "soup"]
	generated = []

	print "Generating Meal Plans for " + str(num) + " meals(s)..."
	
	# for every meal, randomly remove 1 item from each list to be part of the meal.
	for n in range(num):
		# make sure there is enough meals left
		if len(meatDishes) < 1 or len(veggieDishes) < 1:
			print "Ran out of meals to use."
			break

		newMeal = (PickRandomDish(meatDishes), PickRandomDish(veggieDishes))
		meatDishes.remove(newMeal[0])
		veggieDishes.remove(newMeal[1])
		generated.append(newMeal)

	PrintGeneratedDishes(generated)
	# ask if any should be regenerated
	repeat = True
	while repeat:
		confirm = raw_input("Is this meal plan good? Enter 'yes' to confirm. " + \
			"Enter 'redo [number]' regenerate a certain meal. " + \
			"Enter 'no' to cancel and return to the main menu.\n--->").strip().lower()
		if confirm == "y" or confirm == "yes":
			print "Alrightie. Producing a grocery list.\n\n"
			# update freq number
			for m, v in generated:
				m.freq += 1
				v.freq += 1
			SaveDishes()
			# print and save grocery list
			PrintGroceryList(generated)
			print "Grocery list saved. Returning to main menu."
			repeat = False
		elif confirm[0:4] == "redo" and confirm[5:].isdigit():
			mealNum = int(confirm[5:])
			if mealNum < 1 or mealNum > len(generated):
				print str(mealNum) + " is out of range!"
			else:
				#regenerate a certain meal
				RegenerateMeal(meatDishes, veggieDishes, generated, mealNum)
				PrintGeneratedDishes(generated)
		elif confirm == "n" or confirm == "no":
			print "Canceled. Returning to main menu."
			repeat = False
		else:
			print "Invalid input: '" + confirm + "'"

# given a list of leftover meats and veggies, the generated list and a number
# regenerates a certain meal by modifying the generated list in place
def RegenerateMeal(meatDishes, veggieDishes, generated, mealNum):
	print "Regenerating meal #" + str(mealNum)
	num = mealNum - 1 # adjust the index

	meatDishes.append(generated[num][0])
	veggieDishes.append(generated[num][1])

	newMeal = (PickRandomDish(meatDishes), PickRandomDish(veggieDishes))
	meatDishes.remove(newMeal[0])
	veggieDishes.remove(newMeal[1])

	generated.pop(num)
	generated.insert(num, newMeal)


# given a list of meat+veggie tuples, prints it out
def PrintGeneratedDishes(generated):
	for n in range(len(generated)):
		print "Meal #" + str(n+1)
		print "----->meat: " + generated[n][0].name + ", veggie: " + generated[n][1].name

	print str(n+1) + " meals generated.\n"


# outputs a list of ingredients
def PrintGroceryList(generated):
	ingredients = []
	i = 1
	for m, v in generated:
		ingredients.append("Meal " + str(i) + " meat: " + m.name)
		ingredients += [("\t" + d) for d in m.ingredients if not (d in ingredients)]
		ingredients.append("Meal " + str(i) + " veggie: " + v.name)
		ingredients += [("\t" + d) for d in v.ingredients if not (d in ingredients)]
		i += 1
	
	with open("grocery list.txt", "w+") as file:
		for i in ingredients:
			print i
			file.write(i + "\n")


# given a list of dishes, returns a dish at random
# balances the probability so less frequent dishes get higher chance of showing up
def PickRandomDish(dishes):
	# if there's only 1 dish left, just return the 1
	if len(dishes) == 1:
		return dishes[0]

	# find the sum of all freqs
	sum = 0
	for d in dishes:
		sum += d.freq

	# make a list of tuples of the dish plus its probability value
	# probability is inversely related to how frequently the dish shows up
	probList = [(d, sum - d.freq) for d in dishes]

	# calculate the sum based on probability
	newSum = 0
	for (d, p) in probList:
		newSum += p

	# randomly pick from probList based on the probability
	r = random.randint(1,newSum)
	for (d, p) in probList:
		r = r - p
		if r <= 0:
			return d


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


# main method
#if __name__ == '__main__':

print "Welcome to Meal Generator"
LoadDishes()

# main loop
keepGoing = True
while (keepGoing):
	# print the main menu 
	print "\n********************MAIN MENU********************"
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
	
