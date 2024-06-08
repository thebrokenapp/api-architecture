from flask import Flask

app = Flask(__name__)

@app.get("/inventory")
def get_inventory():
	return {"books":["Harry Potter 1, Harry Potter 2, Harry Potter 3"], "furniture":["table", "bed", "sofa", "chair", "wadrobe"], "electronics": ["AC", "Refrigerator"] }
