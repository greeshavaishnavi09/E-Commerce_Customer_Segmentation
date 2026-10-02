import streamlit as st
import requests
import pandas as pd


# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Segmentation",
    page_icon="🛍️",
    layout="centered"
)


# Application title
st.title("🛍️ E-Commerce Customer Segmentation")
st.write("Predict customer segments using RFM values.")


# FastAPI URL
API_URL = "http://127.0.0.1:8000/predict"


# Cluster profiles from the trained GMM
cluster_profiles = {
    0: {
        "Recency": 134.57,
        "Frequency": 1.68,
        "Monetary": 490.88
    },
    1: {
        "Recency": 26.28,
        "Frequency": 8.35,
        "Monetary": 4503.80
    }
}


# Customer RFM inputs
st.subheader("Enter Customer RFM")

recency = st.number_input(
    "Recency",
    min_value=0.0,
    value=25.0
)

frequency = st.number_input(
    "Frequency",
    min_value=1.0,
    value=8.0
)

monetary = st.number_input(
    "Monetary",
    min_value=1.0,
    value=4200.0
)


# Prediction button
if st.button("Predict Customer"):

    customer_data = {
        "recency": recency,
        "frequency": frequency,
        "monetary": monetary
    }

    try:

        response = requests.post(
            API_URL,
            json=customer_data
        )

        if response.status_code == 200:

            result = response.json()

            cluster = result["cluster"]
            membership_probability = result["membership_probability"]

            # Prediction result
            st.success("Prediction completed successfully!")

            st.subheader("Prediction Result")

            st.write(f"**Customer Cluster:** {cluster}")

            st.write(
                f"**Membership Probability:** "
                f"{membership_probability:.2%}"
            )


            # Customer profile
            st.subheader("Customer Profile")

            if cluster == 0:

                st.write(
                    "**Cluster 0 — Lower-engagement segment**"
                )

                st.write(
                    "- Customers purchase less recently"
                )

                st.write(
                    "- Lower purchase frequency"
                )

                st.write(
                    "- Lower monetary contribution"
                )

            else:

                st.write(
                    "**Cluster 1 — Higher-engagement segment**"
                )

                st.write(
                    "- Customers purchase more recently"
                )

                st.write(
                    "- Higher purchase frequency"
                )

                st.write(
                    "- Higher monetary contribution"
                )


            # Cluster comparison
            st.subheader("Customer vs Cluster Profile")

            profile = cluster_profiles[cluster]

            comparison = pd.DataFrame({
                "Metric": [
                    "Recency",
                    "Frequency",
                    "Monetary"
                ],
                "Customer": [
                    recency,
                    frequency,
                    monetary
                ],
                "Cluster Profile": [
                    profile["Recency"],
                    profile["Frequency"],
                    profile["Monetary"]
                ]
            })

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )


            # Business interpretation
            st.subheader("Business Interpretation")

            if cluster == 0:

                st.write(
                    "This customer belongs to a segment with "
                    "higher recency, lower purchase frequency, "
                    "and lower monetary contribution."
                )

            else:

                st.write(
                    "This customer belongs to a segment with "
                    "lower recency, higher purchase frequency, "
                    "and higher monetary contribution."
                )


        else:

            st.error(
                f"FastAPI returned an error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure the FastAPI server is running."
        )