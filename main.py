import pandas as pd
import streamlit as st
import plotly.express as px
import gspread
import plotly.graph_objects as go
from PIL import Image
from streamlit import sidebar, image
from streamlit_plotly_events import plotly_events

# # Replace with your actual sheet ID and name
sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
content_sheet_name = 'Content'
follower_sheet = 'Sheet24'
location_sheet = 'Sheet25'
job_function_sheet = 'Sheet26'
industry_sheet = 'Sheet27'
#
# Construct the URL for CSV export
content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
follower_csv_url =  f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={follower_sheet}'
location_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={location_sheet}'
job_function_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={job_function_sheet}'
industry_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={industry_sheet}'


st.logo('trillium_logo.png', link='https://www.trlm.com/', size='large', icon_image='trillium_trading_logo.png')
st.set_page_config(page_title = "LinkedIn Analytics!!", page_icon = "📈", layout='wide')
st.title("📈 Linkedin Analytics")
st.markdown('<style>div.block-container{padding-top:2rem;} </style>', unsafe_allow_html= True)

tab1, tab2 = st.tabs(["Default Information", "Filtered Data"])

df = pd.read_csv(content_csv_url)
follower_df = pd.read_csv(follower_csv_url)
location_df = pd.read_csv(location_sheet_url)
job_function_df = pd.read_csv(job_function_sheet_url)
industry_df = pd.read_csv(industry_sheet_url)

df['Created date'] = pd.to_datetime(df['Created date'])

startDate = pd.to_datetime(df["Created date"]).min()
endDate = pd.to_datetime(df["Created date"]).max()

with tab1:
    def create_pie_chart(category, aggregate, dataframe, array ):
        group_keys = array
        filtered_df = dataframe.groupby(category)[[aggregate]].sum()
        filtered_df = filtered_df.loc[array]
        print(filtered_df)
        data = {
            'Location' : array,
            "Followers" : filtered_df['Total followers']
        }
        print(data)
        convert_df = pd.DataFrame(data)
        fig = px.pie(convert_df, values='Followers', names='Location')
        st.plotly_chart(fig)


    st.subheader("Total Follower")
    filtered_df = follower_df.groupby('Month/Yr')[['Follower Count']].sum()
    data = {
        "Month/Yr": pd.to_datetime(follower_df['Date']),
        "Follower": follower_df['Follower Count']
    }
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Month/Yr'], y=data['Follower'], name='Follower Count'))
    st.plotly_chart(fig, picker=True, use_container_width=True, theme = None, height=1500)

    st.badge("New")
    st.subheader("Demographics")
    locations = st.multiselect("Pick the location", location_df['Location'])
    if locations:
        create_pie_chart('Location', 'Total followers', location_df, locations)
    st.dataframe(location_df)

    st.badge("New")
    st.subheader("Posting Frequency")
    post_count = df['Month & Year'].value_counts().sort_index()
    match_data = { month : post_count[month] for month in list(df['Month & Year'].unique())[::-1]}
    data = {
        "Month/Yr": list(match_data.keys()),
        "Number of Post": list(match_data.values())
    }
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Month/Yr'], y=data['Number of Post'], name='Post Frequency'))
    st.plotly_chart(fig, picker=True, use_container_width=True, theme = None, height=1500)
    st.dataframe(data)

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

    emoji = st.sidebar.multiselect("Pick the Emoji", df["Type Emoji"].unique())
    if not emoji:
        df8 = df7.copy()
    else:
        df8 = df7[df7["Type Emoji"].isin(emoji)]

    df["Impressions"].astype(int)

    def create_chart(category, aggregate, dataframe ):
        group_keys = list(dataframe.groupby(category).groups.keys())
        filtered_df = dataframe.groupby(category)[['Impressions']].mean().round()
        post_count = list(dataframe.groupby(category)['Number of Post'].sum())
        filtered_df.insert(0, category, group_keys)
        filtered_df.insert(1, "Post Count", post_count)
        organize_time = []
        organize_number_posts = []
        organize_impressions = []
        for i in group_keys:
            organize_time.append(i)
            organize_number_posts.append(filtered_df.loc[filtered_df[category] == i]['Post Count'].values[0])
            organize_impressions.append(filtered_df.loc[filtered_df[category] == i]['Impressions'].values[0])
        data = {
            category : organize_time,
            "Number of Posts": organize_number_posts,
            "Impressions" : organize_impressions
        }
        fig = px.bar(data, x=category, y="Impressions", template='seaborn')
        selected_bar = st.plotly_chart(fig, use_container_width=True, height=200, on_select='rerun')
        st.dataframe(data)
        st.badge("New")
        if selected_bar:
            if selected_bar['selection']['points']:

                post_data = {
                    "Post Title" : list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Post title']),
                    "Link" : list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Post link']),
                    'Impressions' :  list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Impressions']),
                    'Day' : list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Day of the week']),
                    "Date Posted" : list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Created date'].dt.date)
                }

                st.dataframe(post_data, use_container_width=True)



    if year:
        st.subheader(f"Year's Bar Chart")
        create_chart('Year', 'Impressions', df2)

    if month:
        st.subheader(f"Month's Bar Chart")
        create_chart('Month & Year', 'Impressions', df3)

    if day:
        st.subheader(f"Day Bar Chart")
        create_chart('Day of the week', 'Impressions', df4)

    if time:
        st.subheader(f"Time of Post Chart")
        create_chart('Interval Times', 'Impressions', df5)

    if category:
        st.subheader(f"Category Chart")
        create_chart('Category', 'Impressions', df6)

    if sub_category:
        st.subheader(f"Sub-Category Chart")
        create_chart('Sub-Category', 'Impressions', df7)

    if emoji:
        st.subheader(f"Emoji Chart")
        create_chart('Type Emoji', 'Impressions', df8)


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
