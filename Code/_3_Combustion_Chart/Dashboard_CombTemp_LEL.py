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
    f_path = os.path.join(directory, "CR6_TablePLCRTO16Stats - Copy.txt")
    # Call function to parse data in text file. Returns data in list format
    comb_dates, comb_max = TablePLCRTO16Stats(f_path)

    f_path = os.path.join(directory, "CR6_TablePLC_RTOFP - Copy.txt")
    LEL_dates, LEL_132, LEL_300 = TablePLC_RTOFP(f_path)

    f_path = os.path.join(directory, "CR6_TablePLC_RTO32 - Copy.txt")
    CycleDates, CycleTime = TablePLC_RTO32(f_path)


    LEL_132_max, LEL_132_min = get_LEL132_min_max(LEL_132)
    LEL_300_max, LEL_300_min = get_LEL300_min_max(LEL_300)

    if LEL_132_max >= LEL_300_max:
        pct_LEL_max = LEL_132_max
    else:
        pct_LEL_max = LEL_300_max

    if LEL_132_min <= LEL_300_min:
        pct_LEL_min = LEL_132_min
    else:
        pct_LEL_min = LEL_300_min


# Plot line declarations
    # Combustion Temperature max data plot
    trace1 = go.Scatter(
        x=comb_dates,
        y=comb_max,
        name='Comb Temp',
        )
    # LEL 132 max data plot
    trace2 = go.Scatter(
        x=LEL_dates,
        y=LEL_132,
        name='LEL 132 Max',
        yaxis='y2',
        )
    # LEL 300 max data plot
    trace3 = go.Scatter(
        x=LEL_dates,
        y=LEL_300,
        name='LEL 300 Max',
        yaxis='y2'
        )
    # Cycle time data plot
    trace4 = go.Scatter(
        x=CycleDates,
        y=CycleTime,
        name='Cycle Time',
        yaxis='y3'
        )

# State which lines to plot from traces declared above.
    data = [trace1, trace2, trace3, trace4]

# Layout options for chart formatting
    layout = go.Layout(
        title='Combustion Temperature, Cycle Time and LEL Data For Last Seven Days',
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
            title='Combustion Temperature (Deg. F)',
            range=[1600, 1700],
            showline=True,
            ticks='outside',
            ticklen=4,
            tickwidth=2,
            tickcolor='#1f77b4',
            titlefont=dict(
                family='Arial Black',
                color='#1f77b4'
            ),
        ),
        yaxis2=dict(
            title='LEL (%)',
            range=[0, 25],
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False,
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
        yaxis3=dict(
            title='Combustion Chamber Cycle Time (min)',
            range=[0, 25],
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
            tickcolor='#d62728',
            titlefont=dict(
                family='Arial Black',
                color='#d62728'
            ),
        ),
        legend=dict(
            x=0.275,
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
        ),
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

    img_name = '{} CombTemp LEL Cycle'.format(today)

    dload_path = os.path.join(dload, "{}.png".format(img_name))

    if os.path.exists(dload_path) == True:
        os.remove(dload_path)

    offline.plot(fig, filename='{}\_Dashboard_Reports\Report_Output\HTML\{}\{} CombTemp_LEL_Cycle.html'.format(directory, today, today), auto_open=True,
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


def get_LEL132_min_max(LEL_132):
    LEL_132_max = int(float(max(LEL_132))) + 5
    LEL_132_min = int(float(min(LEL_132))) - 5

    return LEL_132_max, LEL_132_min


def get_LEL300_min_max(LEL_300):
    LEL_300_max = int(float(max(LEL_300))) + 5
    LEL_300_min = int(float(min(LEL_300))) - 5

    return LEL_300_max, LEL_300_min


# Function to parse TablePLCRTO16Stats file
def TablePLCRTO16Stats(f_path):
    # Intermediate list that stores ALL data. Data is parsed from this list into the proceeding lists
    parameters = []
    temp_list=[]
    comb_dates = []
    comb_max = []

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
    for xdate in parameters:
        # Column 0 = dates/times
        comb_dates.append(xdate[0].replace('"', ''))
    for xmax in parameters:
        # Column 46 = max combustion temp
        comb_max.append(xmax[46])

    # Remove first 4 items in list because not needed
    for n in range(0, 4):
        comb_dates.pop(0)
        comb_max.pop(0)

    # Return lists (date column and combustion temp column)
    return comb_dates, comb_max



# Function to parse TablePLC_RTOFP file
def TablePLC_RTOFP(f_path):
    # Intermediate list that stores ALL data. Data is parsed from this list into the proceeding lists
    parameters = []
    LEL_dates = []
    LEL_132 = []
    LEL_300 = []

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
    for xdate in parameters:
        # Column 0 = date/time
        LEL_dates.append(xdate[0].replace('"', ''))
    for max132 in parameters:
        # Column 22 = maximum LEL 132 data
        LEL_132.append(max132[22])
    for max300 in parameters:
        # Column 19 = maximum LEL 300 data
        LEL_300.append(max300[19])

    # Remove first 4 items in list because not needed
    for n in range(0, 4):
        LEL_dates.pop(0)
        LEL_132.pop(0)
        LEL_300.pop(0)

    # Return lists (date column, LEL 132 max, LEL 300 max)
    return LEL_dates, LEL_132, LEL_300



def TablePLC_RTO32(f_path):
    parameters = []
    CycleDates = []
    CycleTime = []

    with open(f_path) as f:
        data = f.readlines()
    last5days = data[-700:]

    for i in last5days:
        parameters.append([x.strip() for x in i.split(',')])

    for cdate in parameters:
        CycleDates.append(cdate[0].replace('"', ''))
    for ctime in parameters:
        CycleTime.append(ctime[52])

    for n in range(0,4):
        CycleTime.pop(0)
        CycleDates.pop(0)

    return CycleDates, CycleTime


if __name__ == "__main__":
    main()
