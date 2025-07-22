import pandas as pd
import streamlit as st
import plotly.express as px
import gspread
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

# # Replace with your actual sheet ID and name
sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
content_sheet_name = 'Content'
follower_sheet = 'Sheet24'
#
# Construct the URL for CSV export
content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
follower_csv_url =  f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={follower_sheet}'

st.set_page_config(page_title = "LinkedIn Analytics!!", page_icon = "📈")
st.title("📈 Linkedin Analytics Dynamic")
st.markdown('<style>div.block-container{padding-top:2rem;} </style>', unsafe_allow_html= True)

tab1, tab2 = st.tabs(["Default Information", "Filtered Data"])

df = pd.read_csv(content_csv_url)
follower_df = pd.read_csv(follower_csv_url)

df['Created date'] = pd.to_datetime(df['Created date'])

startDate = pd.to_datetime(df["Created date"]).min()
endDate = pd.to_datetime(df["Created date"]).max()

with tab1:
    st.subheader("Total Follower")
    filtered_df = follower_df.groupby('Month/Yr')[['Follower Count']].sum()
    data = {
        "Month/Yr": pd.to_datetime(follower_df['Date']),
        "Follower": follower_df['Follower Count']
    }
    follower_df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Month/Yr'], y=follower_df['Follower'], name='Follower Count'))
    st.plotly_chart(fig, picker=True, use_container_width=True, theme = None, height=1500)

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

    emoji = st.sidebar.multiselect("Pick the Emoji", df["Type Emoji"].unique())
    if not emoji:
        df8 = df7.copy()
    else:
        df8 = df7[df7["Type Emoji"].isin(emoji)]


    if year:
        st.subheader(f"Year's Bar Chart")
        filtered_df = df2.groupby('Year')[['Impressions']].mean().round()
        post_count = df2['Year'].value_counts()

        data = {
            "Year" : df2['Year'].unique(),
            "Number of Posts" : list(post_count),
            "Impressions" : filtered_df['Impressions'][::-1]
        }
        fig = px.bar(data, x = "Year", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)

        st.dataframe(data)

    if month:
        st.subheader(f"Month's Bar Chart")
        group_keys = list(df3.groupby('Month & Year').groups.keys())
        filtered_df = df3.groupby('Month & Year')[['Impressions']].mean().round()
        post_count = list(df3.groupby('Month & Year')['Number of Post'].sum())
        filtered_df.insert(0, "Month", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_month = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_month.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Month'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Month'] == i]['Impressions'].values[0])
        data = {
            "Month" : organize_month,
            "Number of Posts" : organize_number_posts,
            "Impressions" : organize_impressions
        }
        fig = px.bar(data, x = "Month", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)
        st.dataframe(data)

    if day:
        st.subheader(f"Day Bar Chart")
        group_keys = list(df4.groupby('Day of the week').groups.keys())
        filtered_df = df4.groupby('Day of the week')[['Impressions']].mean().round()
        post_count = list(df4.groupby('Day of the week')['Number of Post'].sum())
        filtered_df.insert(0, "Day", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_day = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_day.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Day'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Day'] == i]['Impressions'].values[0])
        data = {
            "Day" : organize_day,
            "Number of Posts": organize_number_posts,
            "Impressions" : organize_impressions
        }

        fig = px.bar(data, x = "Day", y = "Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height = 200)
        st.dataframe(data)

    if time:
        st.subheader(f"Time of Post Chart")
        group_keys = list(df5.groupby('Interval Times').groups.keys())
        filtered_df = df5.groupby('Interval Times')[['Impressions']].mean().round()
        post_count = list(df5.groupby('Interval Times')['Number of Post'].sum())
        filtered_df.insert(0, "Time", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_time = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_time.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Time'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Time'] == i]['Impressions'].values[0])
        data = {
            "Time" : organize_time,
            "Number of Posts": organize_number_posts,
            "Impressions" : organize_impressions
        }
        fig = px.bar(data, x="Time", y="Impressions", template='seaborn')
        print(st.plotly_chart(fig, use_container_width=True, height=200, on_select="rerun"))
        st.dataframe(data)

    if category:
        st.subheader(f"Category Chart")
        group_keys = list(df6.groupby('Category').groups.keys())
        filtered_df = df6.groupby('Category')[['Impressions']].mean().round()
        post_count = list(df6.groupby('Category')['Number of Post'].sum())
        filtered_df.insert(0, "Category", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_category = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_category.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Category'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Category'] == i]['Impressions'].values[0])
        data = {
            "Category": organize_category,
            "Number of Posts": organize_number_posts,
            "Impressions": organize_impressions
        }
        fig = px.bar(data, x="Category", y="Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height=200)
        st.dataframe(data)

    if sub_category:
        st.subheader(f"Sub-Category Chart")
        group_keys = list(df7.groupby('Sub-Category').groups.keys())
        filtered_df = df7.groupby('Sub-Category')[['Impressions']].mean().round()
        post_count = list(df7.groupby('Sub-Category')['Number of Post'].sum())
        filtered_df.insert(0, "Sub-Category", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_subcategory = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_subcategory.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Sub-Category'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Sub-Category'] == i]['Impressions'].values[0])
        data = {
            "Sub-Category": organize_subcategory,
            "Number of Posts": organize_number_posts,
            "Impressions": organize_impressions
        }
        fig = px.bar(data, x="Sub-Category", y="Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height=200)
        st.dataframe(data)

    if emoji:
        st.subheader(f"Emoji Chart")
        group_keys = list(df8.groupby('Type Emoji').groups.keys())
        filtered_df = df8.groupby('Type Emoji')[['Impressions']].mean().round()
        post_count = list(df8.groupby('Type Emoji')['Number of Post'].sum())
        filtered_df.insert(0, "Type Emoji", group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_emoji = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_emoji.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df['Type Emoji'] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df['Type Emoji'] == i]['Impressions'].values[0])
        data = {
            "Type Emoji": organize_emoji,
            "Number of Posts": organize_number_posts,
            "Impressions": organize_impressions
        }
        fig = px.bar(data, x="Type Emoji", y="Impressions", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height=200)
        st.dataframe(data)



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
