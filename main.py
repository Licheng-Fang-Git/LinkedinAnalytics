import pandas as pd
import streamlit as st
import plotly.express as px
import gspread

# # Replace with your actual sheet ID and name
sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
content_sheet_name = 'Content'
follower_sheet = 'Sheet24'
#
# Construct the URL for CSV export
content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
follower_csv_url =  f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={follower_sheet}'

st.set_page_config(page_title = "Linkedin Analytics!!", page_icon = "📈")
st.title("📈 Linkedin Analytics Dynamic")
st.markdown('<style>div.block-container{padding-top:2rem;} </style>', unsafe_allow_html= True)

tab1, tab2 = st.tabs(["Default Information", "Filtered Data"])

print(follower_csv_url)
df = pd.read_csv(content_csv_url)
follower_df = pd.read_csv(follower_csv_url)

df['Created date'] = pd.to_datetime(df['Created date'])

startDate = pd.to_datetime(df["Created date"]).min()
endDate = pd.to_datetime(df["Created date"]).max()

with tab1:
    print("Whats up")
    st.subheader("Total Follower")
    filtered_df = follower_df.groupby('Month/Yr')[['Follower Count']].sum()
    data = {
        "Month/Yr": pd.to_datetime(follower_df['Date']),
        "Follower": follower_df['Follower Count']
    }
    follower_df = pd.DataFrame(data)
    # fig = px.line(follower_df, x="Month/Yr", y="Follower", title="Growth Overtime", template='seaborn')
    # st.plotly_chart(fig, use_container_width=True, height=1000)
    st.line_chart(follower_df['Month/Yr'])

with tab2:
    col1, col2 = st.columns([2, 2])
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

    time = st.sidebar.multiselect("Pick the Time: ", df4["Interval Times"].unique())

    if not time:
        df5 = df4.copy()

    else:
        df5 = df4[df4["Interval Times"].isin(time)]

    category = st.sidebar.multiselect("Pick the Category", df5["Category"].unique())

    if not category:
        df6 = df5.copy()

    else:
        df6 = df5[df5["Category"].isin(category)]

    sub_category = st.sidebar.multiselect("Pick the Sub-Category", df6["Sub-Category"].unique())

    if not sub_category:
        df7 = df6.copy()
    else:
        df7 = df6[df6["Sub-Category"].isin(sub_category)]

    # avg_impressions = df7["Impressions"].mean()
    df["Impressions"].astype(int)

    if year:

        st.subheader(f"Filtered Data Graph {year[0]}")
        filtered_df = df2.groupby('Year')[['Impressions']].mean().round()
        data = {
            "Year" : df2['Year'].unique(),
            "Impressions" : filtered_df['Impressions'][::-1]
        }
        fig = px.bar(data, x = "Year", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)

    if month:
        st.subheader(f"Filtered Data Graph {month[0]}")
        filtered_df = df3.groupby('Month & Year')[['Impressions']].mean().round()
        data = {
            "Month" : df3['Month & Year'].unique(),
            "Impressions" : filtered_df['Impressions'][::-1]
        }
        fig = px.bar(data, x = "Month", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)

    if day:
        st.subheader(f"Filtered Data Graph {day[0]}")
        filtered_df = df4.groupby('Day of the week')[['Impressions']].mean().round()
        data = {
            "Day" : df4['Day of the week'].unique(),
            "Impressions" : filtered_df['Impressions'][::-1]
        }
        fig = px.bar(data, x = "Day", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)

    if time:
        st.subheader(f"Time of Post")
        filtered_df = df5.groupby('Interval Times')[['Impressions']].mean().round()
        data = {
            "Time" : df5['Interval Times'].unique(),
            "Impressions" : filtered_df['Impressions'][::-1]
        }
        fig = px.bar(data, x = "Time", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)



# if not year and not month and not day and not time:
#     filtered_df = df
# elif not month and not day and not time:
#     filtered_df = df[df["Year"].isin(year)]
# elif not year and not day and not time:
#     filtered_df = df[df["Month & Year"].isin(month)]
# elif not year and not month and not time:
#     filtered_df = df[df["Day of the Week"].isin(day)]
# elif day and time:
#     filtered_df = df4[df["Day of the Week"].isin(day) & df4["Interval Times"].isin(time)]
# elif month and time:
#     filtered_df = df4[df["Day of the Week"].isin(month) & df4["Interval Times"].isin(time)]
# elif year and time:
#     filtered_df = df4[df["Day of the Week"].isin(year) & df4["Interval Times"].isin(time)]
# else:
#     filtered_df = df4[df4["Year"].isin(time)]

# access = gspread.oauth()
# sheet_id = "1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U"
# wb = access.open_by_key(sheet_id)
#
# sheet = wb.worksheet("Content").get_all_records()
# df = pd.DataFrame(sheet)
# print(df.columns)
# print(df._get_column_array(5))
# df = pd.DataFrame(sheet)
# print(df.columns)
# print(df._get_column_array(5))
