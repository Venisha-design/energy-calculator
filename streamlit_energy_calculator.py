import streamlit as st
import pandas as pd
#import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="⚡ Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        text-align: center;
    }
    
    .result-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .energy-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .sidebar .stSelectbox > label {
        font-weight: bold;
        color: #333;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .appliance-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .appliance-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .appliance-card:hover {
        border-color: #4facfe;
        background: rgba(79,172,254,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Energy Consumption Calculator</h1>
    <p>Calculate your home's energy consumption based on your living setup and appliances</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Personal Information")
    
    # Personal details
    name = st.text_input("Enter your name:", placeholder="John Doe")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
    city = st.text_input("Enter your city:", placeholder="Mumbai")
    area = st.text_input("Enter your area name:", placeholder="Andheri West")
    
    st.header("🏠 Housing Details")
    
    # Housing type
    flat_tenament = st.radio(
        "Housing Type:",
        ["Flat", "Tenament"],
        horizontal=True
    )
    
    # Facility type
    facility = st.selectbox(
        "Home Configuration:",
        ["Select your home type", "1BHK", "2BHK", "3BHK"],
        index=0
    )
    
    st.header("⚙️ Appliances")
    
    # Appliances
    ac = st.checkbox("❄️ Air Conditioner", help="Central or window AC units")
    fridge = st.checkbox("🧊 Refrigerator", help="Standard home refrigerator")
    wm = st.checkbox("🧺 Washing Machine", help="Automatic washing machine")
    
    # Calculate button
    calculate_btn = st.button("🔥 Calculate Energy Consumption", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if calculate_btn:
        # Validation
        if not name or not city or not area or facility == "Select your home type":
            st.error("⚠️ Please fill in all required fields!")
        else:
            # Energy calculation logic
            cal_energy = 0
            
            # Base energy calculation based on home type
            if facility.lower() == "1bhk":
                cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
            elif facility.lower() == "2bhk":
                cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
            elif facility.lower() == "3bhk":
                cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
            
            # Add appliance consumption
            appliance_energy = 0
            active_appliances = []
            
            if ac:
                appliance_energy += 3
                active_appliances.append("Air Conditioner")
            if fridge:
                appliance_energy += 3
                active_appliances.append("Refrigerator")
            if wm:
                appliance_energy += 3
                active_appliances.append("Washing Machine")
            
            cal_energy += appliance_energy
            
            # Display results
            st.markdown(f"""
            <div class="result-card">
                <h2>🎉 Energy Consumption Results for {name}</h2>
                <div class="energy-value">{cal_energy:.1f} kWh</div>
                <p>Estimated daily energy consumption</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed breakdown
            st.subheader("📊 Consumption Breakdown")
            
            # Create breakdown data
            breakdown_data = {
                "Source": ["Base Home Consumption", "Appliances"],
                "Energy (kWh)": [cal_energy - appliance_energy, appliance_energy],
                "Color": ["#4facfe", "#00f2fe"]
            }
            
            # Pie chart
            fig_pie = px.pie(
                values=breakdown_data["Energy (kWh)"],
                names=breakdown_data["Source"],
                title="Energy Consumption Breakdown",
                color_discrete_sequence=["#4facfe", "#00f2fe"]
            )
            fig_pie.update_layout(
                font=dict(size=14),
                title_font_size=18,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Bar chart for appliances
            if active_appliances:
                st.subheader("🔌 Appliance Consumption")
                appliance_df = pd.DataFrame({
                    "Appliance": active_appliances,
                    "Energy (kWh)": [3] * len(active_appliances)
                })
                
                fig_bar = px.bar(
                    appliance_df,
                    x="Appliance",
                    y="Energy (kWh)",
                    title="Individual Appliance Consumption",
                    color="Energy (kWh)",
                    color_continuous_scale="blues"
                )
                fig_bar.update_layout(
                    font=dict(size=14),
                    title_font_size=18,
                    xaxis_title="Appliances",
                    yaxis_title="Energy Consumption (kWh)"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Monthly and yearly projections
            st.subheader("📈 Energy Projections")
            
            col_month, col_year = st.columns(2)
            
            with col_month:
                monthly_energy = cal_energy * 30
                st.metric(
                    label="Monthly Consumption",
                    value=f"{monthly_energy:.1f} kWh",
                    delta="30 days"
                )
            
            with col_year:
                yearly_energy = cal_energy * 365
                st.metric(
                    label="Yearly Consumption",
                    value=f"{yearly_energy:.1f} kWh",
                    delta="365 days"
                )
            
            # Cost estimation (approximate)
            st.subheader("💰 Cost Estimation")
            cost_per_unit = 5.0  # Approximate cost per kWh in INR
            
            daily_cost = cal_energy * cost_per_unit
            monthly_cost = daily_cost * 30
            yearly_cost = daily_cost * 365
            
            cost_col1, cost_col2, cost_col3 = st.columns(3)
            
            with cost_col1:
                st.metric(
                    label="Daily Cost",
                    value=f"₹{daily_cost:.2f}",
                    help="Approximate cost per day"
                )
            
            with cost_col2:
                st.metric(
                    label="Monthly Cost",
                    value=f"₹{monthly_cost:.2f}",
                    help="Approximate cost per month"
                )
            
            with cost_col3:
                st.metric(
                    label="Yearly Cost",
                    value=f"₹{yearly_cost:.2f}",
                    help="Approximate cost per year"
                )
            
            # User summary
            st.subheader("👤 User Summary")
            st.info(f"""
            **Name:** {name}  
            **Age:** {age} years  
            **Location:** {area}, {city}  
            **Housing:** {facility} {flat_tenament}  
            **Active Appliances:** {', '.join(active_appliances) if active_appliances else 'None'}
            """)

with col2:
    # Information panel
    st.markdown("""
    <div class="info-card">
        <h3>💡 Energy Saving Tips</h3>
        <ul style="text-align: left; margin: 1rem 0;">
            <li>Use LED bulbs instead of incandescent</li>
            <li>Set AC temperature to 24°C or higher</li>
            <li>Unplug devices when not in use</li>
            <li>Use natural light during the day</li>
            <li>Regular maintenance of appliances</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Energy efficiency guide
    st.markdown("""
    <div class="info-card">
        <h3>📋 Understanding Your Consumption</h3>
        <p style="text-align: left; margin: 1rem 0;">
        <strong>Base Consumption:</strong><br>
        • 1BHK: 2.4 kWh/day<br>
        • 2BHK: 3.6 kWh/day<br>
        • 3BHK: 4.8 kWh/day<br><br>
        <strong>Appliance Consumption:</strong><br>
        • Each appliance: 3 kWh/day
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Environmental impact
    if 'cal_energy' in locals():
        co2_emission = cal_energy * 0.82  # Approximate CO2 emission per kWh in kg
        st.markdown(f"""
        <div class="info-card">
            <h3>🌱 Environmental Impact</h3>
            <p><strong>Daily CO₂ Emission:</strong></p>
            <p style="font-size: 1.5rem; margin: 0.5rem 0;">{co2_emission:.2f} kg</p>
            <p><strong>Monthly:</strong> {co2_emission * 30:.1f} kg</p>
            <p><strong>Yearly:</strong> {co2_emission * 365:.1f} kg</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>⚡ Energy Consumption Calculator | Built with Streamlit</p>
    <p>💡 Promote energy efficiency and sustainability</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for form persistence
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
