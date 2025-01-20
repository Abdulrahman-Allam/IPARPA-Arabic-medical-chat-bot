import streamlit as st

# Streamlit Page Configuration
st.set_page_config(
    page_title="احجز مع دكتور",
    page_icon="📅",
    layout="centered"
)

# Sidebar with Additional Information
# st.sidebar.image("https://via.placeholder.com/150")
st.sidebar.markdown(
    """<h2 style='color: #2E86C1;'>حجز موعد</h2>
    <p>يمكنك حجز موعد بسهولة مع أطباء متخصصين في مختلف المجالات.
    املأ البيانات المطلوبة أدناه واضغط على زر الحجز.</p>""",
    unsafe_allow_html=True
)

# Page Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>احجز مع دكتور</h1>", unsafe_allow_html=True)

# Form Inputs
with st.form("appointment_form"):
    name = st.text_input("اسمك", placeholder="أدخل اسمك هنا")
    age = st.number_input("سنك", min_value=0, step=1)
    phone = st.text_input("رقم تليفونك", placeholder="أدخل رقم هاتفك هنا")

    specialties = ["عظام", "قلب", "جراحة", "عيون", "باطنة", "أطفال"]
    specialty = st.selectbox("اختار التخصص اللي محتاجه", specialties)

    submitted = st.form_submit_button("احجز")

    if submitted:
        if name and phone and specialty:
            st.success(
                f"<div style='color: #117A65;'>تم استلام بياناتك بنجاح!<br><br>"
                f"<strong>الاسم:</strong> {name}<br>"
                f"<strong>السن:</strong> {age}<br>"
                f"<strong>رقم التليفون:</strong> {phone}<br>"
                f"<strong>التخصص:</strong> {specialty}</div>",
                unsafe_allow_html=True
            )
        else:
            st.error("من فضلك ادخل كل البيانات المطلوبة!", icon="⚠️")
