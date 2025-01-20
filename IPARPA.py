import streamlit as st
import sys
import google.generativeai as genai

# Ensure UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Configure Gemini client
def initialize_gemini_client():
    genai.configure(api_key="AIzaSyCrfSGQ4rzgkb-698AI69k8NFb4-gTguiA")
    return genai.GenerativeModel("gemini-1.5-flash")

# Function to generate response from Gemini API
def generate_response(messages, model):
    try:
        # Combine messages into a single prompt (e.g., a conversation)
        prompt = "\n".join([
            f"{message['role']}: {message['content']}"
            for message in messages
        ])
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app setup
st.set_page_config(
    page_title="IPARPA - مساعد طبي",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.sidebar.image("https://via.placeholder.com/150", use_column_width=True)
st.sidebar.markdown(
    """<h2 style='color: #2E86C1;'>!IPARPAمرحبًا بك في </h2>
    <p style='color: white;'>
    نحن هنا لمساعدتك في الإجابة على استفساراتك الطبية.
    استخدم واجهة المحادثة أدناه للحصول على المساعدة.
    </p>""",
    unsafe_allow_html=True
)

st.markdown("""<style>.css-18e3th9 {padding: 1rem;}</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color: #2E86C1;'>IPARPA - مساعدك الطبي الذكي</h1>", unsafe_allow_html=True)

# Initialize chat session
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "انت مساعد طبي مصري ذكي, مبتتكلمش غير باللهجة العربية المصرية, بتساعد الناس في انك تجاوبهم على اسألتهم الطبية, ودايما لما يقولولك شكوتهم تقولهم الف سلامة او سلامتك وبعدين ترد عليهم بطريقة رسمية, وكمان تقولهم ايه التحاليل المناسبة اللي الفمروض يعملوها, وفي نهاية اجابتك دايما اسالهم هل تحب احجزلك لدكتور, اي سؤال ملوش علاقة بالطب اعتذر منه ومتجاوبش, ممكن ترد السلام او الترحاب مفيش مشاكل, كل اجوبتك قولها باللهجة المصرية بطريقة رسمية وبأدب"}    ]

# Display previous messages
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.chat_message('user').markdown(message['content'])
    elif message['role'] == 'assistant':
        st.chat_message('assistant').markdown(message['content'])

# Initialize the Gemini client once
if 'gemini_model' not in st.session_state:
    st.session_state.gemini_model = initialize_gemini_client()

# User input
prompt = st.chat_input("...اتفضل استفسارك")

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Check for specific command and redirect
    if prompt.strip() == "اه احجزلي":
        st.chat_message('assistant').markdown("...هيتم تحويلك لصفحة الحجز [اضغط هنا](./%D8%A7%D8%AD%D8%AC%D8%B2)")
    else:
        # Generate and display response
        with st.spinner("...تحليل"):
            response = generate_response(st.session_state.messages, st.session_state.gemini_model)
            st.chat_message('assistant').markdown(response)
            st.session_state.messages.append({'role': 'assistant', 'content': response})
