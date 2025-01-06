# 🏦 **Retirement Calculator** 🧮

*Welcome to the Retirement Calculator, a Streamlit app designed to help you plan your financial future!* ✨ This tool estimates the future value of your EPF (Employees Provident Fund) savings and investments, both in nominal and inflation-adjusted terms, to provide insights into your retirement preparedness.

## 🎯 **Features**

### 💡 **Customizable Inputs:**
* Set your current age, retirement age, and currency
* Input current EPF savings, monthly contributions, and investment details

### ⚡ **Real-Time Calculations:**
* Computes the future value of your savings and investments
* Adjusts for inflation to show purchasing power in today's terms

### 📊 **Interactive Insights:**
* Breakdown of future EPF and investment values
* Fun projection of how inflation impacts everyday items like burgers 🍔

### 🎨 **User-Friendly Interface:**
* Expandable input form
* Clean, centered layout with helpful sidebars

## 🔄 **How It Works**

The calculator uses the compound interest formula to estimate the growth of your savings and investments over time, factoring in monthly contributions and annual returns. It also adjusts for inflation to provide a realistic view of your purchasing power at retirement.

## ✍️ **Formulas Used**

1. **Future Value (FV):**
```
A = P(1 + r/n)^(nt) + PMT * ((1 + r/n)^(nt) - 1) / (r/n)
```
* P: Present Value
* r: Annual Interest Rate
* n: Compounding Frequency per Year
* t: Time in Years
* PMT: Monthly Payment

2. **_Inflation-Adjusted Value:_**
```
FV_adjusted = FV / (1 + inflation_rate)^t
```

## 📌 **Assumptions**
* EPF annual return: 5% 📈
* Investment annual return: 7% 📊
* Inflation rate: 3% 💰
* Compounding frequency: Monthly ⏱️

## 🚀 **Installation**

Clone the repository:
```
git clone https://github.com/yourusername/retirement-calculator.git
```


## ⚠️ **Disclaimer**

*This calculator is for educational purposes and provides estimates based on user inputs and assumptions. Results may vary based on market conditions and individual circumstances.*

## 🔮 **Future Plans**
* Add customization for assumptions
* Introduce dynamic graphs for better visualization
* Add AI-agents for advice/discussion on personal finance
* Life Calculator - rough estimate of how much your retirement will last until your death

Feel free to contribute or report issues in the issues section! 

### _Enjoy planning your future with the Retirement Calculator!_ 🌟 💫 ✨
