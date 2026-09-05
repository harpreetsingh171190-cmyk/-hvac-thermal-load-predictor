import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="HVAC Thermal Load Predictor", page_icon="🏢", layout="centered")

st.title("🏢 HVAC Thermal Load Predictor")
st.markdown("Predict the **Heating** and **Cooling Load** of a building based on its architectural design. Adjust parameters on the sidebar to see real-time predictions!")

@st.cache_resource
def load_model():
    try:
        return joblib.load('hvac_multi_model.pkl')
    except:
        return None

model = load_model()

st.sidebar.header("⚙️ Building Parameters")
relative_compactness = st.sidebar.slider("Relative Compactness", 0.62, 0.98, 0.75, 0.01)
surface_area = st.sidebar.slider("Surface Area", 514.5, 808.5, 650.0, 0.5)
wall_area = st.sidebar.slider("Wall Area", 245.0, 416.5, 300.0, 0.5)
roof_area = st.sidebar.slider("Roof Area", 110.25, 220.50, 150.0, 0.25)
overall_height = st.sidebar.selectbox("Overall Height (m)", options=[3.5, 7.0])
orientation = st.sidebar.selectbox("Orientation", options=[2, 3, 4, 5], format_func=lambda x: {2: "North", 3: "East", 4: "South", 5: "West"}[x])
glazing_area = st.sidebar.selectbox("Glazing Area (%)", options=[0.0, 0.1, 0.25, 0.40])
glazing_area_dist = st.sidebar.slider("Glazing Area Distribution", 0, 5, 2, 1)

if st.button("Predict Thermal Loads 🚀"):
    if model is not None:
        input_features = np.array([[relative_compactness, surface_area, wall_area, roof_area, overall_height, orientation, glazing_area, glazing_area_dist]])
        prediction = model.predict(input_features)
        
        st.markdown("### 📊 Predicted Results")
        col1, col2 = st.columns(2)
        col1.metric(label="🔥 Heating Load", value=f"{prediction[0][0]:.2f} kWh/m²")
        col2.metric(label="❄️ Cooling Load", value=f"{prediction[0][1]:.2f} kWh/m²")
        st.success("✅ Prediction successful using Random Forest ML Model!")
    else:
        st.error("Model file missing!")
