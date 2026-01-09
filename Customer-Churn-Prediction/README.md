# Customer Churn Prediction and Retention Strategies

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-green)
![ML](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Status-Published-success)

## 📌 Project Overview
This project focuses on predicting customer churn in the telecommunications industry and providing actionable retention strategies. It integrates **Machine Learning models** for prediction, a **Chatbot** for customer interaction, and a **Recommendation System** to suggest personalized retention plans.

This work was developed during our 3rd Year of B.Tech (CSE - Big Data Analytics) and has been **published as a research paper**.

## 👥 Contributors
This project was a collaborative effort by our team 'PU_BDA19':

* **[Jaiswal Vaibhav Rohitbhai](https://github.com/VRJ1718)** - *Data Analyst / Data Collection / Reseach Paper Publication*
* **[Sane Harsh Balkrishna](https://github.com/HAWK9315S)** - *Data Analyst / Documentation / Frontend Developement*
* **[Ashish Thomas John](https://github.com/AJohn200408)** - *Data Analyst / Data Cleaning and Transformation / Model Building and Evaluation*
* **[Adithya Vinod]()** - *Data Analyst / Exploratory Data Analysis / Reseach Paper Publication*

## 📂 Repository Structure
The project is organized into the following directories for clarity:

| Folder Name | Description |
| :--- | :--- |
| **`Trained and Test Data`** | Contains the dataset files (`Telco_Customer_Churn.csv` and `Test_Telc.csv`) used for training and testing. |
| **`EDA and Models`** | Contains Jupyter Notebooks for Exploratory Data Analysis and Model Training (`.ipynb` files). |
| **`Research Paper and Critical Evaluation`** | Contains the published research paper and the critical evaluation document associated with this project. |
| **`Documentation`** | Contains project reports, PowerPoint presentations, and other supporting documentation. |
| **`templates`** | Contains the HTML files (`home.html`, `demo.html`, `chatbot.html`) for the Web Interface. |
| **Root Directory** | Contains `app.py` (Flask App), `model.sav` (Trained Model), and `requirements.txt`. |

## 🚀 Features
- **Churn Prediction Engine**: Uses XGBoost and Decision Tree classifiers to predict if a customer is likely to leave.
- **Exploratory Data Analysis (EDA)**: Deep dive into customer behaviors (Senior Citizens, Payment Methods, Contract types).
- **Intelligent Chatbot**: Integrated AI chatbot (using Cohere API) to assist users with churn-related queries.
- **Web Interface**: A user-friendly Flask web application to interact with the model.

## ⚠️ Environmental Setup & Prerequisites

### Why do we need to install libraries?
This project relies on several powerful external Python libraries to function. Python does not include these by default. Before running the project, we must "import" (install) these dependencies to ensure that:
1.  **The Web App Runs:** `Flask` is required to start the local web server.
2.  **The Model Predicts:** `XGBoost` and `Scikit-Learn` are needed to load the saved machine learning model.
3.  **The Chatbot Responds:** `Cohere` and `Requests` are essential for connecting to the AI API.

Without installing these, the application will crash immediately with `ModuleNotFoundError`.

### ⚙️ How to Run the Project

1. **Clone the repository**
   Open your terminal/command prompt and run:

   ```bash
   git clone [https://github.com/your-username/Customer-Churn-Prediction.git](https://github.com/your-username/Customer-Churn-Prediction.git)
   cd Customer-Churn-Prediction
   ```

2. **Install Libraries**
   Run the following command to install all necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**
   Start the Flask server by running:

   ```bash
    python app.py
    ```

4. **Access the Web App** 
   Once the server starts, open your web browser and go to:

   ```bash
   http://127.0.0.1:5000/
   ```
## 📊 Model Performance
The project implements **SMOTEENN** to handle data imbalance effectively. The final XGBoost model demonstrated robust performance in distinguishing between churners and non-churners.

- **Accuracy**: ~95%
- **Key Churn Drivers**:
  - Contract Type (Month-to-month vs. Yearly)
  - Monthly Charges
  - Tenure (Length of relationship)

## 📄 Research Paper
This project is associated with the research paper titled:

> **"Customer Churn Prediction and Retention Strategies through Machine Learning, Chatbots, and Recommendation Systems"**

You can find the full PDF of the paper and the critical evaluation report in the **`Documentation/`** folder of this repository.

## 📜 License
This project is open-source and available for educational and research purposes.
