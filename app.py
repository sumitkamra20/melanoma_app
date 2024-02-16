import streamlit as st
import requests

# Streamlit UI
st.title("Melanoma Prediction App")

# File uploader for image
uploaded_files = st.file_uploader("Upload 1 to 3 images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Check if the number of uploaded files is within the desired range
if uploaded_files is not None and len(uploaded_files) >= 1 and len(uploaded_files) <= 3:
    # Create a layout with columns for each image and its prediction outcome
    col_count = len(uploaded_files)
    cols = st.columns(col_count)

    # Make a request to the FastAPI server for each uploaded image
    for idx, uploaded_file in enumerate(uploaded_files):
        with cols[idx]:
            # Display the uploaded image
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=150, width=150)

            # Make a request to the FastAPI server
            #url = "http://127.0.0.1:8000/predict"
            url ='https://melanoma-image-4kjxorxgpq-as.a.run.app/predict'
            files = {"image": uploaded_file}
            response = requests.post(url, files=files)

            # Display the prediction outcome
            if response.status_code == 200:
                result = response.json()["outcome"]
                mal_prob_pct = round(result['malignant_probability']*100, 1)
                benign_prob_pct = round(result['benign_probability']*100, 1)
                st.write("Prediction Outcome:")

                # Check if malignant probability is greater than 25%
                if result['malignant_probability'] > 0.25:
                    st.write(f"Malignant Probability: <span style='color:red'>{mal_prob_pct:.1f}% &#9888;</span>", unsafe_allow_html=True)
                else:
                    st.write(f"Benign Probability: <span style='color:green'>{benign_prob_pct:.1f}% &#10004;</span>", unsafe_allow_html=True)
            else:
                st.error(f"Prediction failed for {uploaded_file.name}. Server returned status code: {response.status_code}")
else:
    st.warning("Please upload between 1 and 3 images.")
