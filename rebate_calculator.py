import streamlit as st

# Title
st.title("Fleet Fuel Rebate Calculator")

# User Inputs
total_gallons = st.number_input("Total Gallons Purchased", min_value=0, value=70000)
wawa_ratio = st.slider("Percentage of Gallons Purchased at Wawa (%)", 0, 100, 50)
avg_price_per_gallon = st.number_input("Average Price Per Gallon ($)", min_value=0.0, value=3.000, format="%.3f")
month = st.selectbox("Month of Purchase", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

# Convert Wawa ratio to decimal
wawa_ratio_decimal = wawa_ratio / 100.0

# Fuel allocation (same proportion for Wawa and 7/11 scenarios)
wawa_gallons = total_gallons * wawa_ratio_decimal
seven_eleven_gallons = total_gallons * wawa_ratio_decimal  # Same proportion for 7/11

### **First 6 Months Rebate (Wawa)**
if month in ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]:
    wawa_discount_first_6 = 0.25  # 25¢ per gallon incentive
else:
    wawa_discount_first_6 = 0.05  # Normal 5¢ per gallon after incentive period

if month in ["June", "July", "August"]:
    wawa_discount_first_6 += 0.05  # Extra 5¢ per gallon in summer

rebate_first_6_months = wawa_gallons * wawa_discount_first_6

### **Post-6 Months Rebate (Wawa)**
if wawa_ratio <= 50:
    post_incentive_discount = 0.05
elif wawa_ratio <= 75:
    post_incentive_discount = 0.06
else:
    post_incentive_discount = 0.07

# Add extra 5¢ per gallon in June, July, August
if month in ["June", "July", "August"]:
    post_incentive_discount += 0.05  

rebate_post_6_months = wawa_gallons * post_incentive_discount

### **7/11 Rebate (Using the same proportion)**
seven_eleven_rebate = seven_eleven_gallons * 0.07  # 7¢ per gallon at 7/11

### **Bank Rebate Calculation (Applies to Both Wawa Scenarios)**
if total_gallons >= 75000:
    bank_rebate_basis = 0.0095
elif total_gallons >= 65000:
    bank_rebate_basis = 0.0085
elif total_gallons >= 55000:
    bank_rebate_basis = 0.0075
else:
    bank_rebate_basis = 0.0

# **Direct Debit Bonus (11 Basis Points)**
bank_rebate_basis += 0.0011  # Adds 0.0011 (11 basis points)

# **Final Bank Rebate Calculation**
bank_rebate = total_gallons * avg_price_per_gallon * bank_rebate_basis

# **Total Wawa Rebates (Including Bank Rebate)**
total_rebate_first_6_months = rebate_first_6_months + bank_rebate
total_rebate_post_6_months = rebate_post_6_months + bank_rebate

# **Create Three Columns in Streamlit**
col1, col2, col3 = st.columns(3)

### **Column 1: Wawa (<6M)**
with col1:
    st.subheader("Wawa (<6M)")
    st.write(f"**Wawa Rebate:** ${rebate_first_6_months:,.2f}")
    st.write(f"**Bank Rebate:** ${bank_rebate:,.2f}")
    st.write(f"**Total Rebate:** ${total_rebate_first_6_months:,.2f}")

### **Column 2: Wawa (Post-6M)**
with col2:
    st.subheader("Wawa")
    st.write(f"**Wawa Rebate:** ${rebate_post_6_months:,.2f}")
    st.write(f"**Bank Rebate:** ${bank_rebate:,.2f}")
    st.write(f"**Total Rebate:** ${total_rebate_post_6_months:,.2f}")

### **Column 3: 7/11**
with col3:
    st.subheader("7/11")
    st.write(f"**7/11 Rebate:** ${seven_eleven_rebate:,.2f}")
    st.write("**Bank Rebate:** N/A")  # No bank rebate for 7/11
    st.write(f"**Total Rebate:** ${seven_eleven_rebate:,.2f}")
