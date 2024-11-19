import streamlit as st

# Function to calculate future value
def calculate_future_value(P, r, n, t, PMT):
    A = P * (1 + r/n)**(n*t) + PMT * (((1 + r/n)**(n*t) - 1) / (r/n))
    return A

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

st.title('Retirement Calculator')

# Sidebar for input fields
st.sidebar.header('Input Parameters')

# Currency selection
currency = st.sidebar.selectbox('Currency', ['RM', 'USD', 'EUR', 'GBP'])

current_age = st.sidebar.number_input('Current Age', min_value=0, max_value=100, value=30)
retirement_age = st.sidebar.number_input('Expected Age of Retirement', min_value=0, max_value=100, value=65)
current_epf = float(st.sidebar.text_input(f'Current EPF Amount ({currency})', value='10,000').replace(',', ''))
monthly_epf_contribution = float(st.sidebar.text_input(f'Monthly EPF Contribution (Total) ({currency})', value='500').replace(',', ''))
current_investments = float(st.sidebar.text_input(f'Current Investments (Stocks, Gold, ETFs) ({currency})', value='50,000').replace(',', ''))
monthly_investments = float(st.sidebar.text_input(f'Monthly Investments ({currency})', value='1,000').replace(',', ''))

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

# Main area for results
st.subheader('Results')
st.write(f'By the time you retire (in nominal terms):')
st.write(f'- Your EPF will be worth: {currency}{future_epf:,.2f}')
st.write(f'- Your investments will be worth: {currency}{future_investments:,.2f}')
st.write(f'- Total fund: {currency}{total_fund_by_retirement:,.2f}')

st.write(f'\nIn today\'s purchasing power (inflation-adjusted):')
st.write(f'- Your EPF will be worth: {currency}{real_future_epf:,.2f}')
st.write(f'- Your investments will be worth: {currency}{real_future_investments:,.2f}')
st.write(f'- Total fund: {currency}{real_total_fund:,.2f}')

# Calculate future burger cost based on inflation
current_burger_cost = 2.05  # Example current cost of a burger
future_burger_cost = current_burger_cost * ((1 + inflation_rate) ** years_to_retirement)

# Add a dropdown to explain purchasing power
with st.expander("How purchasing power & inflation works!"):
    st.write(f"""
    If you had RM10,000 in 1993 (30 years ago), adjusted to inflation that amount would be RM20,458.
    The purchasing power of your RM20,458 now, is equal to RM10,000 in 1993.

    Which means that if you bought a burger for RM1 in 1993, it would now cost you RM2.05 to buy the same burger.

    So, your {currency}{total_fund_by_retirement:,.2f} in the future, will be worth {currency}{real_total_fund:,.2f} in today's value.
    
    Which means that if you buy a burger for RM2.05 now, it will cost you RM{future_burger_cost:,.2f} to buy the same burger in {years_to_retirement} years.
    """)

# Disclaimer and details
st.markdown("""
---
**Disclaimer:** This calculator provides an estimate based on the inputs and assumptions provided. Actual results may vary.

**Assumptions:**
- EPF annual return: 5%
- Investment annual return: 7%
- Inflation rate: 3%
- Compounding frequency: Monthly
""")
