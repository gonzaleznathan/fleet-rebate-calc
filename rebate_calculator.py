import streamlit as st

# Title
st.title("Fleet Fuel Rebate Calculator")

# User Inputs
total_gallons = st.number_input("Total Gallons Purchased", min_value=0, value=70000)
wawa_ratio = st.slider("Percentage of Gallons Purchased at Wawa (%)", 0, 100, 50)
seven_eleven_ratio = st.slider("Percentage of Gallons Purchased at 7/11 (%)", 0, 100, 50)
avg_price_per_gallon = st.number_input("Average Price Per Gallon ($)", min_value=0.0, value=3.000, format="%.3f")
month = st.selectbox("Month of Purchase", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

# Convert ratios to decimals
wawa_ratio_decimal = wawa_ratio / 100.0
seven_eleven_ratio_decimal = seven_eleven_ratio / 100.0

# Fuel allocations
wawa_gallons = total_gallons * wawa_ratio_decimal
seven_eleven_gallons = total_gallons * seven_eleven_ratio_decimal

# === Wawa Rebate (<6 Months): Flat 25¢ per gallon
wawa_discount_first_6 = 0.25
rebate_first_6_months = wawa_gallons * wawa_discount_first_6

# === Wawa Rebate (Post-6 Months): Tiered
if wawa_ratio <= 50:
    post_incentive_discount = 0.05
elif wawa_ratio <= 75:
    post_incentive_discount = 0.06
else:
    post_incentive_discount = 0.07

# Summer bonus for post-6-months Wawa only
if month in ["June", "July", "August"]:
    post_incentive_discount += 0.05

rebate_post_6_months = wawa_gallons * post_incentive_discount

# === 7/11 Rebate: Always 7¢ per gallon
seven_eleven_rebate = seven_eleven_gallons * 0.07

# === Bank Rebate Basis (applies to both Wawa scenarios)
if total_gallons >= 75000:
    bank_rebate_basis = 0.0095
elif total_gallons >= 65000:
    bank_rebate_basis = 0.0085
elif total_gallons >= 55000:
    bank_rebate_basis = 0.0075
else:
    bank_rebate_basis = 0.0

# Direct Debit Bonus (11 basis points)
bank_rebate_basis += 0.0011

# Final Bank Rebate Calculation
bank_rebate = total_gallons * avg_price_per_gallon * bank_rebate_basis

# Total Wawa Rebates
total_rebate_first_6_months = rebate_first_6_months + bank_rebate
total_rebate_post_6_months = rebate_post_6_months + bank_rebate

# === Display Results
col1, col2, col3 = st.columns(3)

# Wawa First 6 Months
with col1:
    st.subheader("Wawa (First 6M)")
    st.write(f"**Wawa Rebate:** ${rebate_first_6_months:,.2f}")
    st.write(f"**Bank Rebate:** ${bank_rebate:,.2f}")
    st.write(f"**Total Rebate:** ${total_rebate_first_6_months:,.2f}")

# Wawa Post-6 Months
with col2:
    st.subheader("Wawa (Post-6M)")
    st.write(f"**Wawa Rebate:** ${rebate_post_6_months:,.2f}")
    st.write(f"**Bank Rebate:** ${bank_rebate:,.2f}")
    st.write(f"**Total Rebate:** ${total_rebate_post_6_months:,.2f}")

# 7/11
with col3:
    st.subheader("7/11")
    st.write(f"**7/11 Rebate:** ${seven_eleven_rebate:,.2f}")
    st.write("**Bank Rebate:** N/A")
    st.write(f"**Total Rebate:** ${seven_eleven_rebate:,.2f}")
