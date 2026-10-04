from flask import Flask, render_template, request, redirect

app = Flask(__name__)
items = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        items.append({
            "name": request.form["name"],
            "colour": request.form["colour"],
            "quantity": request.form["quantity"],
        })
        return redirect("/")
    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
