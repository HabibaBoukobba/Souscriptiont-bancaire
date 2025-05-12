import streamlit as st
import numpy as np
import pickle

# Load the model
with open('randomForest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9; /* Fond gris clair */
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #f4f4f9;
    }
    h1, h2, h3 {
        color: #2a2a2a; /* Couleur des titres */
        font-weight: 600;
    }
    .stButton>button {
        background-color: #5c6bc0; /* Couleur des boutons */
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3e4a89; /* Couleur du bouton au survol */
    }
    .stSelectbox, .stNumberInput, .stTextInput {
        border-radius: 8px; /* Bordures arrondies des champs de saisie */
        border: 2px solid #ddd; /* Bordure claire */
        padding: 10px;
        margin-bottom: 15px;
        font-size: 14px;
    }
    .stSelectbox>div, .stNumberInput>div, .stTextInput>div {
        background-color: white;
        border-radius: 8px;
    }
    .stForm {
        background-color: #ffffff; /* Fond blanc pour le formulaire */
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .stAlert {
        border-radius: 8px; /* Bordures arrondies pour les messages de prédiction */
    }
    .stAlert>div {
        background-color: #ffcccb; /* Couleur douce pour les alertes */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title('Souscription à un dépôt bancaire')


with st.form(key='deposit'):
    # Features
    age = st.number_input('Age', min_value=18, max_value=100, value=30)
    
    job = st.selectbox('Job', ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management',
                                'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
    
    marital = st.selectbox('Marital Status', ['divorced', 'married', 'single'])

    education = st.selectbox('Education Level', ['primary', 'secondary', 'tertiary', 'unknown'])

    default = st.selectbox('Has Credit in Default?', ['No', 'Yes'])

    balance = st.number_input('Balance', min_value=0.0, max_value=300000.0, value=50000.0, step=100.0)

    housing = st.selectbox('Has Housing Loan?', ['No', 'Yes'])

    loan = st.selectbox('Has Personal Loan?', ['No', 'Yes'])

    contact = st.selectbox('Contact Communication Type', ['cellular', 'telephone', 'unknown'])

    day = st.number_input('Last Contact Day of the Month', min_value=1, max_value=31, value=15)

    month = st.selectbox('Last Contact Month', ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
    
    duration = st.number_input('Duration of Last Contact (seconds)', min_value=0, max_value=5000, value=300)

    campaign = st.number_input('Number of Contacts During Campaign', min_value=1, max_value=50, value=2)

    pdays = st.number_input('Days Since Last Contact', min_value=-1, max_value=1000, value=-1)  

    previous = st.number_input('Number of Contacts Before Campaign', min_value=0, max_value=100, value=1)

    poutcome = st.selectbox('Outcome of Previous Campaign', ['failure', 'nonexistent', 'success'])

    submit_button = st.form_submit_button(label='Predict')


if submit_button:
    # Encoding categorical variables
    job_map = {'admin.': 0, 'blue-collar': 1, 'entrepreneur': 2, 'housemaid': 3, 'management': 4,
                'retired': 5, 'self-employed': 6, 'services': 7, 'student': 8, 'technician': 9, 'unemployed': 10, 'unknown': 11}
    
    marital_map = {'divorced': 0, 'married': 1, 'single': 2}

    education_map = {'primary': 0, 'secondary': 1, 'tertiary': 2, 'unknown': 3}

    yes_no_map = {'Yes': 1, 'No': 0}

    contact_map = {'cellular': 0, 'telephone': 1, 'unknown': 2}
    
    month_map = {'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3, 'may': 4, 'jun': 5, 
                 'jul': 6, 'aug': 7, 'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11}
    
    poutcome_map = {'failure': 0, 'nonexistent': 1, 'success': 2}

    input_data = np.array([
        age,
        job_map[job],
        marital_map[marital],
        education_map[education],
        yes_no_map[default],
        balance,
        yes_no_map[housing],
        yes_no_map[loan],
        contact_map[contact],
        day,
        month_map[month],
        duration,
        campaign,
        pdays,
        previous,
        poutcome_map[poutcome]
    ]).reshape(1, -1)

    prediction = model.predict(input_data)


    if prediction[0] == 1:
        st.error("Le client est susceptible de SOUSCRIRE à un dépôt à terme.")

    else:
        st.success("Le client n'est PAS susceptible de souscrire à un dépôt à terme.")
