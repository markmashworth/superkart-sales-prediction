import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask("SuperKart Sales Predictor")

# Load the trained SuperKart sales model (preprocessing + Random Forest pipeline)
model = joblib.load("superkart_sales_model_v1_0.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint to predict sales for a single product/store combination
@app.post('/v1/sales')
def predict_sales():
    # Get JSON data from the request
    product_data = request.get_json()

    # Extract the relevant features from the input data, in the order the model expects
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_Type': product_data['Product_Type'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Store_Age': product_data['Store_Age'],
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_Product_Store_Sales_Total': prediction})

# Define an endpoint to predict sales for a batch of product/store combinations
@app.post('/v1/salesbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_Product_Store_Sales_Total'] = predictions

    # Convert results to a list of dictionaries
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
