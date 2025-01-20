import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

# Streamlit Page Configuration
st.set_page_config(
    page_title="أقرب صيدليات ليك",
    page_icon="💊",
    layout="wide"
)

# Sidebar with Instructions
# st.sidebar.image("https://via.placeholder.com/150", use_column_width=True)
st.sidebar.markdown(
    """<h2 style='color: #2E86C1;'>مرحبًا بك!</h2>
    <p>هنا يمكنك العثور على أقرب الصيدليات إلى موقعك الحالي.
    بمجرد تحميل الصفحة، سيتم عرض الصيدليات على الخريطة أدناه.</p>""",
    unsafe_allow_html=True
)

# Function to get user's coordinates
def get_user_location():
    api_key = "0b9602bbf8d645659bd4b84419c8f218"
    location_query = "Cairo"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location_query}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        coords = data['results'][0]['geometry']
        return coords['lat'], coords['lng']
    else:
        st.error("تعذر الحصول على الموقع. حاول مرة أخرى لاحقًا.")
        return None, None

# Function to get nearby pharmacies using Overpass API
def get_nearby_pharmacies(lat, lon, radius=60000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node
      ["amenity"="pharmacy"]
      (around:{radius},{lat},{lon});
    out body;
    """
    response = requests.get(overpass_url, params={"data": query})
    if response.status_code == 200:
        return response.json().get("elements", [])
    else:
        st.error("تعذر الحصول على بيانات الصيدليات. حاول مرة أخرى لاحقًا.")
        return []

# Page Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>أقرب صيدليات ليك</h1>", unsafe_allow_html=True)

latitude, longitude = get_user_location()
if latitude and longitude:
    # Fetch nearby pharmacies
    pharmacies = get_nearby_pharmacies(latitude, longitude)

    # Create Map
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Add user location to map
    folium.Marker(
        [latitude, longitude],
        tooltip="موقعك الحالي",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    # Add pharmacy locations to map
    for pharmacy in pharmacies:
        lat, lon = pharmacy.get("lat"), pharmacy.get("lon")
        name = pharmacy.get("tags", {}).get("name", "صيدلية غير معروفة")
        folium.Marker(
            [lat, lon],
            tooltip=name,
            icon=folium.Icon(color="purple", icon="plus-sign")
        ).add_to(m)

    # Display map
    st_folium(m, width=700, height=500)

    # Pharmacy List
    st.markdown("<h3 style='color: #8E44AD;'>قائمة الصيدليات</h3>", unsafe_allow_html=True)
    for pharmacy in pharmacies:
        name = pharmacy.get("tags", {}).get("name", "صيدلية غير معروفة")
        st.write(f"- {name}")
