import os
import time
from google import genai
import streamlit as st

# Streamlit Page Setup
st.set_page_config(page_title="AI Competitor Spy Engine", page_icon="🎯", layout="wide")

st.title("🎯 AI Competitor Spy & Strategy Engine")
st.caption("Competitors ki offers aur ads paste karein aur instant Counter-Strategy payein.")

# ----------------------------
# TOP HELP / GUIDE BUTTON (English & Urdu)
# ----------------------------
with st.expander("❓ Need Help? Click Here / Madad ke liye yahan click karein"):
    st.markdown("""
        ### 📖 How to Use This Tool (English Guide)
        1. **Enter API Key:** Paste your Google Gemini API Key in the left sidebar configuration box.
        2. **Enter Business Details:** Type your product or business name (e.g., *Leather Shoes Store*) and the competitor's name (optional).
        3. **Paste Competitor Offer:** Copy the competitor's ad text, social media caption, or discount offer and paste it into the offer text box.
        4. **Add Optional Notes:** If you have specific constraints like a tight profit margin or limited stock, write them in the optional extra info box.
        5. **Generate Strategy:** Click the **'Generate Counter-Strategy'** button to get a professional, zero-loss counter offer and ready-to-use ad copy in Roman Urdu.
        6. **Short Summary:** Use the 'Short' button for a quick summary of the generated strategy.
        
        ---
        
        ### 📖 اس ٹول کو کیسے استعمال کریں (اردو گائیڈ)
        1. **اے پی آئی کی درج کریں:** بائیں جانب سیٹنگز میں اپنی گوگل جیمنی اے پی آئی کی درج کریں۔
        2. **اپنا بزنس لکھیں:** اپنے برانڈ یا پروڈکٹ کا نام لکھیں (مثلاً *لییدر شوز سٹور*)۔
        3. **مخالف کی آفر پیسٹ کریں:** اپنے حریف (competitor) کا اشتہار یا آفر کا متن کاپی کرکے خانے میں پیسٹ کریں۔
        4. **اضافی معلومات (اختیاری):** اگر آپ کا پرافٹ کم ہے یا سٹاک محدود ہے، تو اسے اختیاری خانے میں لکھ سکتے ہیں۔
        5. **اسٹریٹجی بنائیں:** **'Generate Counter-Strategy'** کے بٹن پر کلک کریں تاکہ آپ کو رومن اردو میں بہترین اور منافع بخش جوابی آفر مل سکے۔
        6. **شارٹ سمری:** کم وقت کے لیے 'Short' بٹن دبائیں تاکہ فوری سمری مل سکے۔
        """, unsafe_allow_html=True)

# Session State Initializations
if "detailed_report" not in st.session_state:
    st.session_state.detailed_report = ""
if "short_report" not in st.session_state:
    st.session_state.short_report = ""

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password", help="Aap Google AI Studio se free key le sakte hain.")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    my_business = st.text_input("Aapka Product / Business Kya Hai?", placeholder="e.g. Premium Leather Wallets, Clothing Brand, Marketing Agency")
    competitor_name = st.text_input("Competitor Ka Naam (Optional):", placeholder="e.g. Brand X / Shop Y")

with col2:
    competitor_ad = st.text_area("Competitor Ki Offer / Ad Text / Post Caption Paste Karein:", placeholder="e.g. Flat 30% OFF on all Winter Jackets! Minimum order PKR 5000. Limited stock available!", height=130)

# Optional Extra Info Input
extra_info = st.text_area("📌 Extra Info / Special Notes (Optional):", placeholder="Yahan koi bhi aisi baat likhein jo aap strategy mein shamil karna chahte hon (e.g. 'Humara profit margin sirf 20% hai', 'Hum sirf Lahore mein deliver karte hain')", height=80)

# Run Analysis Button
if st.button("🚀 Generate Counter-Strategy", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar!")
    elif not my_business or not competitor_ad:
        st.warning("Please fill in the required input fields.")
    else:
        with st.spinner("Analyzing Competitor Strategy & Profit Margins..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are an expert E-commerce Business Consultant for local Pakistani brands.
                
                STRICT RULES:
                1. Write strictly in clear, easy Roman Urdu.
                2. NO FALSE ASSUMPTIONS: Do NOT claim customers are cancelling orders or hating the competitor unless mentioned in the text.
                3. Be realistic, factual, and direct based purely on the given offer text and extra notes.

                My Business: {my_business}
                Competitor Name: {competitor_name if competitor_name else "Competitor"}
                Competitor's Ad Text: "{competitor_ad}"
                Additional User Notes / Constraints: "{extra_info if extra_info else 'None provided'}"
                
                Provide a realistic strategic report in Markdown format:
                
                ### 1. 🔍 Competitor Offer Analysis
                Is offer ka direct structure aur terms kya hain?
                
                ### 2. ⚠️ Offer Ka Logical Gap / Friction Point
                Is offer mein konsa friction point ya limitation hai?
                
                ### 3. 🛡️ Aapka Winning Zero-Loss Counter-Strategy
                Ek aisi solid counter-offer jo extra notes (profit margin/stock limit) ko dhyaan mein rakhte hue profit safe rakhe.
                
                ### 4. 📢 Ready-to-Use Ad Copy
                2-line ki clean Roman Urdu Ad Copy.
                """

                # Using the exact recommended model gemini-3.6-flash
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                if response and response.text:
                    st.session_state.detailed_report = response.text
                    st.session_state.short_report = ""
                else:
                    st.error("Response object empty mila hai.")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display Detailed Output
if st.session_state.detailed_report:
    st.success("Analysis Complete!")
    st.markdown("---")
    st.markdown(st.session_state.detailed_report)
    
    st.markdown("---")
    if st.button("⚡ Short"):
        if not api_key:
            st.error("Please enter your Gemini API Key!")
        else:
            with st.spinner("Short summary ban rahi hai..."):
                try:
                    client = genai.Client(api_key=api_key)
                    short_prompt = f"""
                    Summarize the report strictly in **Roman Urdu** in UNDER 6 LINES.
                    Format:
                    • **Competitor Condition:** 
                    • **The Logical Gap:** 
                    • **Your Zero-Loss Offer:** 
                    • **Ad Copy:** 

                    Report:
                    {st.session_state.detailed_report}
                    """
                    short_res = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=short_prompt
                    )
                    if short_res and short_res.text:
                        st.session_state.short_report = short_res.text
                except Exception as err:
                    st.error(f"Summary Error: {str(err)}")

# Display Short Summary securely
if st.session_state.short_report:
    st.markdown("### 📋 Fact-Based Quick Summary")
    st.info(st.session_state.short_report)
