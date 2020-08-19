#!/usr/bin/python

import plotly
import plotly.offline as offline
import plotly.graph_objs as go
import datetime
import sys, os
from shutil import copyfile

# Global directory variable where '.txt' files are stored

exe_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(exe_path)
grandparent_dir = os.path.dirname(parent_dir)
directory = os.path.dirname(grandparent_dir)
#\Dashboard_Reporting

# Main function
def main():
    # Hardcode path to file
    f_path = os.path.join(directory, "CR6_TablePLC_SVE - Copy.txt")
    flow_dates, flow_min, flow_max, flow_avg = TablePLCRTO16Stats(f_path)

    
    f_path = os.path.join(directory, "CR6_TablePLC_RTO32 - Copy.txt")
    sys_fan_dates, fan_max = TablePLCRTO32(f_path)

    f_path = os.path.join(directory, "CR6_TablePLC_RTOFP - Copy.txt")
    pt101_dates, pt101 = TablePLCRTOFP(f_path)

    #flow_array_max, flow_array_min = get_array_min_max(flow_min, flow_max)

    # Plot line declarations
    # LEL 132 max data plot
    #ADD COLUMN NUMBER DATA WAS PULLED FROM FOR REFERENCE IN TXT FILE
    trace1 = go.Scatter(
        x=flow_dates,
        y=flow_min,
        name='Flow Min',
        )
    # LEL 300 max data plot
    trace2 = go.Scatter(
        x=flow_dates,
        y=flow_max,
        name='Flow Max',
        )
    # Cycle time data plot
    trace3 = go.Scatter(
        x=flow_dates,
        y=flow_avg,
        name='Flow Avg',
        )
    # System fan speed data plot
    trace4 = go.Scatter(
        x=sys_fan_dates,
        y=fan_max,
        name='SysFanHz',
        yaxis='y2',
        )
    # PT-101 inch w.c. data plot
    trace5 = go.Scatter(
        x=pt101_dates,
        y=pt101,
        name='PT-101',
        yaxis='y3'
        )

# State which lines to plot from traces declared above.
    data = [trace1, trace2, trace3, trace4, trace5]

# Layout options for chart formatting
    layout = go.Layout(
        title='Flow, System Fan Speed and PT-101 Data For Last Seven Days',
        titlefont=dict(
            family='Arial Black',
            color='black'
        ),
        #plot_bgcolor='#efefef',
        autosize=True,
        # Chart margin - where to position chart on screen
        margin = plotly.graph_objs.layout.Margin(
            l=50, # 75
            r=20, # 100
            b=75, # 100
            t=50, # 75
            pad=2 # 3
        ),
        xaxis=dict(
            # Position within declared margin [x, y]
            domain=[0.1, 0.85],
            title='Date',
            showline=True,
            # Axis tick mark fommatting
            tickangle=45,
            ticklen=4,
            tickwidth=2,
            mirror=True,
            titlefont=dict(
                family='Arial Black',
                color='black'
            ),
        ),
        yaxis=dict(
            title='Flow (scfm)',
            range=[400, 600],
            showline=True,
            zeroline=False,
            ticks='outside',
            ticklen=4,
            tickwidth=2,
            tickcolor='#000',
            titlefont=dict(
                family='Arial Black',
                color='black'
            ),
        ),
        yaxis2=dict(
            title='RTO System Fan Speed (Hz)',
            range=[20, 30],
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            ticks='outside',
            ticklen=4,
            tickwidth=2,
            tickcolor='#d62728',
            titlefont=dict(
                family='Arial Black',
                color='#d62728'
            ),
        ),
        yaxis3=dict(
            title='Vacuum @ Pt-101 (inch w.c.)',
            range=[-4, -1],
            overlaying='y',
            position=0,
            anchor='free',
            side='left',
            showgrid=False,
            showline=True,
            zeroline=False,
            ticks='outside',
            ticklen=4,
            tickwidth=2,
            tickcolor='#9467bd',
            titlefont=dict(
                family='Arial Black',
                color='#9467bd'
            ),
        ),
        
        legend=dict(
            x=0.25,
            y=-0.10,
            traceorder='normal',
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            borderwidth=2,
            orientation='h',
        ),
        font=dict(
            family="Segoe UI",
            size=11,
            color="#000"
        )
    )

# Get the last date in file for HTML file name format
    today = datetime.datetime.now()
    m = today.strftime("%m")
    d = today.strftime("%d")
    y = today.strftime("%Y")
    today = '{}-{}-{}'.format(y, m, d)

# Generate figure functions
    fig = go.Figure(data=data, layout=layout)
    # offline.plot keeps all data local. Stores output file as HTML and opens in
    # default browser when program is run

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

    img_name = '{} Flow'.format(today)

    dload_path = os.path.join(dload, "{}.png".format(img_name))

    if os.path.exists(dload_path) == True:
        os.remove(dload_path)
    

    offline.plot(fig, filename='{}\_Dashboard_Reports\Report_Output\HTML\{}\{} Flow.html'.format(directory, today, today), auto_open=True,
                 image='png', image_filename=img_name, image_width=1200, image_height=800)

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




# Function to parse TablePLCRTO16Stats file
def TablePLCRTO16Stats(f_path):
    # Intermediate list that stores ALL data. Data is parsed from this list into the proceeding lists
    parameters = []
    flow_dates=[]
    i_flow_min = []
    i_flow_max = []
    i_flow_avg = []
    
    sd7_flow_min = []
    sd7_flow_max = []
    sd7_flow_avg = []
    
    sd6_flow_min = []
    sd6_flow_max = []
    sd6_flow_avg = []

    flow_min = []
    flow_max = []
    flow_avg = []

    # Open file
    with open(f_path) as f:
        data = f.readlines()

    # 24 hours * 4 readings per hour * 5 days = 480 rows of parameters
    # 500 rows are fetched so technically > 5 days of data
    last5days = data[-700:]

    # Loop through the 500 rows of data
    for i in last5days:
        # Append each row of data to list delineated by comma (',')
        parameters.append([x.strip() for x in i.split(',')])

    # Each list item is now an entire row and a column can be called by an index
    # Create lists for each column of data needed to produce chart
    for fdate in parameters:
        # Column 0 = dates/times
        flow_dates.append(fdate[0].replace('"', ''))
        
    for fmin in parameters:
        i_flow_min.append(fmin[5])
    for fmax in parameters:
        i_flow_max.append(fmax[6])
    for favg in parameters:
        i_flow_avg.append(favg[7])

    for fmin in parameters:
        sd7_flow_min.append(fmin[47])
    for fmax in parameters:
        sd7_flow_max.append(fmax[48])
    for favg in parameters:
        sd7_flow_avg.append(favg[49])

    for fmin in parameters:
        sd6_flow_min.append(fmin[50])
    for fmax in parameters:
        sd6_flow_max.append(fmax[51])
    for favg in parameters:
        sd6_flow_avg.append(favg[52])


    # Remove first 4 items in list because not needed
    for n in range(0, 4):
        flow_dates.pop(0)
        i_flow_min.pop(0)
        i_flow_max.pop(0)
        i_flow_avg.pop(0)
        sd7_flow_min.pop(0)
        sd7_flow_max.pop(0)
        sd7_flow_avg.pop(0)
        sd6_flow_min.pop(0)
        sd6_flow_max.pop(0)
        sd6_flow_avg.pop(0)

    for i in range(len(flow_dates)):
        _min = float(i_flow_min[i]) + float(sd7_flow_min[i]) + float(sd6_flow_min[i])
        _max = float(i_flow_max[i]) + float(sd7_flow_max[i]) + float(sd6_flow_max[i])
        _avg = float(i_flow_avg[i]) + float(sd7_flow_avg[i]) + float(sd6_flow_avg[i])

        flow_min.append(_min)
        flow_max.append(_max)
        flow_avg.append(_avg)

    # Return lists (date column and combustion temp column)
    return flow_dates, flow_min, flow_max, flow_avg



def TablePLCRTO32(f_path):
    # Intermediate list that stores ALL data. Data is parsed from this list into the proceeding lists
    parameters = []
    sys_fan_dates=[]
    fan_max = []

    # Open file
    with open(f_path) as f:
        data = f.readlines()

    # 24 hours * 4 readings per hour * 5 days = 480 rows of parameters
    # 500 rows are fetched so technically > 5 days of data
    last5days = data[-700:]

    # Loop through the 500 rows of data
    for i in last5days:
        # Append each row of data to list delineated by comma (',')
        parameters.append([x.strip() for x in i.split(',')])

    # Each list item is now an entire row and a column can be called by an index
    # Create lists for each column of data needed to produce chart
    for fdate in parameters:
        # Column 0 = dates/times
        sys_fan_dates.append(fdate[0].replace('"', ''))
    for fmax in parameters:
        # Column 54 = max fan speed
        fan_max.append(fmax[54])

    # Remove first 4 items in list because not needed
    for n in range(0, 4):
        sys_fan_dates.pop(0)
        fan_max.pop(0)

    # Return lists (date column and combustion temp column)
    return sys_fan_dates, fan_max



def TablePLCRTOFP(f_path):
    # Intermediate list that stores ALL data. Data is parsed from this list into the proceeding lists
    parameters = []
    pt101_dates=[]
    pt101 = []

    # Open file
    with open(f_path) as f:
        data = f.readlines()

    # 24 hours * 4 readings per hour * 5 days = 480 rows of parameters
    # 500 rows are fetched so technically > 5 days of data
    last5days = data[-700:]

    # Loop through the 500 rows of data
    for i in last5days:
        # Append each row of data to list delineated by comma (',')
        parameters.append([x.strip() for x in i.split(',')])

    # Each list item is now an entire row and a column can be called by an index
    # Create lists for each column of data needed to produce chart
    for fdate in parameters:
        # Column 0 = dates/times
        pt101_dates.append(fdate[0].replace('"', ''))
    for fmax in parameters:
        # Column 54 = max fan speed
        pt101.append(fmax[24])

    # Remove first 4 items in list because not needed
    for n in range(0, 4):
        pt101_dates.pop(0)
        pt101.pop(0)

    # Return lists (date column and combustion temp column)
    return pt101_dates, pt101


if __name__ == "__main__":
    main()
