import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit_authenticator as stauth
from streamlit import session_state, sidebar
import pickle
from pathlib import Path
import streamlit_authenticator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="LinkedIn Analytics!!", page_icon="📈", layout='wide')

# --- USER AUTHENTICATION ---

names = ['Trillium Trading']
usernames = ['ttrading']

# -- Load Data --
file_path = Path(__file__).parent / "hash_pw.pl"

with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

credentials = {
    'usernames': {
        'ttrading': {
            'email': 'jsmith@gmail.com',
            'name': 'Trillium Trading',
            'password': hashed_passwords[0]
        }
    }
}
authenticator = stauth.Authenticate(credentials, 'Linkedin Analytics!!', 'abcdef', 30)
name, authentication_status, username = authenticator.login("main", 5)

if authentication_status is False:
    st.error("Incorrect")

if authentication_status is None:
    st.warning("Please enter")

if authentication_status:

    authenticator.logout('Logout', 'sidebar')
    st.sidebar.title("Welcome to Trillium")

    sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
    content_sheet_name = 'Content'
    follower_sheet = 'Sheet24'
    location_sheet = 'Sheet25'
    job_function_sheet = 'Sheet26'
    industry_sheet = 'Sheet27'
    #
    # Construct the URL for CSV export
    content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
    follower_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={follower_sheet}'
    location_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={location_sheet}'
    job_function_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={job_function_sheet}'
    industry_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={industry_sheet}'

    st.logo('trillium_logo.png', link='https://www.trlm.com/', size='large', icon_image='trillium_trading_logo.png')
    st.title("📈 Linkedin Analytics")
    st.markdown('<style>div.block-container{padding-top:2rem;} </style>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Default Information", "Filtered Data", "Compare Data"])

    df = pd.read_csv(content_csv_url)
    follower_df = pd.read_csv(follower_csv_url)
    location_df = pd.read_csv(location_sheet_url)
    job_function_df = pd.read_csv(job_function_sheet_url)
    industry_df = pd.read_csv(industry_sheet_url)

    df['Created date'] = pd.to_datetime(df['Created date'])

    startDate = pd.to_datetime(df["Created date"]).min()
    endDate = pd.to_datetime(df["Created date"]).max()

    with tab1:
        def create_pie_chart(category, aggregate, dataframe, array):
            group_keys = array
            filtered_df = dataframe.groupby(category)[[aggregate]].sum()
            filtered_df = filtered_df.loc[array]
            data = {
                'Location': array,
                "Followers": filtered_df[aggregate]
            }
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
        st.plotly_chart(fig, picker=True, use_container_width=True, theme=None, height=1500)
        st.divider()
        st.badge("New")
        st.header("Demographics:")
        follower, views = st.columns(2)

        with follower:
            st.subheader("Total Followers Demographics")
            locations = st.multiselect("Pick the Location", location_df['Location'])
            if locations:
                create_pie_chart('Location', 'Total followers', location_df, locations)
            follower_total_data = {
                'Location': location_df['Location'],
                "Total followers": location_df['Total followers']
            }
            st.dataframe(follower_total_data)

        with views:
            st.subheader("Total Views Demographics")
            locations_view = st.multiselect("Pick the Location", location_df['Location View'])
            if locations_view:
                create_pie_chart('Location View', 'Total views', location_df, locations_view)
            follower_total_data = {
                'Location': location_df['Location View'],
                "Total views": location_df['Total views']
            }
            st.dataframe(follower_total_data)

        with follower:
            st.divider()
            st.subheader("Job Field")
            fields = st.multiselect("Pick the Job Field", job_function_df['Job function'])
            if fields:
                create_pie_chart('Job function', 'Total followers', job_function_df, fields)
            follower_total_data = {
                'Job': job_function_df['Job function'],
                'Total followers': job_function_df['Total followers']
            }
            st.dataframe(follower_total_data)

        with views:
            st.divider()
            st.subheader("Job View")
            job_view = st.multiselect("Pick the Job Field", job_function_df['Job View'])
            if job_view:
                create_pie_chart('Job View', 'Total views', job_function_df, job_view)
            follower_total_data = {
                'Job': job_function_df['Job View'],
                'Total views': job_function_df['Total views']
            }
            st.dataframe(follower_total_data)

        with follower:
            st.divider()
            st.subheader("Industry Field")
            industry_fields = st.multiselect("Pick the Industry Field", industry_df['Industry'])
            if industry_fields:
                create_pie_chart('Industry', 'Total followers', industry_df, industry_fields)
            follower_total_data = {
                'Industry': industry_df['Industry'],
                'Total followers': industry_df['Total followers']
            }
            st.dataframe(follower_total_data)

        with views:
            st.divider()
            st.subheader("Industry View")
            industry_view = st.multiselect("Pick the Industry Field", industry_df['Industry View'])
            if industry_view:
                create_pie_chart('Industry', 'Total views', industry_df, industry_view)
            follower_total_data = {
                'Industry': industry_df['Industry'],
                'Total views': industry_df['Total views']
            }
            st.dataframe(follower_total_data)

        st.divider()
        st.subheader("Posting Frequency")
        post_count = df['Month & Year'].value_counts().sort_index()
        match_data = {month: post_count[month] for month in list(df['Month & Year'].unique())[::-1]}
        data = {
            "Month/Yr": list(match_data.keys()),
            "Number of Post": list(match_data.values())
        }
        x = np.array(data['Month/Yr'])
        y = np.array(data['Number of Post'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Month/Yr'], y=data['Number of Post'], name='Post Frequency'))
        st.plotly_chart(fig, picker=True, use_container_width=True, theme=None, height=1500)
        st.dataframe(data)

    with (tab2):
        df["Impressions"].astype(int)
        df["Clicks"].astype(int)
        df["Click through rate (CTR)"].astype(int)
        df["Engagement rate"].astype(int)

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

        type_post = st.sidebar.multiselect('Pick the type of Post', df['Type of Post'].unique())
        if not type_post:
            df9 = df8.copy()
        else:
            df9 = df8[df8['Type of Post'].isin(type_post)]

        agg = st.sidebar.multiselect("Pick the Aggregate",
                                     ['Impressions', 'Clicks', 'Click through rate (CTR)', 'Engagement rate'])

        def process_changes(key_name):
            editor_state = st.session_state.get(key_name, {})
            deleted = editor_state.get('deleted_rows', {})
            st.write(f'Processed Changes')
            st.write(f'Deleted Rows {deleted}')

        @st.fragment
        def show_edit_chart(edit_frame, main_category, category_select, aggregate, all_data, dynamic_key, chart_key):
            edit_posts = st.data_editor(
                edit_frame,
                key=dynamic_key,
                hide_index=True,
                num_rows='dynamic',
                on_change=process_changes(dynamic_key),
            )
            edit_posts = pd.DataFrame(edit_posts)

            new_agg = edit_posts[aggregate].mean().round()
            for idx, value in enumerate(all_data[main_category]):
                if value == category_select:
                    all_data[aggregate][idx] = new_agg
            st.write(new_agg)
            if st.button("Show Edits"):
                fig_plot = px.bar(all_data, x=main_category, y=aggregate, template='seaborn', color=main_category)
                st.plotly_chart(fig_plot, use_container_width=True, height=200, key=chart_key)

                st.dataframe(all_data)


        def create_chart(category, aggregate, dataframe, dynamic_key, chart_key):

            st.subheader(f"{category} {aggregate} Chart")
            group_keys = list(dataframe.groupby(category).groups.keys())
            filtered_df = dataframe.groupby(category)[[aggregate]].mean()
            post_count = list(dataframe.groupby(category)['Number of Post'].sum())
            filtered_df.insert(0, category, group_keys)
            filtered_df.insert(1, "Post Count", post_count)

            organize_time = []
            organize_number_posts = []
            organize_impressions = []

            if aggregate == 'Impressions' or aggregate == 'Clicks':
                for i in group_keys:
                    organize_time.append(i)
                    organize_number_posts.append(filtered_df.loc[filtered_df[category] == i]['Post Count'].values[0])
                    organize_impressions.append(filtered_df.loc[filtered_df[category] == i][aggregate].values[0].round())

            elif aggregate == 'Engagement rate' or aggregate == 'Click through rate (CTR)':
                for i in group_keys:
                    organize_time.append(i)
                    organize_number_posts.append(filtered_df.loc[filtered_df[category] == i]['Post Count'].values[0])
                    organize_impressions.append(
                        (filtered_df.loc[filtered_df[category] == i][aggregate].values[0] * 100).round(2))

            data = {
                category: organize_time,
                "Number of Posts": organize_number_posts,
                aggregate: list(organize_impressions)
            }

            fig = px.bar(data, x=category, y=aggregate, template='seaborn', color=category)
            selected_bar = st.plotly_chart(fig, use_container_width=True, height=200, on_select='rerun')
            st.dataframe(data)

            if selected_bar:
                if selected_bar['selection']['points']:
                    post_data = {
                        "Post Title": list(
                            dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]][
                                'Post title']),
                        "Link": list(
                            dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]]['Post link']),
                        aggregate: list(
                            dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]][aggregate]),
                        'Day': list(dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]][
                                        'Day of the week']),
                        "Date Posted": list(
                            dataframe.loc[dataframe[category] == selected_bar['selection']['points'][0]["x"]][
                                'Created date'].dt.date),
                    }
                    st.dataframe(post_data)
                    show_edit_chart(post_data, category, selected_bar['selection']['points'][0]["x"], aggregate, data, dynamic_key, chart_key)


        if year:
            st.subheader(f"Year's Bar Chart")
            for a in agg:
                create_chart('Year', a, df2, 'dynamic2', 'chart3')
            st.divider()

        if month:
            st.subheader(f"Month's Bar Chart")
            for a in agg:
                create_chart('Month & Year', a, df3, 'dynamic3', 'chart4')
            st.divider()

        if day:
            st.subheader(f"Day Bar Chart")
            for a in agg:
                create_chart('Day of the week', a, df4, 'dynamic4', 'chart5')
            st.divider()

        if time:
            st.subheader(f"Time of Post Chart")
            for a in agg:
                create_chart('Interval Times', a, df5, 'dynamic5', 'chart6')
            st.divider()

        if category:
            st.subheader(f"Category Chart")
            for a in agg:
                create_chart('Category', a, df6, 'dynamic6', 'chart7')
            st.divider()

        if sub_category:
            st.subheader(f"Sub-Category Chart")
            for a in agg:
                create_chart('Sub-Category', a, df7, 'dynamic7', 'chart8')
            st.divider()

        if emoji:
            st.subheader(f"Emoji Chart")
            for a in agg:
                create_chart('Type Emoji', a, df8, 'dynamic8', 'chart9')
            st.divider()

        if type_post:
            st.subheader(f"Type Post Chart")
            for a in agg:
                create_chart('Type of Post', a, df9, 'dynamic9', 'chart10')
    with tab3:

        # Sidebar option
        st.sidebar.title("Analysis Options")
        analysis_option = st.sidebar.selectbox("Choose an analysis", ["TF-IDF Similarity Clustering"])


        # Load data
        @st.cache_data
        def load_data():
            sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
            content_sheet_name = 'Content'
            content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
            return pd.read_csv(content_csv_url)  # Change this path as needed

        df = load_data()

        if analysis_option == "TF-IDF Similarity Clustering":
            st.title("Detect Similar Posts Using TF-IDF")

            # Ensure 'Content' column exists
            if "Post title" not in df.columns:
                st.error("No 'Post title' column found in dataset.")
            else:
                # Fill NaNs with blanks for text processing
                contents = df['Post title'].fillna("")

                # Compute TF-IDF
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(contents)

                # Compute cosine similarity
                cos_sim = cosine_similarity(tfidf_matrix)

                # Flag similar pairs above threshold
                threshold = 0.5
                similar_pairs = np.argwhere((cos_sim > threshold) & (cos_sim < 1.0))
                similar_df = pd.DataFrame(similar_pairs, columns=['Post A', 'Post B'])

                # Drop duplicates (e.g. (1,2) and (2,1))
                similar_df = similar_df[similar_df['Post A'] < similar_df['Post B']]

                st.subheader(f"Posts with Similarity > {threshold}")
                st.write(similar_df)
                print(df.iloc[68]['Year'])
                # Optionally show the actual text
                for _, row in similar_df.iterrows():
                    idx_a = row['Post A']
                    idx_b = row['Post B']
                    st.markdown(f"**Pair {idx_a} & {idx_b}:**")
                    st.text(f"Post A: {contents.iloc[idx_a]}")
                    a_similar_data = {
                        "Date posted": df.iloc[idx_a]['Created date'],
                        "Impression count": df.iloc[idx_a]['Impressions']
                    }
                    st.dataframe(a_similar_data)

                    st.text(f"Post B: {contents.iloc[idx_b]}")

                    b_similar_data = {
                        "Date posted": df.iloc[idx_b]['Created date'],
                        "Impression count": df.iloc[idx_b]['Impressions']
                    }
                    st.dataframe(b_similar_data)
