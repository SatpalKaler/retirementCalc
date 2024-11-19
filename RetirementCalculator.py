import streamlit as st
import math
from datetime import datetime

# This must be the first Streamlit command
st.set_page_config(
    page_title="Retirement Calculator",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Configure dark mode text color based on theme
if st.get_option("theme.base") == "dark":
    st.markdown("""
        <style>
            body, p, h1, h2, h3, h4, h5, h6, li, span {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Function to calculate future value
def calculate_future_value(P, r, n, t, PMT):
    A = P * (1 + r/n)**(n*t) + PMT * (((1 + r/n)**(n*t) - 1) / (r/n))
    return A

# Custom CSS for consistent, muted colors and vibrant highlights that respect theme
st.markdown("""
    <style>
        /* Light theme styles */
        [data-theme="light"] {
            --text-color: #666666;
        }
        
        /* Dark theme styles */
        [data-theme="dark"] {
            --text-color: #E0E0E0;
        }
        
        /* Rest of your existing CSS... */
    </style>
""", unsafe_allow_html=True)

st.title('Retirement Calculator')
# Input fields in a card at the top
with st.expander("**Input Information**", expanded=True):
    # Currency selection
    col1, col2, col3 = st.columns([0.2, 0.3, 0.3])
    
    with col1:
        currency = st.text_input('Currency', value='RM')
    with col2:
        current_age = st.number_input('Current Age', min_value=0, max_value=100, value=0, step=1)
    with col3:
        retirement_age = st.number_input('Expected Age of Retirement', min_value=0, max_value=100, value=0, step=1)

    col4, col5 = st.columns([0.5, 0.5])
    
    with col4:
        current_epf = float(st.text_input(f'🏦 Current EPF Amount ({currency})', value='0').replace(',', ''))
    with col5:
        monthly_epf_contribution = st.slider(f'🏦 Monthly EPF Contribution (Total) ({currency})', min_value=0, max_value=10000, value=0, step=100)
    
    col6, col7 = st.columns([0.5, 0.5])
    
    with col6:
        current_investments = float(st.text_input(f'📈 Current Investments ({currency})', value='0').replace(',', ''))
    with col7:
        monthly_investments = st.slider(f'📈 Monthly Investments ({currency})', min_value=0, max_value=20000, value=0, step=100)

# Constants
epf_annual_rate = 0.05  # 5% annual return for EPF
investment_annual_rate = 0.07  # 7% annual return for investments
inflation_rate = 0.03  # 3% annual inflation rate
compounding_frequency = 12  # Monthly compounding

# Calculate the number of years to retirement
years_to_retirement = retirement_age - current_age


# Calculate future values (nominal)
future_epf = calculate_future_value(current_epf, epf_annual_rate, compounding_frequency, years_to_retirement, monthly_epf_contribution)
future_investments = calculate_future_value(current_investments, investment_annual_rate, compounding_frequency, years_to_retirement, monthly_investments)
net_worth_by_retirement = future_epf + future_investments

# Calculate inflation-adjusted values
real_future_epf = future_epf / ((1 + inflation_rate) ** years_to_retirement)
real_future_investments = future_investments / ((1 + inflation_rate) ** years_to_retirement)
real_net_worth = real_future_epf + real_future_investments

# # Main area for results at the bottom
# st.subheader('Results')

# Organize results into two sections using columns
col1, col2 = st.columns(2)

# Separate nominal and inflation into different rows
# st.markdown("### Nominal Values")
col1, col2 = st.columns([0.5, 0.5])
# Net Worth Section
st.markdown("<p style='font-size: 16px; color: #666; margin-top: 0; text-decoration: underline;'>Net Worth by Retirement</p>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: clamp(40px, 10vw, 88px); margin-bottom: 0; margin-top: -40px;'>{currency}{net_worth_by_retirement:,.2f}</h1>", unsafe_allow_html=True)

# Breakdown of net worth
st.markdown("<div style='font-size: 12px; color: var(--text-color); margin-top: 20px;'>", unsafe_allow_html=True)
st.markdown(f"EPF: {currency}{future_epf:,.2f} • Investments: {currency}{future_investments:,.2f}", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Inflation adjusted section with spacing
st.markdown("<div style='margin-top: 80px;'>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; color: #666; margin-top: 0; text-decoration: underline;'>Inflation-Adjusted Net Worth</p>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: clamp(40px, 10vw, 88px); margin-bottom: 0; margin-top: -40px;'>{currency}{real_net_worth:,.2f}</h1>", unsafe_allow_html=True)

# Breakdown of net worth
st.markdown("<div style='font-size: 12px; color: var(--text-color); margin-top: 20px;'>", unsafe_allow_html=True)
st.markdown(f"EPF: {currency}{future_epf:,.2f} • Investments: {currency}{future_investments:,.2f}", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)



# Calculate future burger cost based on inflation
initial_burger_cost_1993 = 5.00  # Initial cost of a burger in 1993


current_year = datetime.now().year
years_since_1993 = current_year - 1993
current_burger_cost = initial_burger_cost_1993 * math.pow((1 + inflation_rate), years_since_1993)

# Calculate future burger cost based on inflation
future_burger_cost = current_burger_cost * math.pow((1 + inflation_rate), years_to_retirement)

# Add a dropdown to explain purchasing power
with st.expander("💡 **How Inflation Works**"):
    st.write(f"""
    Imagine this:
             
    RM10,000 in 1993 ({years_since_1993} years ago) could buy the same things as **RM{10000 * math.pow((1 + inflation_rate), years_since_1993):,.2f}** today because prices have increased over {years_since_1993} years due to inflation.
    
    For example, a burger that cost **RM5** in 1993 now would cost **RM{current_burger_cost:,.2f}**.

    Looking into the future:
    
    If you have **{currency}{net_worth_by_retirement:,.2f}** in {years_to_retirement} years, it will  buy as much as **{currency}{real_net_worth:,.2f}** can today because money loses value over time.
    
    That means a burger costing **RM{current_burger_cost:,.2f}** today could cost **RM{future_burger_cost:,.2f}** in {years_to_retirement} years.
    """)
# Disclaimer and details in the sidebar
st.sidebar.markdown("""
**Disclaimer:** This calculator provides an estimate based on the inputs and assumptions provided. Actual results may vary.

---
                    
**Assumptions:**
- EPF annual return: 5%
- Investment annual return: 7%
- Inflation rate: 3%
- Compounding frequency: Monthly

---
                    
**Formulas:**
- **Future Value (FV):**
  ```
  A = P(1 + n/r)^(nt) + PMT * ((1 + n/r)^(nt) - 1) / (r/n)
  ```
  Where:
  - `P` = Present Value
  - `r` = Annual Interest Rate
  - `n` = Number of Compounding Periods per Year
  - `t` = Number of Years  - `PMT` = Payment per Period

  &nbsp;
                    
- **Inflation-Adjusted Value:**
  ```
  FV_adjusted = PV * (1 + r)^t
  ```
  Where:
  - `FV_adjusted` = Future Value adjusted for inflation
  - `PV` = Present Value
  - `r` = Inflation Rate
  - `t` = Number of Years
  
  ---

**References:**
- [CPI Inflation Calculator](https://www.dosm.gov.my/cpi_calc/index.php)
- [Compound Interest Calculator](https://www.thecalculatorsite.com/finance/calculators/compound-interest-formula)
- [Compound Interest - Wikipedia](https://en.wikipedia.org/wiki/Compound_interest)
- [Future Value - Wikipedia](https://en.wikipedia.org/wiki/Future_value)
""")