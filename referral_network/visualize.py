import json

import networkx as nx
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.offline as py
from collections import deque
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def queue(a, b, qty):
    """either x0 and x1 or y0 and y1, qty of points to create"""
    q = deque()
    q.append((0, qty - 1))  # indexing starts at 0
    pts = [0] * qty
    pts[0] = a
    pts[-1] = b  # x0 is the first value, x1 is the last
    while len(q) != 0:
        left, right = q.popleft()  # remove working segment from queue
        center = (left + right + 1) // 2  # creates index values for pts
        pts[center] = (pts[left] + pts[right]) / 2
        if right - left > 2:  # stop when qty met
            q.append((left, center))
            q.append((center, right))
    return pts


def make_middle_points(first_x, last_x, first_y, last_y, qty):
    """line segment end points, how many midpoints, hovertext"""
    # Add 2 because the origin will be in the list, pop first and last (the nodes)
    middle_x_ = queue(first_x, last_x, qty + 2)
    middle_y_ = queue(first_y, last_y, qty + 2)
    middle_x_.pop(0)
    middle_x_.pop()
    middle_y_.pop(0)
    middle_y_.pop()
    return middle_x_, middle_y_


def make_edge(x, y, text, width, color):
    return  go.Scatter(x         = x,
                       y         = y,
                       line      = dict(width = width, color = color),
                       hoverinfo = 'text',
                       text      = ([text]),
                       mode      = 'lines')


def make_edge_middlepoints(x, y, text, opc, col):
    return  go.Scatter(x         = x,
                       y         = y,
                       marker=go.scatter.Marker(opacity=opc),
                       hovertemplate="Edge %{hovertext}<extra></extra>",
                       hovertext=text,
                       mode      = "markers",
                       marker_size = 1,
                       marker_color = col,
                       showlegend=False)


def make_graph(path: str):

    print("creating graph...")

    synthetic_referral = pd.read_csv(path)


    common_nodes = list(set(synthetic_referral['Referred To']).intersection(set(synthetic_referral['Referred From'])))

    synthetic_referral_grp = synthetic_referral.groupby(['Referred From','Referred To']).\
                apply(lambda s: pd.Series({"Days to Schedule": s["Days to Schedule"].median(), \
                                        "count_of_appointments": s["Days to Schedule"].count(),})).reset_index()

    synthetic_referral_grp['weight'] = \
                MinMaxScaler().fit_transform(np.array(synthetic_referral_grp['Days to Schedule']).reshape(-1,1))



    synthetic_referral_grp['weight_standard'] = \
                StandardScaler().fit_transform(np.array(synthetic_referral_grp['Days to Schedule']).reshape(-1,1))

    synthetic_referral_grp['weigh_scaled'] = 2*synthetic_referral_grp['weight']**4

    synthetic_referral_grp['weigh_scaled_0_10'] = np.floor(1 + (synthetic_referral_grp['Days to Schedule']/synthetic_referral_grp['Days to Schedule'].max())*9)



    synthetic_referral_grp['Schedule_Bins'] = np.where(synthetic_referral_grp['Days to Schedule']<50, 50,
                                    np.where(synthetic_referral_grp['Days to Schedule']<150, 150,
                                            np.where(synthetic_referral_grp['Days to Schedule']<300, 300, 
                                                        400)))

    synthetic_referral_grp['Schedule_Bins'] = np.where(synthetic_referral_grp['Days to Schedule']<=50, 50,
                                    np.where(synthetic_referral_grp['Days to Schedule']<=250, 250, 400))



    synthetic_referral_grp['weight'] = np.where(synthetic_referral_grp['count_of_appointments']<=50, .008,
                                    np.where(synthetic_referral_grp['count_of_appointments']<=150, .04,
                                            np.where(synthetic_referral_grp['count_of_appointments']<=250, .15, 
                                                        .4)))

    synthetic_referral_grp['Schedule_Bins_color'] = np.where(synthetic_referral_grp['Schedule_Bins']==50, 'green',
                                    np.where(synthetic_referral_grp['Schedule_Bins']==250,'orange','red'))

    #### Keeping only the required columns
    synthetic_referral_grp = synthetic_referral_grp[['Referred From', 'Referred To', 'Days to Schedule',\
                                                    'count_of_appointments', 'weight', 'Schedule_Bins',\
                                                    'Schedule_Bins_color']]

    synthetic_referral_grp['weight_for_layout'] = synthetic_referral_grp['Days to Schedule']*\
                                                    synthetic_referral_grp.count_of_appointments

    synthetic_referral_grp['weight_for_layout'] = \
        StandardScaler().fit_transform(np.array(synthetic_referral_grp['weight_for_layout']).reshape(-1,1))







    node_size_list = list(synthetic_referral['Referred From'])+list(synthetic_referral['Referred To'])

    #nodesize = dict(zip(synthetic_referral_cnt['Referred From'],synthetic_referral_cnt['Referred To Scaled']))

    node_size = dict()
    for i in sorted(node_size_list):
        node_size[i] = node_size.get(i, 0)+1

    node_size_scaled = pd.DataFrame(list(node_size.items()), columns=['node','appearnce_cnt'])
    node_size_scaled['appearnce_cnt_scaled'] = \
            np.floor(1 + (node_size_scaled['appearnce_cnt']/node_size_scaled['appearnce_cnt'].max())*24)


    nodesize = dict(zip(node_size_scaled['node'],node_size_scaled['appearnce_cnt_scaled']))


    outgoing_connection =  list(synthetic_referral['Referred From'])
    node_size_og = dict()
    for i in sorted(outgoing_connection):
        node_size_og[i] = node_size_og.get(i, 0)+1
        
    node_size_og = pd.DataFrame(list(node_size_og.items()), columns=['node','og_appearnce_cnt'])


    incoming_connection =  list(synthetic_referral['Referred To'])
    node_size_in = dict()
    for i in sorted(incoming_connection):
        node_size_in[i] = node_size_in.get(i, 0)+1
        
    node_size_ic = pd.DataFrame(list(node_size_in.items()), columns=['node','in_appearnce_cnt'])


    outgoing_connection =  list(synthetic_referral['Referred From'])
    node_size_og = dict()
    for i in sorted(outgoing_connection):
        node_size_og[i] = node_size_og.get(i, 0)+1
        
    node_size_og = pd.DataFrame(list(node_size_og.items()), columns=['node','og_appearnce_cnt'])


    incoming_connection =  list(synthetic_referral['Referred To'])
    node_size_in = dict()
    for i in sorted(incoming_connection):
        node_size_in[i] = node_size_in.get(i, 0)+1
        
    node_size_ic = pd.DataFrame(list(node_size_in.items()), columns=['node','in_appearnce_cnt'])

    G = nx.from_pandas_edgelist(synthetic_referral_grp,source='Referred From',target='Referred To',\
                                edge_attr='weight_for_layout', create_using=nx.Graph())
    pos = nx.spring_layout(G)

    G = nx.from_pandas_edgelist(synthetic_referral_grp,source='Referred From',target='Referred To',\
                                edge_attr='weight', create_using=nx.Graph())

    referral = G
    pos_ = pos

    EDGE_POINTS_QUANTITY = 20
    EDGE_POINTS_OPACITY = 0.01

    edge_trace = []
    edge_md_trace = []

    for edge in referral.edges():
        
        #if referral.edges()[edge]['weight'] > 0.5:
        char_1 = edge[0]
        char_2 = edge[1]

        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]

        text   = ''#str(char_1) + '--' + str(char_2) + ': ' + str(referral.edges()[edge]['weight'])
        
        col = ''
        color_line = synthetic_referral_grp.query(f'`Referred From`=={char_1} & `Referred To`=={char_2}')
        
        if not(color_line.empty):
            col = color_line['Schedule_Bins_color'].item()
        else:
            color_line = synthetic_referral_grp.query(f'`Referred To`=={char_1} & `Referred From`=={char_2}')
            col = color_line['Schedule_Bins_color'].item()

        trace  = make_edge([x0, x1, None], [y0, y1, None], text, referral.edges()[edge]['weight'], col)
                        #0.002*referral.edges()[edge]['weight']**2)
            
        edge_trace.append(trace)
        
        edge_width_condition = color_line['weight'].item()
        if(edge_width_condition>0.008):
            median_days_to_schedule = color_line['Days to Schedule'].item()
            number_of_encounters = color_line['count_of_appointments'].item()
            edge_middle_x, edge_middle_y, edge_middle_text = [], [], []
            middle_x, middle_y = make_middle_points(x0, x1, y0, y1, EDGE_POINTS_QUANTITY)
            edge_middle_x.extend(middle_x)
            edge_middle_y.extend(middle_y)
            edge_middle_text.extend([f"{char_1} - {char_2}<br>Median Days To Schedule {median_days_to_schedule}<br>Number of Encounters {number_of_encounters}"] * EDGE_POINTS_QUANTITY)

            trace = make_edge_middlepoints(edge_middle_x,edge_middle_y,edge_middle_text,EDGE_POINTS_OPACITY,col)
            edge_md_trace.append(trace)
        
    # Make a node trace
    node_trace = go.Scatter(x         = [],
                            y         = [],
                            text      = [],
                            textposition = "top center",
                            textfont_size = 7,
                            mode      = 'markers+text',
                            hoverinfo = 'text',
                            hovertext = ([text]),
                            marker    = dict(color = [],
                                            size  = [],
                                            line  = None))

    # For each node in referral, get the position and size and add to the node_trace
    for node in referral.nodes():
        x, y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        
        if(node in common_nodes):
            node_trace['marker']['color'] += tuple(['cornflowerblue'])
        elif(node in list(node_size_og.node)):
            node_trace['marker']['color'] += tuple(['MidnightBlue'])
        else:
            node_trace['marker']['color'] += tuple(['Goldenrod'])
        
        
        node_trace['marker']['size'] += tuple([nodesize[node]])
        
        node_trace['text'] += tuple(['<b>' + str(node) + '</b>'])
        
        n_ofconnections = node_size_scaled.query(f'node=={node}')['appearnce_cnt'].item()
        
        n_ogconnections = 0
        n_icconnections = 0    
        if not(node_size_og.query(f'node=={node}').empty):
            n_ogconnections = node_size_og.query(f'node=={node}')['og_appearnce_cnt'].item()
        
        if not(node_size_ic.query(f'node=={node}').empty):
            n_icconnections = node_size_ic.query(f'node=={node}')['in_appearnce_cnt'].item()
            
    #     node_trace['hovertext'] += tuple(['<b>' + 'node:</b>'+ str(node) + '<br>' \
    #                                 + '<b>#connections:</b>' + str(n_ofconnections) + '</br>'])
        
        node_trace['hovertext'] += tuple(['<b>' + 'node:</b>'+ str(node) + '<br>' \
                                + '<b>#total connections:</b>' + str(n_ofconnections) + '<br>' 
                                + '<b>#out connections:</b>' + str(n_ogconnections) + '<br>'    
                                + '<b>#in connections:</b>' + str(n_icconnections) + '</br>'])

    x = list(node_trace.hovertext)
    x.pop(0)
    node_trace.hovertext = x
    width=1000
    height=700

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )


    fig = go.Figure(layout = layout)


    for trace in edge_trace:
        fig.add_trace(trace)

    for trace in edge_md_trace:
        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(
        showlegend = False,
        title=go.layout.Title(
            text="Network of Referral <br>"\
                +"<sup>The larger the node, the more connected it is to other departments.<br></sup>",
            xref="paper",
            x=0
        ),
        margin_b=90,
        annotations = [dict(xref='paper',
                            yref='paper',
                            x=0.5, y=-0.07,
                            showarrow=False,
                            text =  "<sup>Dark Blue nodes only make a referrals. Light blue nodes makes and receive referrals.Yellow nodes only receives referrals."
                                    +"Less visible edges indicate less than 50 referral. Somewhat visible edges mean 50-150 referrals. Visible edges indicate 150-250. Dense edges indicate more than 250 referrals.<br>"
                                    +"Red &#128308; edges indicate more than 250 days to schedule. Orange &#128992; edges indicate 50-250 days needed to schedule. Green &#128994; edges indicate 50 or less days need to schedule.<br>"
                                    +"For example, a red dense edge means more number of referrals and more time to schedule.<br>"
                                    +"</sup></br></br>"
                    )]
    )


    fig.update_xaxes(showticklabels = False)

    fig.update_yaxes(showticklabels = False)

    # fig.show()

    # py.plot(fig, filename='referrals3.html')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    print("returning graph...")

    return graphJSON


if __name__ == '__main__':
    visualize("/Users/jake/Projects/referral-network/referral_network/static/files/data.csv")