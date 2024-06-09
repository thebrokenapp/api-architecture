from flask import Flask, request, make_response

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


@app.get("/inventory/<category_name>")
def get_category(category_name):
	if category_name not in inventory.keys():
		return {"message": "Category Does Not Exist"}
	return inventory.get(category_name)

@app.get("/inventory/<category_name>/<item>")
def get_item(category_name, item):
	response_data = make_response({})
	if category_name not in inventory.keys():
		response_data = make_response({"message": category_name +  " Category Does Not Exist"})
		response_data.status_code = 404
		response_data.location = "/inventory/" + category_name + "/" + item
		return response_data
	else:
		if item not in inventory[category_name].keys():
			response_data = make_response({"message": item +  " Item Does Not Exist"})
			response_data.status_code = 404
			response_data.location = "/inventory/" + category_name + "/" + item
			return response_data
		else:
			response_data = make_response({"message": item +  " Found", "count": inventory.get(category_name).get(item)})
			response_data.status_code = 201
			response_data.location = "/inventory/" + category_name + "/" + item
			return response_data
