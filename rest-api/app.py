from flask import Flask, request

app = Flask(__name__)

inventory = {
				"books":{
					"Harry Potter & Sorcerer's Stone": 20,
					"Harry Potter & Chambers of Secret": 19,
					"Harry Potter & Prisone of Azakab": 12
				},
				"furniture":{
					"Table": 100,
					"Sofa": 50,
					"Bed": 31,
					"Chair": 28
				},
				"electronics": {
					"AC": 2,
					"Refrigerator": 5
				}
			}


@app.get("/inventory")
def get_inventory():
	return inventory


'''
SAMPLE REQUEST
{
    "category":"food",
    "item": "chips",
    "count": 7
}
'''
@app.post("/addInventory")
def add_inventory():
	request_data = request.get_json()
	print(request_data)

	inventory_category = request_data.get("category")
	inventory_item = request_data.get("item")
	count = request_data.get("count", 0)

	if inventory_category in inventory.keys():
		if inventory_item in inventory.get(inventory_category):
			inventory[inventory_category][inventory_item] += count
		else:
			inventory[inventory_category][inventory_item] = count
	else:
		inventory[inventory_category] = {inventory_item: count}

	return {"Status": "Inventory Updated", "Updated With": request_data}, 201
