#!/usr/bin/python

#from plotly import subplots
from plotly import tools
#import plotly, openpyxl, datetime, sys, os
import plotly, datetime, sys, os
import plotly.offline as offline
import plotly.graph_objs as go
from shutil import copyfile
import pandas as pd

import Dashboard_TC_Dataframes


exe_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(exe_path)
grandparent_dir = os.path.dirname(parent_dir)
directory = os.path.dirname(grandparent_dir)
xl_file = os.path.join(directory, '_Dashboard_Reports\Thermocouples\ALL_TC_DATA.xlsx')

def main(remove_tc):
##    remove_tc = ['TC1-7', 'TC2-16', 'TC2-32', 'TC2-36', 'TC3-37', 'TC4-19', 'TC4-30']
    
    df = pd.read_excel(xl_file, encoding=sys.getfilesystemencoding())#, na_values=['NA'])

# FUNCTION TO CREATE LIST OF DATAFRAMES FOR EACH THERMOCOUPLE DEPTH
    df_list = Dashboard_TC_Dataframes.CreateDataframes(df)

    dfs = []
    for frame in df_list:
        frame_copy = frame.iloc[-168:]
        frame_copy = frame_copy.reset_index(drop=True)
        header = list(frame_copy.columns)
        frame_copy[header[0]].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        dfs.append(frame_copy)

#Check if last TC date is within last 10 days
    today = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    week_ago = today - week

    if dfs[1].iloc[-1][0] < week_ago:
        while True:
            print ''
            print 'Thermocouple data is older than 7 days. Continue?'
            print '  (1) Continue'
            print '  (2) Skip Thermocouple Chart'
            print '  (0) Exit'
            user_continue = raw_input('\nYour Selection: ')
            print ''

            if user_continue== '1':
                break
            elif user_continue == '2':
                return
            elif user_continue == '0':
                exit()
            else:
                continue

    # color_list = blue, green, orange, red, pink, 
    color_list1 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list2 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list3 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list4 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list5 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list6 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list7 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list8 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']
    color_list9 = ['rgb(51, 99, 255)', 'rgb(0, 133, 35)', 'rgb(255, 180, 41)', 'rgb(255, 69, 56)', 'rgb(211, 3, 252)']

    tc_data = []
    tc_index_dict = {'TC1': [], 'TC2': [], 'TC3': [], 'TC4': [], 'TC5': [], 'TC6': [], 'TC7': [], 'TC8': [], 'TC9': []}
    tc_index = 0
    for frame in dfs:
        header = list(frame.columns)

        _name = header[0].replace(' Date', '')
        if _name in remove_tc:
            continue

        _x = [x for x in frame[header[0]]]
        _y = [x for x in frame[header[1]]]
        
        if 'TC1' in header[0]:
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC1 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list1.pop(0)}
                })
            tc_index_dict['TC1'].append(tc_index)
        elif 'TC2' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC2 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list2.pop(0)}
                })
            tc_index_dict['TC2'].append(tc_index)
        elif 'TC3' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC3 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list3.pop(0)}
                })
            tc_index_dict['TC3'].append(tc_index)
        elif 'TC4' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC4 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list4.pop(0)}
                })
            tc_index_dict['TC4'].append(tc_index)
        elif 'TC5' in header[0]:
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC5 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list5.pop(0)}
                })
            tc_index_dict['TC5'].append(tc_index)
        elif 'TC6' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC6 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list6.pop(0)}
                })
            tc_index_dict['TC6'].append(tc_index)
        elif 'TC7' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC7 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list7.pop(0)}
                })
            tc_index_dict['TC7'].append(tc_index)
        elif 'TC8' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC8 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list8.pop(0)}
                })
            tc_index_dict['TC8'].append(tc_index)
        elif 'TC9' in header[0]: 
            tc_data.append({
                    'x': _x,
                    'y': _y,
                    'legendgroup': 'TC9 Group',
                    'name': _name,
                    'mode': 'lines',
                    'marker': {'color': color_list9.pop(0)}
                })
            tc_index_dict['TC9'].append(tc_index)
            
    fig = tools.make_subplots(rows=3, cols=3, print_grid=False)
    #fig = subplots.make_subplots(rows=2, cols=3, print_grid=False)

    for t in range(len(tc_data)):
        tc_trace = go.Scatter(tc_data[t])

        if 'TC1' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 1, 1)
        elif 'TC2' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 1, 2)
        elif 'TC3' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 1, 3)
        elif 'TC4' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 2, 1)
        elif 'TC5' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 2, 2)
        elif 'TC6' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 2, 3)
        elif 'TC7' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 3, 1)
        elif 'TC8' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 3, 2)
        elif 'TC9' in tc_data[t]['legendgroup']:
            fig.append_trace(tc_trace, 3, 3)

    fig['layout'].update(
            title='Temperature by Depth for Thermocouple Locations',
            titlefont=dict(
                family='Arial Black',
                color='black'
            ),
            margin = plotly.graph_objs.layout.Margin(
                l=50, # 50
                r=50, # 20
                b=75, # 75
                t=80, # 80
                pad=1 # 2
            ),
            autosize=True,
            plot_bgcolor='#efefef',
            font=dict(
                family='Segoe UI',
                color='black'
                ),
            legend=dict(
                x=1.01,
                y=0.95,
                bgcolor='#E2E2E2',
##                bordercolor='Black',
##                borderwidth=1,
                font=dict(
                    family='Segoe UI',
                    color='black',
                    size=11
                    )
                ),

            xaxis1=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis1=dict(
                title='Temperature (Deg. F)',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis2=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis2=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis3=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis3=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),

            xaxis4=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis4=dict(
                title='Temperature (Deg. F)',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis5=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis5=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis6=dict(
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis6=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),

            
            xaxis7=dict(
                title='Date',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis7=dict(
                title='Temperature (Deg. F)',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis8=dict(
                title='Date',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis8=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            xaxis9=dict(
                title='Date',
                titlefont=dict(
                    family='Arial Black',
                    color='black',
                    size=13
                    ),
                showline=True,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=8,
                showticklabels=True,
                tickangle=30,
                zeroline=False,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            yaxis9=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                gridcolor='#dddbdb',
                gridwidth=1,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                nticks=6,
                ticklen=4,
                tickwidth=2,
                mirror=True
                ),
            
            annotations=[
                dict(
                    text='TC1',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.14,
                    y=1.03,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    ),
                ),
                dict(
                    text='TC2',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=.5,
                    y=1.03,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    ),
                ),
                dict(
                    text='TC3',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=.87,
                    y=1.03,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    ),
                ),
                dict(
                    text='TC4',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.14,
                    y=0.646,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    ),
                ),
                dict(
                    text='TC5',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.646,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    ),
                ),
                dict(
                    text='TC6',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.87,
                    y=0.646,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    )
                ),
                dict(
                    text='TC7',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.14,
                    y=0.265,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    )
                ),
                dict(
                    text='TC8',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.265,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    )
                ),
                dict(
                    text='TC9',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.87,
                    y=0.265,
                    font=dict(
                        family='Arial Black',
                        color='black',
                        size=12
                    )
                ),
            ]
        )

    today = datetime.datetime.now()
    m = today.strftime("%m")
    d = today.strftime("%d")
    y = today.strftime("%Y")
    today = '{}-{}-{}'.format(y, m, d)

    dload = os.path.expanduser('~\Downloads')

    img_folder = os.path.join(directory, '_Dashboard_Reports\Report_Output\Images\{}'.format(today))
    if os.path.exists(img_folder) == True:
        pass
    else:
        os.mkdir(img_folder)

    html_folder = os.path.join(directory, '_Dashboard_Reports\Report_Output\HTML\{}'.format(today))
    if os.path.exists(html_folder) == True:
        pass
    else:
        os.mkdir(html_folder)

    img_name = '{} Thermocouples'.format(today)

    dload_path = os.path.join(dload, "{}.png".format(img_name))

    if os.path.exists(dload_path) == True:
        os.remove(dload_path)

    offline.plot(fig, filename='{}\_Dashboard_Reports\Report_Output\HTML\{}\{} Thermocouples.html'.format(directory, today, today), auto_open=True,
                 image='png', image_filename=img_name, image_width=1200, image_height=800)#1600x900

    while True:
        img_path = '{}\_Dashboard_Reports\Report_Output\Images\{}\{}.png'.format(directory, today, img_name)
        if os.path.exists(img_path) == False:
            print ''
            print 'Click "Save" when/if prompted.'
            print 'An image file will be saved to your downloads folder.'
            print 'If an image was not saved, you will have to generate this chart again.\n'
            print '  (1) "{}.png" was saved to downloads'.format(img_name)
            print '  (0) "{}.png" was not saved to downloads\n'.format(img_name)
            user_saved = raw_input('Your selection: ')

            if user_saved == '1':
                copyfile('{}\{}.png'.format(dload, img_name), img_path)
                break
            elif user_saved == '0':
                break
            else:
                print '\n'
                continue

        elif os.path.exists('{}\_Dashboard_Reports\Report_Output\Images\{}\{}.png'.format(directory, today, img_name)) == True:
            print ''
            print 'An image has already been generated for this data.'
            while True:
                print 'Do you want to replace the existing file?'
                print '  (Y) Yes, replace file.'
                print '  (N) Do not replace file.\n'
                user_replace = raw_input('Your selection: ')
                if user_replace.upper() == 'Y':
                    os.remove('{}\_Dashboard_Reports\Report_Output\Images\{}\{}.png'.format(directory, today, img_name))
                    copyfile('{}\{}.png'.format(dload, img_name), img_path)
                    break
                elif user_replace.upper() == 'N':
                    break
                else:
                    print '\n'
                    continue
        break

    print '\n******************************************************************************\n'


if __name__ == "__main__":
    remove_tc = ['TC1-7', 'TC2-16', 'TC2-32', 'TC2-36', 'TC3-37', 'TC4-19', 'TC4-30']
    main(remove_tc)
