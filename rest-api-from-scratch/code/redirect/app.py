from flask import Flask, redirect, url_for, jsonify

app = Flask(__name__)

# 1. Permanent Redirect (301) with Path Parameter
@app.route('/old-url/<userid>')
def old_url(userid):
    # Redirect to a new URL permanently with the userid parameter
    return redirect(url_for('new_url', userid=userid), code=301)

@app.route('/new-url/<userid>')
def new_url(userid):
    return jsonify({"message": f"This is the new URL for user {userid}!"})

if __name__ == '__main__':
    app.run(debug=True)
