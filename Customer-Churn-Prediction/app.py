import os
import pandas as pd
from flask import Flask, request, render_template, jsonify
import pickle
import requests
import json
import sys
print(sys.executable)
app = Flask(__name__)


app = Flask("Customer Churn Predictor")

# Load the dataset
df_1 = pd.read_csv("Trained and Test Data/Test_Telc.csv")


@app.route("/")
def load_demo_page():
    """
    Renders the demo.html page as the initial landing page.
    """
    return render_template('demo.html')

@app.route("/home")
def load_home_page():
    """
    Renders the home.html page.
    """
    return render_template('home.html', query="")

@app.route("/ask-to-ai")
def load_chatbot_page():
    """
    Renders the chatbot.html page.
    """
    return render_template('chatbot.html')

@app.route("/api/chat", methods=['POST'])
def chat_api():
    """
    API endpoint to handle chat queries related to customer churn prediction using Cohere Command R+ API.
    """
    data = request.get_json()
    user_message = data.get('message', '').strip()
    chat_history = data.get('chat_history', [])

    if not user_message:
        response_text = "Please enter a valid question about customer churn prediction."
        return jsonify({"response": response_text})

    cohere_api_url = "https://api.cohere.ai/v1/chat"
    cohere_api_key = "afs34b7yzpJHa9B6X3mPmJQVEmHVvQi2Y8UPbKen"

    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }

    preamble = "You are a domain expert in Customer Churn Prediction. Answer only questions related to churn metrics, machine learning models, data preprocessing, and KPI analysis. Politely decline unrelated questions."

    payload = {
    "model": "command-r-plus-08-2024",  # Updated from "command-r-plus"
    "preamble": preamble,
    "message": user_message,
    "chat_history": chat_history
}

    try:
        response = requests.post(cohere_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            response_text = response_json.get("text", "Sorry, no response text received.")
        else:
            response_text = f"Cohere API request failed with status code {response.status_code}."
            print(response_text)
    except Exception as e:
        response_text = "Sorry, there was an error processing your request."
        print(f"Cohere API error: {e}")

    return jsonify({"response": response_text})

@app.route("/predict", methods=['POST'])
def predict():
    """
    Handles the prediction request from the home.html form.
    """
    # Retrieve input data from the form
    input_data = [
        request.form['query1'],  # SeniorCitizen
        request.form['query2'],  # MonthlyCharges
        request.form['query3'],  # TotalCharges
        request.form['query4'],  # gender
        request.form['query5'],  # Partner
        request.form['query6'],  # Dependents
        request.form['query7'],  # PhoneService
        request.form['query8'],  # MultipleLines
        request.form['query9'],  # InternetService
        request.form['query10'], # OnlineSecurity
        request.form['query11'], # OnlineBackup
        request.form['query12'], # DeviceProtection
        request.form['query13'], # TechSupport
        request.form['query14'], # StreamingTV
        request.form['query15'], # StreamingMovies
        request.form['query16'], # Contract
        request.form['query17'], # PaperlessBilling
        request.form['query18'], # PaymentMethod
        request.form['query19']  # tenure
    ]

    # Validate inputs
    if not validate_inputs(input_data):
        return render_template('home.html', output1="Invalid input data!", output2="", query="")

    # Load the model
    model = pickle.load(open("model.sav", "rb"))

    # Create a DataFrame for the new input
    new_df = pd.DataFrame([input_data], columns=[
        'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
        'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 
        'DeviceProtection', 'TechSupport', 'StreamingTV', 
        'StreamingMovies', 'Contract', 'PaperlessBilling', 
        'PaymentMethod', 'tenure'
    ])

    # Concatenate with the existing DataFrame
    df_2 = pd.concat([df_1, new_df], ignore_index=True)

    # Group the tenure in bins of 12 months
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
    df_2['tenure_group'] = pd.cut(df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels)

    # Drop the 'tenure' column
    df_2.drop(columns=['tenure'], axis=1, inplace=True)

    # Create dummy variables
    new_df_dummies = pd.get_dummies(df_2[['gender', 'SeniorCitizen', 'Partner', 'Dependents', 
                                             'PhoneService', 'MultipleLines', 'InternetService', 
                                             'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                                             'TechSupport', 'StreamingTV', 'StreamingMovies', 
                                             'Contract', 'PaperlessBilling', 'PaymentMethod', 
                                             'tenure_group']])

    # Align the input DataFrame with the model's expected features
    expected_features = model.get_booster().feature_names
    new_df_dummies = new_df_dummies.reindex(columns=expected_features, fill_value=0)

    # Make the prediction
    single = model.predict(new_df_dummies.tail(1))
    probability = model.predict_proba(new_df_dummies.tail(1))[:, 1]

       # Prepare output messages
    if single == 1:
        output1 = "This customer is likely to be churned!!"
    else:
        output1 = "This customer is likely to continue!!"
    
    output2 = "Confidence: {:.2f}%".format(probability[0] * 100)

    # === Dynamic Recommendations ===
    # === Dynamic Recommendations ===
    recommendations = []

    senior = int(request.form['query1'])
    monthly_charges = float(request.form['query2'])
    tenure = int(request.form['query19'])
    internet_service = request.form['query9']
    online_security = request.form['query10']
    tech_support = request.form['query13']
    contract = request.form['query16']
    payment_method = request.form['query18']

# Add churn/stay and confidence-based statements first
    if single == 1:  # Likely to churn
        if probability[0] * 100 > 80:
            recommendations.append("High churn risk detected — immediate retention action recommended.")
        elif probability[0] * 100 > 50:
            recommendations.append("Moderate churn risk — consider preventive offers.")
        else:
            recommendations.append("Slight churn risk — monitor and maintain engagement.")
    else:  # Likely to stay
        if probability[0] * 100 > 80:
            recommendations.append("Very strong customer loyalty — focus on rewarding them.")
        elif probability[0] * 100 > 50:
            recommendations.append("Good retention probability — maintain satisfaction.")
        else:
            recommendations.append("Retention is likely but monitor periodically.")

# Factor-based suggestions (same as original but applied after status)
    if contract == "Month-to-month":
        recommendations.append("Encourage switching to annual or biennial contracts with discounts.")
    if payment_method == "Electronic check":
        recommendations.append("Promote switching to auto-pay or credit card to reduce churn risk.")
    if internet_service == "Fiber optic":
        recommendations.append("Highlight speed and reliability to justify the higher cost.")
    if online_security == "No":
        recommendations.append("Offer bundled online security at a discounted rate.")
    if tech_support == "No":
        recommendations.append("Offer a free trial of tech support for customer engagement.")
    if monthly_charges > 80:
        recommendations.append("Suggest lower-tier or loyalty discount plans.")
    if senior == 1:
        recommendations.append("Provide special assistance or senior-friendly offers.")
    if tenure < 12:
        recommendations.append("Offer onboarding benefits for new customers.")

# Positive reinforcements
    if contract in ["One year", "Two year"]:
        recommendations.append("Maintain customer satisfaction with periodic rewards.")
    if online_security == "Yes":
        recommendations.append("Continue offering valued security services.")
    if tech_support == "Yes":
        recommendations.append("Highlight your quick resolution times.")
    if tenure >= 24:
        recommendations.append("Reward loyalty with exclusive offers.")
    if monthly_charges < 60:
        recommendations.append("Promote added services without increasing cost drastically.")
    if payment_method in ["Bank transfer (automatic)", "Credit card (automatic)"]:
        recommendations.append("Highlight convenience of current payment method.")

    ai_recommendations = "\n".join([f"• {rec}" for rec in recommendations]) \
                     if recommendations else "No specific recommendations — profile stable."





    return render_template('home.html', output1=output1, output2=output2, ai_recommendations=ai_recommendations,
                           query1=request.form['query1'], 
                           query2=request.form['query2'],
                           query3=request.form['query3'],
                           query4=request.form['query4'],
                           query5=request.form['query5'], 
                           query6=request.form['query6'], 
                           query7=request.form['query7'], 
                           query8=request.form['query8'], 
                           query9=request.form['query9'], 
                           query10=request.form['query10'], 
                           query11=request.form['query11'], 
                           query12=request.form['query12'], 
                           query13=request.form['query13'], 
                           query14=request.form['query14'], 
                           query15=request.form['query15'], 
                           query16=request.form['query16'], 
                           query17=request.form['query17'],
                           query18=request.form['query18'], 
                           query19=request.form['query19'])

def validate_inputs(inputs):
    """
    Validates the input data types.
    """
    try:
        inputs[0] = int(inputs[0])  # SeniorCitizen
        inputs[1] = float(inputs[1])  # MonthlyCharges
        inputs[2] = float(inputs[2])  # TotalCharges
        # Add more validations as needed
    except ValueError:
        return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
