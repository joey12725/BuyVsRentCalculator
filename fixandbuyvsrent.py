import streamlit as st
import pandas as pd
#comparing the cost of buying a house from family that needs heavy repairs vs renting our current house

purchase_price = st.number_input('Purchase price of the house', value=80000)
down_payment = st.number_input('Down payment', value=0)
loan_balance = purchase_price - down_payment
cost_to_repair_and_renovate = st.number_input('Cost to repair and renovate', value=130000)

mortgage_term = st.number_input('Mortgage term', value=30)
mortgage_rate = st.number_input('Mortgage rate', value=5)
property_tax_rate = st.number_input('Property tax rate', value=1.91)
home_insurance = st.number_input('Yearly Home insurance', value=4800)
hoa_fees = st.number_input('Yearly HOA fees', value=0)
annual_maintenance = st.number_input('Annual maintenance', value=3000)
home_value_increase = st.number_input('Home value increase', value=3)
home_value_once_repaired = st.number_input('Home value once repaired', value=325000)

rent = st.number_input('Rent', value=1000)
renters_insurance = st.number_input('Renters insurance', value=200)
rent_increase = st.number_input('Rent increase', value=3)
display_years = st.number_input('Years to display', value=30)
#when her grandmother passes, the remaining balance of the mortgage will be forgiven
years_paying_mortgage = st.number_input('Years paying mortgage', value=15)

#now visualize the total spend over time of each scenario on a graph
initial_costs = down_payment + cost_to_repair_and_renovate
monthly_mortgage_payment = loan_balance * (mortgage_rate / 1200) / (1 - (1 + mortgage_rate / 1200) ** (-mortgage_term * 12))
monthly_property_tax = purchase_price * property_tax_rate / 1200
monthly_home_insurance = home_insurance / 12
monthly_maintenance = annual_maintenance / 12
monthly_hoa_fees = hoa_fees/12
monthly_rent = rent


monthly_costs_house = monthly_mortgage_payment + monthly_property_tax + monthly_home_insurance + monthly_hoa_fees + monthly_maintenance
monthly_costs_house_no_mortgage = monthly_property_tax + monthly_home_insurance + monthly_hoa_fees + monthly_maintenance
monthly_costs_rent = monthly_rent + renters_insurance
appreciation_multiplier = ((home_value_increase/12) / 100)
time_series = pd.DataFrame(columns=['Time', 'Total Cost House', 'Total Cost Rent', 'Total House Impact on Net Worth', 'Total Rent Impact on Net Worth'])
paying_mortgage = True
for i in range(12*display_years):
    if paying_mortgage:
        total_cost_house = initial_costs + (monthly_costs_house * i)
        total_cost_rent = monthly_costs_rent * i
        total_house_impact_on_net_worth = home_value_once_repaired + (home_value_once_repaired*appreciation_multiplier* i) - total_cost_house - loan_balance
        total_rent_impact_on_net_worth = -monthly_costs_rent * i
        loan_balance = loan_balance - monthly_mortgage_payment
    else:
        total_cost_house = initial_costs + (monthly_costs_house*years_paying_mortgage*12) + (monthly_costs_house_no_mortgage * (i-years_paying_mortgage*12))
        total_cost_rent = monthly_costs_rent * i
        total_house_impact_on_net_worth = home_value_once_repaired + (home_value_once_repaired*appreciation_multiplier* i) - total_cost_house
        total_rent_impact_on_net_worth = -monthly_costs_rent * i
    if i == years_paying_mortgage * 12:
        paying_mortgage = False
        loan_balance = 0
    time_series.loc[i] = [i, total_cost_house, total_cost_rent, total_house_impact_on_net_worth, total_rent_impact_on_net_worth]

total_costs_house = time_series['Total Cost House'].max()
total_costs_rent = time_series['Total Cost Rent'].max()
advantage_of_buying = home_value_once_repaired + (home_value_once_repaired*appreciation_multiplier* display_years*12) + (total_costs_rent-total_costs_house)
st.line_chart(time_series[['Total Cost House', 'Total Cost Rent']])
st.line_chart(time_series[['Total House Impact on Net Worth', 'Total Rent Impact on Net Worth']])

#Now make annother version where the inital costs are invested in the market and the difference in monthly costs is invested in the market
#and compare the total net worth of the two scenarios
market_return = st.slider('Market return', -3, 20, 7)
initial_investment = initial_costs
monthly_investment =  monthly_costs_rent - monthly_costs_house
time_series_market = pd.DataFrame(columns=['Time', 'Net Worth House', 'Net Worth Rent'])
net_worth_house = home_value_once_repaired - loan_balance
net_worth_rent = initial_investment
paying_mortgage = True

for i in range(12*display_years):
    if paying_mortgage:
        net_worth_house = net_worth_house + monthly_investment + (net_worth_house * (market_return/1200)) + monthly_mortgage_payment
        net_worth_rent = net_worth_rent + (net_worth_rent * (market_return/1200))
        loan_balance = loan_balance - monthly_mortgage_payment
    else:
        monthly_investment = monthly_costs_rent - monthly_costs_house_no_mortgage
        net_worth_house = net_worth_house + monthly_investment + (net_worth_house * (market_return/1200))
        net_worth_rent = net_worth_rent + (net_worth_rent * (market_return/1200))
    if i == years_paying_mortgage * 12:
        paying_mortgage = False
        loan_balance = 0
    time_series_market.loc[i] = [i, net_worth_house, net_worth_rent]

st.line_chart(time_series_market[['Net Worth House', 'Net Worth Rent']])


st.markdown(f"""
## Cash On Hand Needed To Buy: ${round(initial_costs, 0)}
## Monthly Mortgage Payment: ${round(monthly_mortgage_payment, 0)}
## Total Monthly Costs House: ${round(monthly_costs_house, 0)}
## Total Monthly Costs House without Mortgage: ${round(monthly_costs_house_no_mortgage, 0)}
## Total Monthly Costs Rent: ${round(monthly_costs_rent, 0)}
## Advantage of Buying over the Display Term: ${round(advantage_of_buying, 0)}
""")