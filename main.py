import pandas as pd
import streamlit as st
import gspread

# # Replace with your actual sheet ID and name
# sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
# sheet_name = 'Content' # Example: 'Data Sheet'
#
# # Construct the URL for CSV export
# csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
csv_url = 'https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Content'
# Read the data into a Pandas DataFrame
print(csv_url)

st.set_page_config(page_title = "Linkedin Analytics!!", page_icon = "📈")
st.title("📈 Linkedin Analytics Dynamic")
st.markdown('<style>div.block-container{padding-top:2rem;} </style>', unsafe_allow_html= True)

df = pd.read_csv(csv_url)
print(df.columns)
df['Created date'] = pd.to_datetime(df['Created date'])
print(df['Created date'])

startDate = pd.to_datetime(df["Created date"]).min()
endDate = pd.to_datetime(df["Created date"]).max()
print(startDate, endDate)

col1, col2 = st.columns((2))

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Created date"] >= date1) & (df["Created date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Create for region
year = st.sidebar.multiselect("Pick the Year: ", df["Year"].unique())

if not year:
    df2 = df.copy()
else:
    df2 = df[df["Year"].isin(year)]

# Create for state
month = st.sidebar.multiselect("Pick the Month: ", df2["Month & Year"].unique())

if not month:
    df3 = df2.copy()

else:
    df3 = df2[df2["Month & Year"].isin(month)]

day = st.sidebar.multiselect("Pick the Day: ", df3["Day of the week"].unique())

if not day:
    df4 = df3.copy()

else:
    df4 = df3[df3["Day of the week"].isin(day)]

time = st.sidebar.multiselect("Pick the Time: ", df3["Interval Times"].unique())

# access = gspread.oauth()
# sheet_id = "1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U"
# wb = access.open_by_key(sheet_id)
#
# sheet = wb.worksheet("Content").get_all_records()
# df = pd.DataFrame(sheet)
# print(df.columns)
# print(df._get_column_array(5))
