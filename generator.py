#!/user/bin/python

print "hello world!"

class Dish(object):
		def __init__(self, name, ingredients, tags):
			self.name = name
			self.ingredients = ingredients #list of strings
			self.tags = tags #list of strings

		def __str__(self):
			return "name: " + self.name + "\ningredients: " + self.ingredients + "\ntags: " + self.tags


if __name__ == '__main__':
	name = raw_input("Name of the dish: ")
	ingredients = raw_input("Enter ingreidents used, separated with a comma. ---> ")
	tags = raw_input("Is this a 'veggie', 'meat', or 'soup' dish? ---> ")
	dish = Dish(name, ingredients, tags)
	print dish 
