# 🛍️ E-Commerce Customer Segmentation

An end-to-end **unsupervised machine learning project** that segments e-commerce customers using **RFM (Recency, Frequency, Monetary)** analysis.

The project compares multiple clustering algorithms and exposes the final model through **FastAPI** and an interactive **Streamlit** application.

## 📌 Problem Statement

Identify meaningful customer segments based on purchasing behavior using unsupervised machine learning.

## 📊 Dataset

**UCI Online Retail Dataset**

- 541,909 transaction records
- 8 original features
- 4,338 customers after preprocessing

### RFM Features

- **Recency** – Days since the customer's last purchase
- **Frequency** – Number of unique invoices
- **Monetary** – Total customer spending


## 🤖 Models Used

- K-Means
- Hierarchical Clustering
- DBSCAN
- Gaussian Mixture Model (GMM)

### Model Evaluation

The clustering models were compared using:

- Silhouette Score ↑
- Davies-Bouldin Index ↓
- Calinski-Harabasz Score ↑
- AIC ↓
- BIC ↓

## 🏆 Final Model

**Gaussian Mixture Model (GMM)**

Components       : 2
Covariance Type  : spherical
N-Init           : 20
Random State     : 42


### Final Evaluation

 Metric                        Score 

| Silhouette Score           | 0.4307 |
| Davies-Bouldin Index       | 0.9023 |
| Calinski-Harabasz Score    | 4300.76 |
| AIC                        | 32563.45 |
| BIC                        | 32620.83 |

## 👥 Customer Segments

| Cluster | Recency | Frequency | Monetary | Customers |

| 0       | 134.57  | 1.68      | 490.88   | 2,654     |
| 1       | 26.28   | 8.35      | 4503.80  | 1,684     |

### Cluster 0 — Lower-Engagement Segment

Customers with:

- Higher recency
- Lower purchase frequency
- Lower monetary contribution

### Cluster 1 — Higher-Engagement Segment

Customers with:

- Lower recency
- Higher purchase frequency
- Higher monetary contribution

## 🔮 Prediction Pipeline

The trained GMM model can predict the segment of a new customer using RFM values.

Customer RFM
     ↓
Log Transformation
     ↓
Saved StandardScaler
     ↓
Saved GMM Model
     ↓
Predicted Cluster
     ↓
Membership Probability


Example:

Recency    = 25
Frequency  = 8
Monetary   = 4200

Predicted Cluster = 1
Membership Probability ≈ 99.98%


> Membership probability represents the GMM probability assigned to the predicted cluster. It is not classification accuracy.

## 🌐 Application

### FastAPI

The FastAPI backend provides a prediction endpoint:

POST /predict


Example request:

json
{
    "recency": 25,
    "frequency": 8,
    "monetary": 4200
}


Example response:

json
{
    "cluster": 1,
    "membership_probability": 0.9997639168360254
}


Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Streamlit

The Streamlit application allows users to:

- Enter customer RFM values
- Predict the customer segment
- View membership probability
- View the customer profile
- Compare customer RFM with the cluster profile
- View the business interpretation


## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
- FastAPI
- Pydantic
- Uvicorn
- Streamlit
- Joblib
- YAML


###  Start FastAPI

uvicorn api.main:app --reload


Open Swagger:

http://127.0.0.1:8000/docs


###  Start Streamlit

Open another terminal:

conda activate clust
streamlit run app.py

Open:

http://localhost:8501


