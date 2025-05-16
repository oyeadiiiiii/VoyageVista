from flask import Flask, request, render_template, jsonify
import joblib

app = Flask(__name__)

model = joblib.load("D:\PROJECTS\VoyageVista\CODE\decision_tree_model.joblib")


status_mapping = {
    0: "CERTIFIED",
    1: "DENIED"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prediction/y_predict", methods=["POST"])
def y_predict():

    full_time_position = request.form.get("FULL_TIME_POSITION")
    soc_n = request.form.get("SOC_N")
    prevailing_wage = request.form.get("PREVAILING_WAGE")
    year = request.form.get("YEAR")


    full_time_position = 1 if full_time_position == "Full Time" else 0
    soc_mapping = {
        "Administrative": 0, "Agriculture": 1, "Audit": 2, "Database": 3,
        "Education": 4, "Estate": 5, "Executives": 6, "Finance": 7,
        "H.R": 8, "IT": 9, "Manager": 10, "Mechanical": 11, 
        "Medical": 12, "P.R": 13, "Sales & Market": 14, "others": 15
    }
    soc_n = soc_mapping.get(soc_n, 15)  


    input_data = [[full_time_position, float(prevailing_wage), int(year), soc_n]]


    prediction = model.predict(input_data)[0]
    result = status_mapping.get(prediction, "Unknown")

    return jsonify({"prediction_text": result})


if __name__ == "__main__":
    app.run(debug=True)
