import streamlit as st
import pandas as pd
import os
import urllib.parse
import plotly.express as px
import base64

# ==========================================
# 1. PREMIUM CONFIG & DESIGN
# ==========================================
st.set_page_config(page_title="TNEA Elite AI 2026", layout="wide", page_icon="🎓")

# FIXED LOCAL PATH: Change this path to your actual image location
LOCAL_BG_PATH = r"D:\TNEA final project\avs.jpg"
DATA_PATH = r"D:\TNEA final project\data-4.csv"

# Function to encode local image for CSS background
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_base64 = get_base64(LOCAL_BG_PATH)
if bg_base64:
    app_bg = f"url('data:image/jpeg;base64,{bg_base64}')"
else:
    app_bg = "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)" # Fallback

# CSS for Split Screen, Glassmorphism, and Dark Image Cards
st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{
        background: {app_bg};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Overlay for readability */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.6); /* Darker overlay to combat white backgrounds */
        backdrop-filter: blur(5px);
        z-index: -1;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 2px solid #fbbf24;
    }}

    /* Title Styling */
    .main-title {{
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: left;
        font-size: 3.5rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* === NEW: Generic Glass Card for Info Pages & Chat === */
    .glass-card {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        color: #f8fafc;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
    }}
    
    .glass-card h3, .glass-card h4 {{ color: #fbbf24; margin-top: 0; }}
    .glass-card p, .glass-card li {{ color: #e2e8f0; font-size: 16px; line-height: 1.6; }}

    /* Fix Chatbot bubbles to be dark cards */
    [data-testid="stChatMessage"] {{
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}

    /* College Card */
    .college-card {{
        position: relative;
        background: rgba(2, 6, 23, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 5px solid #fbbf24;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        overflow: hidden;
        transition: transform 0.3s, background 0.3s;
    }}
    
    .college-card:hover {{
        transform: translateY(-5px);
        border-left: 5px solid #22c55e;
        background: rgba(2, 6, 23, 0.95);
    }}

    .college-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0.25; 
        mix-blend-mode: overlay;
        z-index: 0;
    }}

    .card-content {{ position: relative; z-index: 1; }}
    .card-content h3 {{ color: #fbbf24 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.9); }}
    .card-content p {{ color: #f8fafc !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9); }}
    .card-content b {{ color: #38bdf8 !important; }}

    .btn-link {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        margin-right: 10px;
        margin-top: 15px;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}
    .btn-map {{ background: #2563eb; color: white !important; }}
    .btn-web {{ background: #fbbf24; color: black !important; }}
    .btn-map:hover {{ background: #1d4ed8; }}
    .btn-web:hover {{ background: #f59e0b; }}
    
    /* Make standard st.write text white to avoid blending into bright backgrounds */
    p, li, span, label {{ color: #f8fafc; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE
# ==========================================
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame() 

df = load_data()

# ==========================================
# 3. NAVIGATION
# ==========================================
st.sidebar.markdown("<h1 style='text-align:center; color:#fbbf24;'>✨ TNEA ELITE 4.0</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("EXPLORE", ["🎯 AI Predictor", "ℹ️ TNEA Master Guide", "🤖 Counselor Bot", "🏛️ College Directory"])

# ==========================================
# PAGE 1: AI PREDICTOR
# ==========================================
if page == "🎯 AI Predictor":
    st.markdown("<h1 class='main-title'>Smart College Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>Enter your marks to find matching colleges. Background images showcase campus vibes!</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        u_cutoff = st.number_input("Your TNEA Cutoff", 70.0, 200.0, 175.0)
    with col2:
        u_cat = st.selectbox("Community", sorted(df["Category"].unique()) if not df.empty else ["OC"])
    with col3:
        u_dist = st.multiselect("Select Districts", sorted(df["District"].unique()) if not df.empty else [])
    
    u_course = st.multiselect("Select Preferred Courses", sorted(df["Course"].unique()) if not df.empty else [])

    if st.button("🚀 PREDICT TOP COLLEGES"):
        filtered = df[df["Category"] == u_cat]
        if u_dist: filtered = filtered[filtered["District"].isin(u_dist)]
        if u_course: filtered = filtered[filtered["Course"].isin(u_course)]
        
        filtered['Diff'] = filtered['Cutoff'] - u_cutoff
        results = filtered[filtered['Diff'] <= 5].sort_values(by='Cutoff', ascending=False).head(10)

        if not results.empty:
            for _, row in results.iterrows():
                chance = "HIGH CHANCE" if u_cutoff >= row['Cutoff'] else "COMPETITIVE"
                badge_color = "#22c55e" if chance == "HIGH CHANCE" else "#eab308"
                
                search_query = urllib.parse.quote(f"{row['College_Name']} {row['District']}")
                map_url = f"https://www.google.com/maps/search/{search_query}"
                web_url = f"https://www.google.com/search?q={search_query}+official+website"

                st.markdown(f"""
                <div class="college-card">
                    <div class="card-content">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="margin:0; font-size: 22px;">{row['College_Name']}</h3>
                            <span style="background:{badge_color}; color:black; padding:5px 15px; border-radius:20px; font-weight:bold;">{chance}</span>
                        </div>
                        <p style="margin: 10px 0; font-size: 16px;">
                            📍 District: <b>{row['District']}</b>  |  📚 Course: <b>{row['Course']}</b>  |  📊 Prev. Cutoff: <b>{row['Cutoff']}</b>
                        </p>
                        <a href="{map_url}" target="_blank" class="btn-link btn-map">📍 View on Maps</a>
                        <a href="{web_url}" target="_blank" class="btn-link btn-web">🌐 College Website</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # --- NEW: PIE CHART AT THE BOTTOM ---
            st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin-top: 40px;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#fbbf24; text-shadow: 2px 2px 5px black;'>📊 High Chance Colleges Distribution</h2>", unsafe_allow_html=True)
            
            # Create a Pie Chart based on the top results 
            fig = px.pie(
                results, 
                names='College_Name', 
                values='Cutoff', 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="white"),
                showlegend=False # Hiding legend to save space, data shows on hover
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No matches found. Try widening your filters.")

# ==========================================
# PAGE 2: TNEA MASTER GUIDE
# ==========================================
elif page == "ℹ️ TNEA Master Guide":
    st.markdown("<h1 class='main-title'>TNEA 2026 Master Guide</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧮 Cutoff Formula", "🛡️ Reservation", "📅 Timeline", "📜 Documents", "🎥 Video Guides"])
    
    with tab1:
        st.markdown("""
        <div class="glass-card">
            <h3>How to Calculate Your Cutoff (Out of 200)</h3>
            <ul>
                <li><b>Mathematics:</b> Convert your mark to 100.</li>
                <li><b>Physics:</b> Divide your mark by 2 (Max 50).</li>
                <li><b>Chemistry:</b> Divide your mark by 2 (Max 50).</li>
                <li><b>Total:</b> Add them up!</li>
            </ul>
            <p style="color:#38bdf8;"><i>Example: If you scored Maths: 90, Physics: 80, Chemistry: 80.<br>Cutoff = 90 + (80/2) + (80/2) = <b>170 / 200</b>.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            <div class="glass-card">
                <h3>General Quota</h3>
                <ul>
                    <li><b>OC:</b> 31.0%</li>
                    <li><b>BC:</b> 26.5%</li>
                    <li><b>BCM:</b> 3.5%</li>
                    <li><b>MBC & DNC:</b> 20.0%</li>
                    <li><b>SC:</b> 15.0% | <b>SCA:</b> 3.0% | <b>ST:</b> 1.0%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown("""
            <div class="glass-card" style="border-left-color: #22c55e;">
                <h3>🏫 7.5% Government School Quota</h3>
                <p>A horizontal reservation of 7.5% is provided for students who studied from <b>6th to 12th standard</b> in Tamil Nadu Government Schools.</p>
                <p><b>Benefits:</b> Complete tuition fee, hostel fee, and counseling fee waiver!</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
            <h3>The Counseling Journey</h3>
            <ol>
                <li><b>Notification & Registration:</b> Usually begins in May.</li>
                <li><b>Certificate Verification:</b> Done online at TFC centers.</li>
                <li><b>Rank List Release:</b> A general and community rank is published.</li>
                <li><b>Counseling Rounds:</b> Based on rank, students are called in 3-4 rounds.</li>
                <li><b>Choice Filling:</b> You have 3 days to add as many colleges as you want.</li>
                <li><b>Tentative Allotment:</b> Confirm, Accept & Upward, or Decline.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with tab4:
        st.markdown("""
        <div class="glass-card">
            <h3>Keep These Ready (Originals & Copies)</h3>
            <ul>
                <li>10th and 12th Marksheets</li>
                <li>Transfer Certificate (TC)</li>
                <li>Community Certificate</li>
                <li>Nativity Certificate (If studied outside TN for any duration between 8th-12th)</li>
                <li>First Graduate Certificate / Joint Declaration (For tuition fee waiver)</li>
                <li>Income Certificate (If applicable for scholarships)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with tab5:
        st.markdown("<div class='glass-card'><h3>Helpful YouTube Guides</h3><p>Watch these videos for step-by-step TNEA counseling procedures.</p></div>", unsafe_allow_html=True)
        # Note: Swap these URL strings with actual helpful TNEA videos you want to feature
        colA, colB = st.columns(2)
        with colA:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Replace URL
        with colB:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Replace URL

# ==========================================
# PAGE 3: COUNSELOR BOT
# ==========================================
elif page == "🤖 Counselor Bot":
    st.markdown("<h1 class='main-title'>AI Admissions Expert</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>Chat with our AI to clear up your TNEA doubts instantly.</div>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Vanakkam! Ask me anything about TNEA cutoffs, counseling rounds, or document verification!"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask about Fees, Quota, First Graduate..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        reply = "That's a great question! Make sure to check the 'TNEA Master Guide' tab for detailed breakdowns, or ask me specifically about 'Cutoff calculation' or 'Required documents'."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ==========================================
# PAGE 4: COLLEGE DIRECTORY
# ==========================================
elif page == "🏛️ College Directory":
    st.markdown("<h1 class='main-title'>Institutional Database</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>Search the full database of engineering colleges across Tamil Nadu.</div>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search College or District")
    if not df.empty:
        display_df = df[['College_Name', 'District', 'Course', 'Cutoff']].drop_duplicates()
        if search:
            display_df = display_df[display_df['College_Name'].str.contains(search, case=False) | display_df['District'].str.contains(search, case=False)]
        
        # Encase dataframe in a dark div for aesthetic blending
        st.markdown("<div style='background: rgba(15,23,42,0.9); padding: 15px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.dataframe(display_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# UNIVERSAL FOOTER / CREDITS
# ==========================================
st.markdown("""
<br><br>
<div style="text-align: center; padding: 20px; background: rgba(15, 23, 42, 0.9); border: 1px solid #fbbf24; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
    <h3 style="color: #fbbf24; margin: 0; text-transform: uppercase; letter-spacing: 1px; font-size: 18px;">
        👨‍💻 The team of : DEVANAND.S, KISHOR.R is created this site and ML model
    </h3>
</div>
""", unsafe_allow_html=True)