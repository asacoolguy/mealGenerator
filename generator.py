#!/user/bin/python
import json


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
	ingredients = [x.strip().lower() for x in ingredients_input.split(',')]
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
			print "Alrightie."
			dishList.append(newDish)
			break

		elif confirm == "n" or confirm == "no":
			print "Canceled. Returning to main menu."
			break
		else:
			print "Invalid input: '" + tag + "'"


def DisplayDishes():
	print "Here is a list of all saved dishes:"
	for d in dishList:
		print str(dishList.index(d)+1) + ". " + d.name


def RemoveDish():
	name = raw_input("Name of the dish to be removed: ").strip().lower()
	for d in dishList:
		if d.name == name:
			dishList.remove(d)
			print "Dish '" + name + "' successfully removed. Returning to main menu."
			return
	print "Dish '" + name + "' not found. Returning to main menu"


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
	print "Dishes saved."


# main method
#if __name__ == '__main__':

print "Welcome to Meal Generator"
LoadDishes()

# main loop
keepGoing = True
while (keepGoing):
	# print the main menu 
	command = raw_input("Enter 'add' or 'remove' to modify dishes." + \
		" Enter 'list' to list currently saved dishes." + \
		" Enter 'generate' to generate meals.\n--->").strip().lower()

	if command == 'add':
		AddDish()
		SaveDishes()
	elif command == 'list':
		DisplayDishes()
	elif command == 'remove':
		RemoveDish()
		SaveDishes()
	else:
		print "Invalid input. Please try again. \n"
	
