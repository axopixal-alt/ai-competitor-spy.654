import os
import time
from google import genai
import streamlit as st

# Streamlit Page Setup
st.set_page_config(
    page_title="AI Competitor Spy Engine", page_icon="🎯", layout="wide"
)

# HIDE STREAMLIT DEPLOY BUTTON & EXTRA MENUS VIA CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🎯 AI Competitor Spy & Strategy Engine")
st.caption(
    "Competitors ki offers aur ads paste karein aur instant Counter-Strategy payein."
)

# ----------------------------
# TOP HELP / GUIDE BUTTON (English & Urdu) with WhatsApp Support
# ----------------------------
with st.expander("❓ Need Help? Click Here / Madad ke liye yahan click karein"):
    st.markdown(
        """
        ### 📖 How to Use This Tool (English Guide)
        1. **Enter API Key:** Paste your Google Gemini API Key in the box below.
        2. **Enter Business Details:** Type your product or business name (e.g., *Leather Shoes Store*) and the competitor's name (optional).
        3. **Paste Competitor Offer:** Copy the competitor's ad text, social media caption, or discount offer and paste it into the offer text box.
        4. **Add Optional Notes:** If you have specific constraints like a tight profit margin or limited stock, write them in the optional extra info box.
        5. **Generate Strategy:** Click the **'Generate Counter-Strategy'** button to get a professional, zero-loss counter offer and ready-to-use ad copy in Roman Urdu.
        6. **Short Summary & Chat:** Use the 'Short' button for a quick summary or use the chatbox below to ask AI for alternative strategies if you are worried about profit loss.
        
        ---
        
        ### 📖 اس ٹول کو کیسے استعمال کریں (اردو گائیڈ)
        1. **اے پی آئی کی درج کریں:** نیچے دیے گئے خانے میں اپنی گوگل جیمنی اے پی آئی کی درج کریں۔
        2. **اپنا بزنس لکھیں:** اپنے برانڈ یا پروڈکٹ کا نام لکھیں (مثلاً *لییدر شوز سٹور*)۔
        3. **مخالف کی آفر پیسٹ کریں:** اپنے حریف (competitor) کا اشتہار یا آفر کا متن کاپی کرکے خانے میں پیسٹ کریں۔
        4. **اضافی معلومات (اختیاری):** اگر آپ کا پرافٹ کم ہے یا سٹاک محدود ہے، تو اسے اختیاری خانے میں لکھ سکتے ہیں۔
        5. **اسٹریٹجی بنائیں:** **'Generate Counter-Strategy'** کے بٹن پر کلک کریں تاکہ آپ کو رومن اردو میں بہترین اور منافع بخش جوابی آفر مل سکے۔
        6. **شارٹ سمری اور چیٹ:** کم وقت کے لیے 'Short' بٹن دبائیں یا نیچے چیٹ باکس میں حریف کی آفر سے متعلق مزید سوالات پوچھیں۔
        
        <br>
        <b>💡 Need Support?</b> Agar koi baat samajh na aaye ya koi masla ho, toh aap hamari support team ko is WhatsApp number par rabta kar sakte hain: <b style="color: #60a5fa;">03278509578</b>
        """,
        unsafe_allow_html=True,
    )

# Session State Initializations
if "detailed_report" not in st.session_state:
    st.session_state.detailed_report = ""
if "short_report" not in st.session_state:
    st.session_state.short_report = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# API Key Input Box on Main Screen
api_key = st.text_input(
    "🔑 Enter Your Google Gemini API Key:",
    type="password",
    placeholder="AI Studio se free key yahan paste karein...",
    help="Aap Google AI Studio se free key le sakte hain.",
)

st.markdown("---")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    my_business = st.text_input(
        "Aapka Product / Business Kya Hai?",
        placeholder="e.g. Premium Leather Wallets, Clothing Brand, Marketing Agency",
    )
    competitor_name = st.text_input(
        "Competitor Ka Naam (Optional):", placeholder="e.g. Brand X / Shop Y"
    )

with col2:
    competitor_ad = st.text_area(
        "Competitor Ki Offer / Ad Text / Post Caption Paste Karein:",
        placeholder="e.g. Flat 30% OFF on all Winter Jackets! Minimum order PKR 5000. Limited stock available!",
        height=130,
    )

# Optional Extra Info Input
extra_info = st.text_area(
    "📌 Extra Info / Special Notes (Optional):",
    placeholder="Yahan koi bhi aisi baat likhein jo aap strategy mein shamil karna chahte hon (e.g. 'Humara profit margin sirf 20% hai', 'Hum sirf Lahore mein deliver karte hain')",
    height=80,
)


# Safe Execution Function using latest stable models
def call_gemini_safely(client, prompt_text):
    models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash"]
    last_error = ""
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name, contents=prompt_text
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = str(e)
            continue
    return f"Asli Error yeh hai: {last_error}"


# Run Analysis Button
if st.button("🚀 Generate Counter-Strategy", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the box above!")
    elif not my_business or not competitor_ad:
        st.warning("Please fill in the required input fields.")
    else:
        with st.spinner("Analyzing Competitor Strategy & Profit Margins..."):
            try:
                client = genai.Client(api_key=api_key.strip())

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

                result_text = call_gemini_safely(client, prompt)
                st.session_state.detailed_report = result_text
                st.session_state.short_report = ""
                st.session_state.chat_history = [
                    {
                        "role": "model",
                        "text": f"Mene aapke business ({my_business}) aur di gayi extra details ke mutabiq strategy tayar kar di hai! Agar mazeed koi sawal ho ya help chahiye ho, toh yahan pooch sakte hain ya WhatsApp (03278509578) par rabta karein.",
                    }
                ]

            except Exception as e:
                st.error(f"Error occurred: {e}")

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
                client = genai.Client(api_key=api_key.strip())
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
                st.session_state.short_report = call_gemini_safely(
                    client, short_prompt
                )

# Display Short Summary
if st.session_state.short_report:
    st.markdown("### 📋 Fact-Based Quick Summary")
    st.info(st.session_state.short_report)

# Interactive Strategy Chatbot
if st.session_state.detailed_report:
    st.markdown("---")
    st.markdown("### 💬 AI Strategy Advisor Chat")
    st.caption(
        "Agar is strategy mein mazeed changes chahiye ya koi naya constraint add karna hai, toh yahan likhein!"
    )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["text"])

    user_query = st.chat_input(
        "e.g., 'Ab isme free delivery ki shart add karke naya idea do'"
    )

    if user_query:
        if not api_key:
            st.error("Please enter your Gemini API Key!")
        else:
            st.session_state.chat_history.append(
                {"role": "user", "text": user_query}
            )
            with st.chat_message("user"):
                st.write(user_query)

            with st.chat_message("assistant"):
                with st.spinner("Updated profit-safe alternative socha ja raha hai..."):
                    client = genai.Client(api_key=api_key.strip())

                    chat_prompt = f"""
                    You are an expert E-commerce Profit Strategist helping a Pakistani local brand owner.
                    
                    CONTEXT:
                    - User's Business: {my_business}
                    - Competitor Ad: {competitor_ad}
                    - Extra Notes Provided: {extra_info if extra_info else 'None'}
                    - Original Report: {st.session_state.detailed_report}
                    
                    USER CONCERN / NEW REQUEST:
                    "{user_query}"
                    
                    INSTRUCTION:
                    Answer strictly in **Roman Urdu**. Give concrete, practical, low-risk alternatives that respect any constraints or extra notes mentioned by the user while beating the competitor.
                    """

                    ai_reply = call_gemini_safely(client, chat_prompt)
                    st.write(ai_reply)

                    st.session_state.chat_history.append(
                        {"role": "model", "text": ai_reply}
                    )
