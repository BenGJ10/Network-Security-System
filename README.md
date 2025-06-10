# 🔐 Network Security System Project for Phishing Data

This project focuses on building a Network Security System that processes phishing data using ETL (Extract, Transform, Load) pipelines.

## 📌 Overview

The system is designed to identify and analyze phishing-related data through structured data workflows. It aims to automate the ingestion and processing of large datasets related to phishing activities for security analysis and detection.

## Workflow
![Workflow Diagram](images/workflow.png)

The core of this system is built around the ETL process:

## ⚙️ ETL Pipeline – Extract, Transform, Load

### 🔍 Extract
- Data is extracted from **CSV files** (currently local source, extendable to APIs/streams).
- Loaded into **Pandas DataFrames** and then converted to Python dictionary format for MongoDB ingestion.

### 🛠 Transform
- Data cleaning and structuring.
- Future scope: Feature engineering, advanced transformations, scaling, and encoding.

### ☁️ Load
- Loads data into a **MongoDB Atlas** cluster using secure TLS connection.
- MongoDB operations include:
  - Client creation via `.env` credentials
  - Database and collection access
  - Bulk insertion of records

**✅ Benefits**:
- Scalable, secure, and easy to monitor
- Modular and reusable design

---

## 📥 Data Ingestion

The **Data Ingestion** module fetches raw data and prepares it for further processing.

- Reads from CSV
- Performs **stratified train-test split**
- Saves artifacts in a structured directory
- Outputs metadata and paths via `DataIngestionArtifact`

**✅ Benefits**:
- Ensures reproducibility
- Traceable file-based artifacts
- Clean interface for pipeline integration

---

## ✅ Data Validation

The **Data Validation** module ensures input data quality and schema compliance.

### 🧬 Schema Validation
- Validates column count and names/types using a schema YAML file
- Ensures required numerical columns are present

### 📊 Statistical Drift Detection
- Uses **Kolmogorov–Smirnov test** to detect dataset drift
- Generates a detailed **drift report (YAML)**

### 📝 Logs & Artifacts
- Logs validation steps and errors
- Produces validated paths for next pipeline stages

**✅ Benefits**:
- Prevents pipeline failure due to corrupted input
- Ensures test/train consistency
- Drift detection increases model reliability

---

## 🔄 Data Transformation

This module prepares validated data for machine learning.

- Applies **KNN Imputation** (`KNNImputer`) for missing values
- Encodes labels (`-1` ➝ `0`)
- Uses a **Scikit-learn pipeline** for transformation
- Saves:
  - Processed **NumPy arrays**
  - The **transformer object** (joblib)

**✅ Benefits**:
- Clean and ready for ML models
- Stored transformation logic enables consistent inference
- Efficient for large datasets

---

## 🤖 Model Training

The **Model Trainer** selects and trains the best-performing model from multiple ML algorithms using hyperparameter tuning.

### 🧠 Supported Models
- Random Forest
- Decision Tree
- Gradient Boosting
- AdaBoost
- Logistic Regression

### 🛠 Evaluation
- Trains all models using **GridSearchCV** with predefined parameter grids
- Evaluates using classification metrics (e.g., F1 score, Precision, Recall)
- Logs performance for each model
- Selects the **best model** based on test set performance

### 📦 Output
- Saves the best model along with its preprocessor using `joblib`
- Returns a `ModelTrainerArtifact` containing:
  - Trained model path
  - Training and testing evaluation metrics

**✅ Benefits**:
- Automated model selection and evaluation
- Modular, configurable design
- Saves entire pipeline (model + preprocessing) for future inference

---

### 🧱 Modular Architecture

Every phase is broken into independent, testable, and reusable components.

- Configuration handled via `ConfigEntity` classes
- Data and metadata passed through structured `ArtifactEntity` classes

**🏗 Design Principles**:
- Maintainability
- Scalability
- Ease of debugging and monitoring

---
