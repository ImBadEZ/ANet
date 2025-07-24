from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "sites.json"

# Load or create the site storage
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        sites = json.load(f)
else:
    sites = {}

# GET site by domain
@app.route("/site/<domain>", methods=["GET"])
def get_site(domain):
    domain = domain.lower()
    code = sites.get(domain)
    return jsonify({"code": code})

# POST to add or update a site
@app.route("/site", methods=["POST"])
def add_site():
    data = request.json
    domain = data.get("domain", "").lower()
    code = data.get("code", "")

    if not domain or not code:
        return "Missing domain or code", 400

    sites[domain] = code
    with open(DATA_FILE, "w") as f:
        json.dump(sites, f, indent=2)

    return "Saved", 200

if __name__ == "__main__":
    app.run(debug=True)
