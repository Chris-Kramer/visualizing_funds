import streamlit as st
import pandas as pd
from visualization_modules.generate_figs import generate_bar_chart, generate_bubble_chart, generate_bubble_words, generate_graph_top_n, generate_graph_words, generate_graph_single_word, generateSankey, generateStacked_categories
from visualization_modules.text_viz import get_all_words, generate_data

# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")

## Load dataset
full_df = pd.read_csv('data/dff.csv', index_col=False)

## Fetch data
institution = []
for i in full_df['Institution']:
    if i not in institution and str(i) != 'nan':
        institution.append(i)

with st.sidebar:
    st.markdown(f"[Home](#home)")
    st.markdown(f"[Distribution of Research Grants](#sankey)")
    st.markdown(f"[Scientific  Areas Funded](#stack)")
    st.markdown(f"[Most Researched Topics](#bar)")
    st.markdown(f"[How Research Topics are Funded](#bubble)")
    st.markdown(f"[Connectivity Between Research Topics](#connectivity)")
    st.markdown(f"[Compare Research Topics](#topicsearch)")

# Home
st.header("DFF Funding Explorer", anchor="home")
st.write("""
         This is a minor personal project. It started as a university project, but I have since taken the data and tried to make it more visually appealing. 
         This dashboard visualisez how DFF (Danmarks Frie Forskningsfond) have funded different universities, sciencetific fields and research topics from 2013 to 2022
         The data have been scraped from DFF's public records of research grants and cleaned using pandas. It has been deployed with streamlit.  
         Hope you enjoy.  
         """)

# Select Institution
st.write(f"### Select Institution and Year")
st.write("**Choose Institution(s)**")
all_options = st.checkbox("Select all Institutions")
if all_options:
    locations = institution.copy()
    locations.append("All")
    st.multiselect("**Choose institutions**", options=locations, default="All", disabled=True, label_visibility="hidden")
    multi_choice = institution
    all_inst = True
    df = full_df 
    multi_choice_display = "All Institutions"   
else:
    locations = institution.copy()
    multi_choice = st.multiselect("**Choose institutions**", options=locations, default="Syddansk Universitet", disabled=False, label_visibility = "hidden")
    df = full_df.loc[full_df['Institution'].isin(multi_choice)]
    all_inst = False    
    multi_choice_display = ", ".join([str(choice) for i, choice in enumerate(multi_choice)])
stacked_df = df

year = st.slider("**Select Year Range**", 2013, 2022, (2020, 2022))
df = df.loc[(df["År"] >= year[0]) & (df["År"] <= year[1])]

if not df.empty:
    display_dict = {"Institution": [],
                    "Number of Projects": [],
                    "Total Funding": [],
                    "Average Project Funding": []}

    if "All" in locations:
        inst_choice = "All institutions"           
        all_sum = sum(full_df["Bevilliget beløb"])
        num_projects = len(full_df)
        try:
            avg_fund = all_sum//num_projects
        except ZeroDivisionError:
            avg_fund = 0
        display_dict["Institution"].append(inst_choice)
        display_dict["Average Project Funding"].append(avg_fund)
        display_dict["Total Funding"].append(all_sum)
        display_dict["Number of Projects"].append(num_projects)   
    else:
        for inst_choice in multi_choice:                
            temp_df = df.loc[(df["Institution"] == inst_choice)]                
            all_sum = sum(temp_df["Bevilliget beløb"]) if len(temp_df["Bevilliget beløb"]) > 0 else 0
            num_projects = len(temp_df)
            try:
                avg_fund = all_sum//num_projects
            except ZeroDivisionError:
                avg_fund = 0
            display_dict["Institution"].append(inst_choice)
            display_dict["Average Project Funding"].append(avg_fund)
            display_dict["Total Funding"].append(all_sum)
            display_dict["Number of Projects"].append(num_projects)                    
    display_df = pd.DataFrame.from_dict(display_dict)
    display_df['Average Project Funding (Millions)'] = display_df['Average Project Funding'].apply(lambda x: "${:.1f}M Dkk".format((x/1000000)))
    display_df['Total Funding (Millions)'] = display_df['Total Funding'].apply(lambda x: "{:.1f}M Dkk".format(x/1000000))
    display_df = display_df[["Institution", "Number of Projects", "Total Funding (Millions)", "Average Project Funding (Millions)"]]
    st.table(display_df, )
    "---"
    "\n"
    "\n"

    st.header(body = f"Distribution of Research Grants from {year[0]} to {year[1]}", anchor = "sankey")
    st.write(f"**Selected Institutions:** *{multi_choice_display}*")
    st.write("""This Sankey chart takes your previous filters and displays how the funding is flowing from a given year to a funding mechanism, to a university and to a scientific area.
    By hovering over each bar, you can get more detailed information about the funding flow and the exact amount of funding.""")
    sankey = generateSankey(df, category_columns=['År','Virkemidler', 'Institution', 'Område'], all_inst = all_inst)
    st.plotly_chart(sankey, use_container_width=True)    
    "---"
    "\n"
    "\n"

    st.header(f"Scientific  Areas Funded From {year[0]} to {year[1]}",  anchor = "stack")
    if len(multi_choice) == 0:

        st.write("Please select some institutions")

    else:
        st.write(f"**Selected Institutions:** *{multi_choice_display}*")
        st.write("""
        This stacked area chart displays,
        how much funding different research areas from the selected universities have recieved up during the selected years. 
        """)
        stacked_temp = df
        stacked = generateStacked_categories(stacked_temp, institution_list=multi_choice, all_inst = all_inst)
        st.plotly_chart(stacked, use_container_width=True)
        "---"
        "\n"
        "\n"

        st.header(f"Most Researched Topics From {year[0]} to {year[1]}",  anchor = "bar")
        st.write(f"**Selected Institutions:** *{multi_choice_display}*")
        st.write(
            """
            This barchart displays the words which appears in most titles.
            The colors of the bars indicates how much average funding each word has.
            You can hover over the bars to get the exact numbers for its funding and appearences in titles (frequency).
        """)
        top_n = st.select_slider("Use the slider below to change how many words you want to display.",
                    options=[i for i in range(10, 51)],
                    value = 50,
                    key = "top_n_bar_slider")
        barchart = generate_bar_chart(df, animated = False, top_n = top_n)
        st.plotly_chart(barchart, use_container_width=True)
        "---"
        "\n"
        "\n"
        "\n"

        st.header(f"How Research Topics are Funded From {year[0]} to {year[1]}",  anchor = "bubble")
        st.write(f"**Selected Institutions:** *{multi_choice_display}*")
        st.write(
            """
            This bubble plot shows the words with the highest combined funding and plots it.
            The combined funding is indicated vertically and the average funding horizontally.
            Word markers at the top of the plot have a high combined funding, and word markers at the furthest right have a high average funding.
            The color and size indicates how many titles the word appears in (word frequency).
            You can hover over the word marker to get the exact numbers for its funding and appearences in titles.  
            """)
        top_n = st.select_slider("Use the slider below to change how many topics you wish to display.",
                    options=[i for i in range(10, 81)],
                    value = 50,
                    key = "top_n_bub_slider")
        bubchart = generate_bubble_chart(df, top_n = top_n, animated = False)
        st.plotly_chart(bubchart, use_container_width=True)
        "---"
        "\n"
        "\n"

        st.header(f"Connectivity Between Topics From {year[0]} to {year[1]}",  anchor = "connectivity")
        st.write(f"**Selected Institutions:** *{multi_choice_display}*")
        st.write(
        """
        This network graph displays which words (stopwords excluded) most frequently appear in the same title.
        The more often two words appear together the larger the line between them will be. 
        Therefore, words, which often appear in the same title, will have a more visible line between them.
        You can hover over the small number between the lines to see how strong the connection between two words are.
        Moreover, the size of the word marker is determined by its general connectivity.
        The general connectivity is a number for how many unique words a given word appears together with across all titles.\n
        """)
        slider_label = "Use the slider below to choose how many connections (number of lines) you wish to display."
        top_n = st.select_slider(slider_label,
                    options=[i for i in range(2, 81)],
                    value = 30,
                    key = "top_n_words_slider")
        graph_chart = generate_graph_top_n(df, top_n)
        st.plotly_chart(graph_chart, use_container_width=True)  
        "---"
        "\n"
        "\n"


        st.header(f"Compare Topics From {year[0]} to {year[1]}",  anchor = "topicsearch")
        st.write(f"**Selected Institutions:** *{multi_choice_display}*")
        avg_funding, funding, freqs =  generate_data(df = df,
                                                    funding_thresh_hold = 0)
        all_words = get_all_words(df)

        selected_words = st.multiselect("Select Topic:", options = all_words, default = all_words[0], ) 
        selected_words = [str(s_word) for s_word in selected_words] # Convert to strings

        word_col1, word_col2, word_col3, word_col4, word_col5, word_col6 = st.columns([1,3,3,3,3,1], gap="medium")  
        with word_col2:
            st.write("**Selected Topics:**")
            for word in selected_words:
                st.write(f"{word}")
        with word_col3:
            st.write("**Combined Funding:**")
            for word in selected_words:
                st.write(f"{funding[word]:,} DKK")
        with word_col4:
            st.write("**Average Funding:**")
            for word in selected_words:
                st.write(f"{avg_funding[word]:,} DKK")   
        with word_col5:
            st.write("**Times used in Title:**")
            for word in selected_words:
                st.write(f"{freqs[word]}")
        # Extra linespace
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        with st.expander("*Description*", expanded=True):
            st.write(
                """
                - *Combined Funding:* Sum of all funding for titles which contain the chosen word.
                - *Average Funding:* The average funding for each title containing the chosen word, calculated thusly: *Combined Funding / Times Used in Title*
                - *Times Used in Title:* How many different titles the word appears in.
                """)                
        "---"

else:
    st.write("**No data to display **")



