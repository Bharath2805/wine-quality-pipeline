import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from google.cloud import storage

import pickle
import os

# Create models directory
os.makedirs("../models", exist_ok=True)

# Load dataset
data = pd.read_csv('data/winequality-red.csv', sep=';')


# Split features and labels
X = data.drop('quality', axis=1)
y = data['quality']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
with open('models/wine_quality_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to ../models/wine_quality_model.pkl")
from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"✅ Uploaded {source_file_name} to gs://{bucket_name}/{destination_blob_name}")

# Upload to GCS after saving locally
upload_to_gcs('wine-quality-models-bucket', 'models/wine_quality_model.pkl', 'wine_quality_model.pkl')
