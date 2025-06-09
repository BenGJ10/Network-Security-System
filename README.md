# Network Security System Project for Phishing Data

This project focuses on building a Network Security System that processes phishing data using ETL (Extract, Transform, Load) pipelines.

## 📌 Overview

The system is designed to identify and analyze phishing-related data through structured data workflows. It aims to automate the ingestion and processing of large datasets related to phishing activities for security analysis and detection.

## Workflow
![Workflow Diagram](images/workflow.png)

### ⚙️ Know about ETL Pipelines

The core of this system is built around the ETL process:

### Extract
- Data is extracted from **CSV files** (currently from a file source, can be extended to APIs or real-time feeds).
- The CSV is read into a **Pandas DataFrame** and converted into a JSON-like format (Python dictionaries) for further use.

### Transform
- Data is cleaned and structured into a format suitable for insertion into **MongoDB**.
- Future transformation logic (e.g., feature engineering, preprocessing) will be integrated here.

### Load
- Data is loaded into a **MongoDB Atlas** cluster.
- The connection uses secure TLS (SSL) via the `certifi` CA bundle and a `.env` configuration for credentials.
- The MongoDB insertion logic handles:
  - Creating a client.
  - Connecting to a specific **database** and **collection**.
  - Uploading all records from the DataFrame.

This modular pipeline ensures data consistency, scalability, and ease of monitoring.

---

### Data Ingestion

The **Data Ingestion** module is responsible for fetching raw data and preparing it for processing:

- Reads data from a **CSV file source**.
- Splits the data into **training** and **testing** sets using stratified sampling .
- Saves the split data into organized folders within an **Artifacts** directory for pipeline reproducibility.
- Generates metadata such as file paths for downstream modules to consume.
- Maintains modular design through configuration and entity classes (`DataIngestionConfig`, `DataIngestionArtifact`).

**Key Benefits:**
- Ensures reproducibility and traceability of data sources.
- Modularized using configuration and artifact classes for flexible integration.

---

### Data Validation

The **Data Validation** component ensures the integrity, structure, and quality of ingested data:

- **Schema Validation**:
  - Compares the number of columns and column names/types against a predefined schema YAML file.
  - Checks whether all expected **numerical columns** are present.

- **Statistical Validation**:
  - Uses the **Kolmogorov-Smirnov test** to detect **dataset drift** between training and testing data.
  - Generates a **drift report YAML file** to document any statistical deviations.

- **Validated Output**:
  - If validation is successful, the train/test files are marked as valid and passed to the next stage.
  - Logs are generated at each step to capture any anomalies or validation failures.

**Key Benefits:**
- Prevents broken pipelines due to malformed data.
- Captures distributional drift between training and testing datasets.
- Facilitates auditability with automated drift reports and schema checks.

---

###  Data Transformation

The **Data Transformation** module processes validated data and prepares it for modeling or analytics:

- Applies **KNN Imputation** (`sklearn.impute.KNNImputer`) to handle missing values in numerical columns.
- Separates input features from the **target column**.
  - Converts target labels from `-1` to `0`.
- Wraps the imputation step in a **Scikit-learn Pipeline** for modular transformation.
- Saves:
  - The transformed data as **NumPy arrays** for modeling input.
  - The **transformation object (pipeline)** using `joblib` for consistent use in inference pipelines.

**Key Benefits:**
- Makes data ML-ready by ensuring missing value handling is consistent and encapsulated.
- Stores transformation logic for future inference consistency.
- Scales well with increasing data size due to use of NumPy arrays.


## Modular Design

Each phase of the pipeline is **encapsulated in reusable, testable components**. All data exchange between components happens via structured **Artifact** and **Config** classes, promoting:

- Scalability
- Debuggability
- Maintainability

---

## Upcoming Features

- Model training and evaluation.
- CI/CD pipeline with GitHub Actions.
- Integration with AWS cloud storage.
- Real-time streaming ingestion.
---
