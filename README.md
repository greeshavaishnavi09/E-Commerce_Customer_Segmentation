# 🛍️ E-Commerce Customer Segmentation

An end-to-end **unsupervised machine learning project** that segments e-commerce customers using **RFM (Recency, Frequency, Monetary)** analysis.

The project compares multiple clustering algorithms and deploys the final model through **FastAPI and Streamlit**.

##Problem Statement

Identify meaningful customer segments based on purchasing behavior using unsupervised machine learning.

##Dataset

**UCI Online Retail Dataset**

- 541,909 transaction records
- 8 original features
- 4,338 customers after preprocessing

### RFM Features

- **Recency** – Days since the customer's last purchase
- **Frequency** – Number of unique invoices
- **Monetary** – Total customer spending

 Project Workflow

```text
Raw Data
   ↓
Data Ingestion
   ↓
Data Validation
   ↓
Data Cleaning & Transformation
   ↓
RFM Feature Engineering
   ↓
Log Transformation
   ↓
Standard Scaling
   ↓
Clustering Experiments
   ↓
Model Comparison
   ↓
Final GMM Model
   ↓
Prediction Pipeline
   ↓
FastAPI
   ↓
Streamlit

## 🤖 Models Used
- K-Means
- Hierarchical Clustering
- DBSCAN
- Gaussian Mixture Model (GMM)


## Models were compared using:
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score
- AIC / BIC for GMM


## 🏆 Final Model
   
   Gaussian Mixture Model (GMM)

Components: 2
Covariance Type: spherical
N-Init: 20


## Final Evaluation

Metric	                   Score

Silhouette Score	      0.4307
Davies-Bouldin Index	  0.9023
Calinski-Harabasz Score	  4300.76
AIC	                      32563.45
BIC	                      32620.83


## Customer Segments

Cluster	 Recency	Frequency	Monetary
0	      134.57	  1.68	     490.88
1	       26.28	  8.35	     4503.80


Cluster 0: Less recent, lower-frequency and lower-monetary customers.
Cluster 1: More recent, higher-frequency and higher-monetary customers.