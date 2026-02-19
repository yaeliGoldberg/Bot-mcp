import streamlit as st
from Agent import agent

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳")

st.title("🍳 AI Recipe Generator")
st.write("Enter your products and choose difficulty level")

# קלט מוצרים
products_input = st.text_input(
    "Products (comma separated)",
    placeholder="milk, cheese, eggs"
)

# בחירת רמת קושי
level = st.selectbox(
    "Difficulty level",
    ["easy", "medium", "hard"]
)

# כפתור שליחה
if st.button("Generate Recipe"):
    if not products_input:
        st.warning("Please enter at least one product.")
    else:
        products = [p.strip() for p in products_input.split(",")]

        request_data = {
            "products": products,
            "level": level
        }

        with st.spinner("Generating recipe..."):
            response = agent(request_data)

        st.success("Recipe ready!")
        st.write(response)
