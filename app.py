import streamlit as st
import yfinance as yf
from numerize import numerize

st.title("Mergers & Acquisitions")
st.header("Impact of the funding mechanism on the beta of the acquiring firm")

st.write("Enter the stock ticker for both firms")

with st.form(key='tickers'):
    c1, c2 = st.columns(2)
    with c1:
        acquirer_ticker = st.text_input("Acquirer",value="MSFT")
    with c2:
        target_ticker = st.text_input("Target",value="ATVI")
    submitButton = st.form_submit_button(label = 'Enter')
acquirer = yf.Ticker(acquirer_ticker)
target = yf.Ticker(target_ticker)

acquirer_marketcap = acquirer.info.get('marketCap')
acquirer_marketcap_n = numerize.numerize(acquirer_marketcap)

target_marketcap = target.info.get('marketCap')
target_marketcap_n = numerize.numerize(target_marketcap)

acquirer_debt = acquirer.info.get('totalDebt')
acquirer_debt_n = numerize.numerize(acquirer_debt)

target_debt = target.info.get('totalDebt')
target_debt_n = numerize.numerize(target_debt)

acquirer_beta = acquirer.info.get('beta')
acquirer_beta_n = round(acquirer_beta,2)

target_beta = target.info.get('beta')
target_beta_n = round(target_beta,2)

acquirer_firm_value = acquirer_marketcap + acquirer_debt
acquirer_firm_value_n = numerize.numerize(acquirer_firm_value)

target_firm_value = target_marketcap + target_debt
target_firm_value_n = numerize.numerize(target_firm_value)

acquirer_deratio = acquirer_debt/acquirer_marketcap
acquirer_deratio_pct = round(acquirer_deratio*100,2)

target_deratio = target_debt/target_marketcap
target_deratio_pct = round(target_deratio*100,2)

acquirer_cash = acquirer.info.get('totalCash')
acquirer_cash_n = numerize.numerize(acquirer_cash)

target_cash = target.info.get('totalCash')
target_cash_n = numerize.numerize(target_cash)

st.subheader("Metrics for the acquiring and target firms")

col1, col2 = st.columns(2)
col1.metric("Acquirer Market Cap", acquirer_marketcap_n)
col2.metric("Target Market Cap", target_marketcap_n)

col1, col2 = st.columns(2)
col1.metric("Acquirer Debt", acquirer_debt_n)
col2.metric("Target Debt", target_debt_n)

col1, col2 = st.columns(2)
col1.metric("Acquirer Beta", acquirer_beta_n)
col2.metric("Target Beta", target_beta_n)

col1, col2 = st.columns(2)
col1.metric("Acquirer Cash Balance", acquirer_cash_n)
col2.metric("Target Cash Balance", target_cash_n)

col1, col2 = st.columns(2)
col1.metric("Acquirer Firm Value", acquirer_firm_value_n)
col2.metric("Target Firm Value", target_firm_value_n)

col1, col2 = st.columns(2)
col1.metric("Acquirer D/E Ratio %", acquirer_deratio_pct)
col2.metric("Target D/E Ratio %", target_deratio_pct)

st.subheader("Unlever the regression beta by removing the impact of debt")

st.write("Enter the marginal tax rate and how the acquisition will be funded in terms of debt & equity")
st.write("The marginal tax rate and D/E ratio impacts the unlevered beta of the firms. Unlevered Beta = Levered Beta / (1 + (Marginal Tax Rate * D/E Ratio))")

with st.form(key='taxrate'):
    marginal_taxrate_input = st.number_input("Marginal Tax Rate %",value=27.00)
    submitButton = st.form_submit_button(label = 'Enter')
marginal_taxrate = round(marginal_taxrate_input/100,2)

acquirer_unleveredbeta = acquirer_beta/(1 + (marginal_taxrate*acquirer_deratio))
acquirer_unleveredbeta_n = round(acquirer_unleveredbeta,2)

target_unleveredbeta = target_beta/(1 + (marginal_taxrate*target_deratio))
target_unleveredbeta_n = round(target_unleveredbeta,2)

col1, col2 = st.columns(2)
col1.metric("Acquirer Unlevered Beta", acquirer_unleveredbeta_n)
col2.metric("Target Unlevered Beta", target_unleveredbeta_n)

st.subheader("Funding the acquisition with debt, equity or both")

st.write("Enter the % of debt that will used to fund this acquisition")

debt_input = st.slider("Debt %",0,100,0)
debt = round(debt_input/100,2)
equity = round((100-debt)/100,2)

col1, col2 = st.columns(2)
col1.metric("Debt %", round(debt*100,2))
col2.metric("Equity %", round(equity*100,2))

total_firm_value = acquirer_firm_value + target_firm_value
total_firm_value_n = numerize.numerize(total_firm_value)

weightedavg_unleveredbeta = (acquirer_unleveredbeta*(acquirer_firm_value/total_firm_value)) + (target_unleveredbeta*(target_firm_value/total_firm_value))
weightedavg_unleveredbeta_n = round(weightedavg_unleveredbeta,2)

total_debt = acquirer_debt + target_debt + (debt*target_marketcap)
total_debt_n = numerize.numerize(total_debt)

total_equity = acquirer_marketcap + (target_marketcap-(debt*target_marketcap))
total_equity_n = numerize.numerize(total_equity)

total_deratio = total_debt/total_equity
total_deratio_n = round(total_deratio*100,2)

new_beta = weightedavg_unleveredbeta*(1+ (marginal_taxrate*total_deratio))
new_beta_n = round(new_beta,2)

st.subheader("Metrics for combined firm after the acquisition")

col1, col2 = st.columns(2)
col1.metric("Combined Firm Value", total_firm_value_n)
col2.metric("Weighted Avg. Unlevered Beta", weightedavg_unleveredbeta_n)

col1, col2 = st.columns(2)
col1.metric("Debt", total_debt_n)
col2.metric("Equity", total_equity_n)

col1, col2 = st.columns(2)
col1.metric("D/E Ratio %", total_deratio_n)
col2.metric("Beta", new_beta_n)
