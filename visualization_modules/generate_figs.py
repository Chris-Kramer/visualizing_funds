from visualization_modules.text_viz import *
import pandas as pd
from PIL import ImageColor


#############
# Bar plots #
#############
def generate_bar_chart(df, top_n = None, animated = False, words = None):
    """
    Wrapper function for generating frequncy bar charts
    """
    if animated:
        return create_animated_bar(df,
                                  x_col= "freqs",
                                  color_col = "avg_funding",
                                  color_label= "Average Funding pr. Grant",
                                  x_label = "Word Frequency",
                                  top_n = top_n,
                                  title = "Top {top_n} Most Used Words By Year")
    elif words is None:
        return create_bar_plot(df = gen_chart_data(df, top_n = top_n, yearly = False, sort_col = "funding"),
                              x_col = "freqs",
                              color_col = "avg_funding",
                              title = f" ",
                              color_label = "Average Funding pr. Grant",
                              x_label = "Frequency")
    elif words is not None:
        return create_bar_plot(df = gen_chart_data(df, yearly = False, sort_col = "funding", words=words),
                               x_col = "freqs",
                               color_col = "avg_funding",
                               title = f" ",
                               color_label = "Average Funding pr. Grant",
                               x_label = "Frequency")


#########
# Buble #
#########
X_STRETCH = 0.1
Y_STRETCH = 0.1

def generate_bubble_chart(df, top_n = 50, animated = False):
    """
    Wrapper function for creating bubble charts
    """

    if animated:
        return create_bubble_plot(df = gen_chart_data(df, top_n= top_n, yearly = True, sort_col = "funding"),
                          y_col = "funding",
                          x_col = "avg_funding",
                          size_col = "freqs",
                          color_col= "freqs",
                          y_strech = Y_STRETCH,
                          x_strech = X_STRETCH,
                          title=f"Top {top_n} Most Funded Words Each Year",
                          y_lab = "Combined Funding",
                          x_lab= "Average Funding pr. Grant",
                          size_lab = "Word Frequency",
                          color_lab = "Word Frequency")
    else:
        return create_bubble_plot(df = gen_chart_data(df, top_n = top_n, yearly = False, sort_col = "funding"),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f" ",
                                y_lab = "Combined Funding",
                                x_lab= "Average Funding pr. Grant",
                                size_lab = "Word Frequency",
                                color_lab = "Word Frequency")


def generate_bubble_words(df, words, animated = False):
    if animated:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "freqs", yearly = True, words = words),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f"Funding for Chosen words Each Year",
                                y_lab = "Number of Grants Containing Word",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Combined Funding for all Grants Containing Word",
                                color_lab = "Combined Funding for all Grants Containing Word")    
    else:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "funding", yearly = False, words = words),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f" ",
                                y_lab = "Combined Funding",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Frequency",
                                color_lab = "Frequency")
##########
# Graphs #
##########
def generate_graph_top_n(df, top_n = 10):
    """
    Wrapper for generating a graph over total word connectivity in a dataframe
    """
    G = generate_graph_data_all(df = df, top_n = top_n)
    return plot_graph(G, title = f" ")

def generate_graph_words(df, words):
    """
    Wrapper for generating a graph over connectivity between chosen words
    """
    G = generate_graph_data_words(df = df, words = words)
    return plot_graph(G, title = f" ")

def generate_graph_single_word(df, word, top_n):
    """
    Wrapper for generating a graph over connectivity for a chosen word
    """
    G = generate_graph_data_word(df = df, word = word, top_n = top_n)
    return plot_graph(G, title = f" ")    


def generateSankey(df, category_columns=None, all_inst = False):

    colorpalette = px.colors.qualitative.Dark24 + px.colors.qualitative.Light24 + px.colors.qualitative.Alphabet # hex values
    opacity = 0.5

    if all_inst:
        df["Institution"] = "All Institutions"
    
    df_sankey = df.loc[:,category_columns + ['Bevilliget beløb']] # if False we do not include the Institution column

    # create list of labels, i.e. unique values from each column except the values
    labels = []
    for col in category_columns:
        labels = labels + list(set(df_sankey[col].values)) # adds unique labels in each category to list

    # define colors based on number of labels
    color_dict_labels = dict(zip(labels, colorpalette)) # zips labels list with colorpalette

    # initiate input for for loop
    df_link_input = pd.DataFrame({'source' : [], 'target': [], 'count': []})

    # create data for go.Sankey function
    for i in range(len(category_columns)-1):
        if len(category_columns) == 1:
            print("Number of input categories must be at least 2")
        else:
            temporary_df = df_sankey.groupby([category_columns[i], category_columns[i+1]]).agg({'Bevilliget beløb':'sum'}).reset_index() # loop over columns and group by column to the right, i.e. 'År' and 'Virkemidler', and then 'Virkemidler' and 'Område'
            temporary_df.columns = ['source','target','count']
            df_link_input = df_link_input._append(temporary_df)

    # add index for source-target pair
    df_link_input['sourceID'] = df_link_input['source'].apply(lambda x: labels.index(x))
    df_link_input['targetID'] = df_link_input['target'].apply(lambda x: labels.index(x))

    # define colors based on source
    colorlist_source = [color_dict_labels[i] for i in df_link_input['source']] # loops over source column, and finds the value in the dictionary, and appends it to a new list. For example, the first 8 sources are 2022, so we append the value paired with our key, i.e. 2022.
    colorlist_source_rgba = ["rgba" + str(ImageColor.getcolor(color, "RGB") + (opacity, )) for color in colorlist_source] # converts hex colors to rgba

    # creating the sankey diagram
    fig = go.Figure(data=[go.Sankey(
        valueformat = ",",
        valuesuffix = " kr.",
        # define nodes
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = list(color_dict_labels.values())
            ),
        link = dict(
            source = df_link_input['sourceID'], # indices correspond to labels, e.g. '2022', 'Forskningsprojekt 1', 'Forskningsprojekt 2', ...
            target = df_link_input['targetID'],
            value = df_link_input['count'],
            color = colorlist_source_rgba
        ))])

    fig.update_layout(font_size=10, width=1200,
    height=600)
    return fig


# stacked area chart
def generateStacked_categories(df, institution_list, all_inst = False):
    if all_inst:
        df["Institution"] = "All Institutions"
        institution_list = ["All Institutions"]

    # categories Område - only the six biggest
    categories_list = ['Kultur og Kommunikation', 'Natur og Univers',
                       'Samfund og Erhverv', 'Sundhed og Sygdom',
                       'Teknologi og Produktion', 'Tværrådslig', 'Total Funding']

    # data for stacked
    df_stacked = df.groupby(['År', 'Institution']).agg({'Bevilliget beløb':'sum'}).reset_index()
    df_stacked['Område'] = 'Total Funding'

    prut = df.groupby(['År', 'Område', 'Institution']).agg({'Bevilliget beløb':'sum'}).reset_index()
    df_stacked_category = prut[prut['Område'].isin(categories_list)]
    df_stacked = pd.concat([df_stacked, df_stacked_category], axis=0)
 
    years = list(set(df["År"]))
    for cat in categories_list:
        test_df = df_stacked.loc[(df_stacked["Område"] == cat)]
        for year in years:
            test_df = test_df.loc[(test_df["År"] == year)]
            for inst in institution_list:
                test_df = test_df.loc[(test_df["Institution"] == inst)]
                if len(test_df) == 0:
                    df_row = pd.DataFrame({"År":[year],
                                            "Område":[cat],
                                            "Institution":[inst],
                                            "Bevilliget beløb":[0]})
                    df_stacked = pd.concat([df_stacked, df_row])
    df_stacked = df_stacked.groupby(['År', 'Område', 'Institution']).agg({'Bevilliget beløb':'sum'}).reset_index()

    df_stacked_category = df_stacked[df_stacked['Område'].isin(categories_list)]

    df_stacked_all = df_stacked_category.groupby(['År', 'Område']).agg({'Bevilliget beløb':'sum'}).reset_index()
    
    df_stacked_institution = df_stacked_category[df_stacked_category['Institution'].isin(institution_list)]

    # Comparisson variables
    if len(institution_list)>=2:
        #titel = 'Funding over time for ' + str(institution_list[0]) + ' and ' + str(institution_list[1])
        height, width = len(institution_list)*250, 1000
    else:
        #titel = 'Funding over time for ' + str(institution_list[0])
        height, width = 300, 1000

    # figure
    if any("All Periods" in string for string in institution_list): # if All Periods is checked of new figure
        fig = px.area(df_stacked_all,
                  x="År",
                  y='Bevilliget beløb',
                  facet_col='Område',
                  color='Område',
                  title="",
                  category_orders={"Område": categories_list},
                  height=height, width=width,
                  labels={"År": "Year", "Bevilliget beløb": "Granted amount"})
    else:
        fig = px.area(df_stacked_institution,
                  x="År",
                  y='Bevilliget beløb',
                  facet_col='Område',
                  color='Område',
                  facet_row='Institution',
                  title="",
                  category_orders={"Område": categories_list},
                  height=height, width=width,
                  labels={"År": "Year", "Bevilliget beløb": "Granted amount"})   



    # remove '=' from titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    # font size
    fig.update_layout(font = dict(size = 10, color = "Black"), showlegend=False)
    fig.update_xaxes(dtick=1, tickangle=90)

    return fig

