import streamlit as st

# Function to calculate future value
def calculate_future_value(P, r, n, t, PMT):
    A = P * (1 + r/n)**(n*t) + PMT * (((1 + r/n)**(n*t) - 1) / (r/n))
    return A

# Set the page configuration to wide layout and hide the sidebar by default
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

st.title('Retirement Calculator')
# Input fields in a card at the top
with st.expander("**Input Information**", expanded=True):
    # Currency selection
    col1, col2, col3 = st.columns([0.3, 0.7, 0.7])
    
    with col1:
        currency = st.text_input('Currency', value='RM')
    with col2:
        current_age = st.number_input('Current Age', min_value=0, max_value=100, value=30)
    with col3:
        retirement_age = st.number_input('Expected Age of Retirement', min_value=0, max_value=100, value=65)

    col4, col5 = st.columns([0.5, 0.5])
    
    with col4:
        current_epf = float(st.text_input(f'Current EPF Amount ({currency})', value='10,000').replace(',', ''))
    with col5:
        monthly_epf_contribution = float(st.text_input(f'Monthly EPF Contribution (Total) ({currency})', value='500').replace(',', ''))
    
    col6, col7 = st.columns([0.5, 0.5])
    
    with col6:
        current_investments = float(st.text_input(f'Current Investments ({currency})', value='50,000').replace(',', ''))
    with col7:
        monthly_investments = float(st.text_input(f'Monthly Investments ({currency})', value='1,000').replace(',', ''))

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
total_fund_by_retirement = future_epf + future_investments

# Calculate inflation-adjusted values
real_future_epf = future_epf / ((1 + inflation_rate) ** years_to_retirement)
real_future_investments = future_investments / ((1 + inflation_rate) ** years_to_retirement)
real_total_fund = real_future_epf + real_future_investments

# Main area for results at the bottom
st.subheader('Results')

# Total fund by retirement
st.markdown(f"<h3 style='color: #0000FF;'>Total fund by the time you retire: {currency}{total_fund_by_retirement:,.2f}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #000000;'>- Your EPF will be worth: {currency}{future_epf:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #000000;'>- Your investments will be worth: {currency}{future_investments:,.2f}</p>", unsafe_allow_html=True)

# Inflation-adjusted total fund
st.markdown(f"<h3 style='color: #008000;'>Total fund inflation-adjusted: {currency}{real_total_fund:,.2f}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #000000;'>- Your EPF will be worth: {currency}{real_future_epf:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #000000;'>- Your investments will be worth: {currency}{real_future_investments:,.2f}</p>", unsafe_allow_html=True)

# Calculate future burger cost based on inflation
current_burger_cost = 5  # Example current cost of a burger
future_burger_cost = current_burger_cost * ((1 + inflation_rate) ** years_to_retirement)

# Add a dropdown to explain purchasing power
with st.expander("**How purchasing power & inflation works!**"):
    st.write(f"""
    If you had **RM10,000** in 1993 (30 years ago), adjusted for inflation, that amount would be equivalent to **RM20,458** today. 
    
    This means the purchasing power of **RM20,458** now is the same as **RM10,000** in 1993.

    For example, if a burger cost **RM5** in 1993, it would now cost **RM10.25** due to inflation.

    Using the same logic, if you have **{currency}{total_fund_by_retirement:,.2f}** in the future, it will have the purchasing power of **{currency}{real_total_fund:,.2f}** in today’s value.

    So, if a burger costs **RM10.25** today, it could cost **RM{future_burger_cost:,.2f}** in **{years_to_retirement}** years.
    """)

# Disclaimer and details in the sidebar
st.sidebar.markdown("""
---
**Disclaimer:** This calculator provides an estimate based on the inputs and assumptions provided. Actual results may vary.

**Assumptions:**
- EPF annual return: 5%
- Investment annual return: 7%
- Inflation rate: 3%
- Compounding frequency: Monthly
""")
st.sidebar.markdown("""
**Formulas:**
- **Future Value (FV):**
  ```
  A = P(1 + n/r)^(nt) + PMT * ((1 + n/r)^(nt) - 1) / (r/n)
  ```
  Where:
  - `P` = Present Value
  - `r` = Annual Interest Rate
  - `n` = Number of Compounding Periods per Year
  - `t` = Number of Years
  - `PMT` = Payment per Period

- **Inflation-Adjusted Value:**
  ```
  FV_adjusted = PV * (1 + r)^t
  ``` 
  Where:
  - `FV_adjusted` = Future Value adjusted for inflation
  - `PV` = Present Value
  - `r` = Inflation Rate
  - `t` = Number of Years
  

**References:**
- [CPI Inflation Calculator](https://www.dosm.gov.my/cpi_calc/index.php)
- [Compound Interest Calculator](https://www.thecalculatorsite.com/finance/calculators/compound-interest-formula)
- [Compound Interest - Wikipedia](https://en.wikipedia.org/wiki/Compound_interest)
- [Future Value - Wikipedia](https://en.wikipedia.org/wiki/Future_value)
""")
