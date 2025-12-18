import streamlit as st
from app.prediction import make_prediction

def show_prediction_form(pipeline):
    """Displays the interactive prediction form"""
    
    st.title("🎯 Loan pre approval predictor")
    st.markdown("Complete the form below to get your personalized prediction")
    
    # for return in case of applicant income or loan amount 0 
    error_placeholder = st.empty()
    
    with st.form("prediction_form"):
        st.subheader("📝 Personal Information")
        
        # Form layout in columns
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender", options=["Male", "Female", "Prefer not to say"])
            married =  st.selectbox("Married", options=["Yes", "No", "Not Specified"])
            education =  st.selectbox("Education", options=["Graduate", "Not Graduate", "Not Specified"])
            dependents = st.number_input("Dependets", min_value=0, max_value=20, step=1)            
        with col2:
            applicantincome = st.number_input("Applicant Income", min_value=1, max_value=100000)
            self_employed =  st.selectbox("Self employed?", options=["Yes", "No"])
            credit_history =  st.selectbox("Do you have credit history?", options=[ "No","Yes"])
            coapplicantincome = st.number_input("Coapplicant Income", min_value=0, max_value=100000, value=0)
            
        
        loan_amount_term = st.slider("Loan amount term (in months)", 
                                     min_value=60, 
                                     max_value=480, 
                                     value=360, 
                                     step=60
                                     )   
        property_area = st.radio("Property Area", options=["Urban", "Semiurban", "Rural"])
        loanamount = st.number_input("Loan amount", min_value=1, max_value=700)
        
        # Submit button
        submitted = st.form_submit_button("🎯 Calculate Prediction", type="primary")
    
    # Handle form submission
    if submitted:
        # Create input dictionary
        if applicantincome == 0 or loanamount == 0:
            st.error("""
                     ❌ Error: 'Applicant Income' and 'Loan amount' must be 
                     greater than zero (0) to proceed with the calculation. 
                     Please correct the values.
                     """)
            return
        error_placeholder.empty()
        user_input = {            
            'Gender': (lambda x: 'DK' if x == 'Prefer not to say' else x)(gender),
            'Married': (lambda x: 'DK' if x == 'Not Specified' else x)(married),
            'Dependents': dependents,
            'Education': (lambda x: 'DK' if x == 'Not Specified' else x)(education),
            'Self_Employed': self_employed,            
            'ApplicantIncome': applicantincome,
            'CoapplicantIncome' : coapplicantincome,
            'LoanAmount' : loanamount,            
            'Loan_Amount_Term': loan_amount_term,
            'Credit_History': (lambda x: 1 if x == 'Yes' else 0)(credit_history),
            'Property_Area' : property_area,
         
            }
        # Make prediction
        label, prob = make_prediction(pipeline, user_input)
                   
        # Display results
        show_prediction_results(label, user_input, prob)
        

def show_prediction_results(prediction, user_input, prob=None):
    """Displays the prediction results in an attractive way"""
    
    st.success("✅ Prediction calculated successfully!")
    
    # Result section
    st.subheader("📊 Prediction Results")
    
    if prediction == 1:
        display_value = "Pre-Approved"
    elif prediction == 0:
        display_value = "Not Pre-Approved"
    
    # Main prediction 
    st.metric(
        label="Predicted Value", 
        value=display_value,
        delta=None  
    )
    
    
    # User input summary
    with st.expander("📋 Review Your Input"):
        review_col1, review_col2 = st.columns(2)
        with review_col1:
            for key in list(user_input.keys())[:len(user_input)//2]:
                st.write(f"**{key.title()}:** {user_input[key]}")
        with review_col2:
            for key in list(user_input.keys())[len(user_input)//2:]:
                st.write(f"**{key.title()}:** {user_input[key]}")
    
    # Interpretation guide
    with st.expander("💳 Important: Understanding Your Results"):
        st.markdown(
        """
        > **💳 NON-BINDING TENTATIVE RESULT**
        > 
        > Thank you for utilizing our credit analysis tool. Please be aware that the outcome provided by this online tool is **STRICTLY TENTATIVE** and for informational purposes only. It is based solely on the data you submitted and general market guidelines.
        >
        > This preliminary result does **NOT** constitute a final approval, a binding credit offer, or a formal commitment from any financial institution.
        >
        > **---**
        > 
        > **☝️ FINAL CREDIT DECISION WARNING:**
        > 
        > The final credit decision, including eligibility and loan terms, **must be officially processed and managed directly with the bank or the specific lending entity.** The bank will conduct its own comprehensive evaluation, which may lead to a different final outcome.
        > 
        > We highly recommend you contact your financial institution to proceed with the official application.
        """,
    
        )