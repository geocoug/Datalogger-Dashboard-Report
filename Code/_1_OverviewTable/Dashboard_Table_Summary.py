#!/usr/bin/python

# https://plot.ly/~empet/14689/table-with-cells-colored-according-to-th/#/

import plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
import datetime, sys, os
from shutil import copyfile

exe_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(exe_path)
grandparent_dir = os.path.dirname(parent_dir)
directory = os.path.dirname(grandparent_dir)
#\Dashboard_Reporting

def main():
    f_path = os.path.join(directory, "CR6_TablePLC_SVE - Copy.txt")
    with open(f_path) as f:
        data = f.readlines()
    data = data[-3500:]

    parameters = []
    dates = []
    for i in data:
        parameters.append([x.strip() for x in i.split(',')])

    date = parameters[-1][0]
    date = date.replace('"', '')
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date = date.strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    yesterday = date - datetime.timedelta(days=1)

    _30_days_ago = yesterday - datetime.timedelta(days=30)
    
    dates_list = []
    index = 0
    for i in parameters:
        date = parameters[index][0]
        date = date.replace('"', '')
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        dates_list.append(date)
        index += 1

    count = 0
    for date in reversed(dates_list):
        if date.month == _30_days_ago.month and date.day == _30_days_ago.day:
            count += 1
            line_count = count
        else:
            count += 1

    
    f_path = os.path.join(directory, "CR6_TablePLCRTO16Stats - Copy.txt")
    with open(f_path) as f:
        Stats_Data = f.readlines()
    Stats_Data = Stats_Data[-line_count:]

    f_path = os.path.join(directory, "CR6_TablePLC_SVE - Copy.txt")
    with open(f_path) as f:
        SVE_Data = f.readlines()
    SVE_Data = SVE_Data[-line_count:]

    f_path = os.path.join(directory, "CR6_TablePLC_RTOFP - Copy.txt")
    with open(f_path) as f:
        RTOFP_Data = f.readlines()
    RTOFP_Data = RTOFP_Data[-line_count:]


    import Dashboard_Table_Data as d
    comb_min_max = d.get_combust_min_max(Stats_Data)
    comb_temp_ranges_in_seconds = d.get_comb_temp_ranges(Stats_Data)
    avg_SVE_flow = d.get_avg_SVE_flow(SVE_Data)
    burner_on_time = d.get_burner_on_time(Stats_Data)
    blower_min_max = d.get_blower_min_max(Stats_Data, SVE_Data)
    LEL_min_max = d.get_LEL_min_max(RTOFP_Data)
    DilAir_max = d.get_DilAir_max(RTOFP_Data)
    cond_lvl_avg = d.get_condensate_avg(SVE_Data)
    condensate_rate = d.get_condensate_rate(cond_lvl_avg)


    create_table(comb_min_max, comb_temp_ranges_in_seconds, avg_SVE_flow,
                 burner_on_time, blower_min_max, LEL_min_max, DilAir_max,
                 cond_lvl_avg, condensate_rate)



def create_table(comb_min_max, comb_temp_ranges_in_seconds, avg_SVE_flow,
                 burner_on_time, blower_min_max, LEL_min_max, DilAir_max,
                 cond_lvl_avg, condensate_rate):
    
    key_list = comb_min_max.keys()
    for key in key_list:
        key.replace("'", '')
    key_list = sorted(key_list, key=lambda x: datetime.datetime.strptime(x, '%m-%d-%Y'))

    _1 = [key for key in key_list]
    _2 = [comb_min_max[key][0] for key in key_list]
    _3 = [comb_min_max[key][1] for key in key_list]
    _4 = [datetime.datetime.strptime(str(datetime.timedelta(seconds=comb_temp_ranges_in_seconds[key][0])), "%H:%M:%S").strftime("%H:%M") for key in key_list]
    _5 = [datetime.datetime.strptime(str(datetime.timedelta(seconds=comb_temp_ranges_in_seconds[key][1])), "%H:%M:%S").strftime("%H:%M") for key in key_list]
    _6 = [datetime.datetime.strptime(str(datetime.timedelta(seconds=comb_temp_ranges_in_seconds[key][2])), "%H:%M:%S").strftime("%H:%M") for key in key_list]

    _7 = []
    seconds_in_day = int((60 * 60) * 24)
    for key in key_list:
        if int(comb_temp_ranges_in_seconds[key][3]) >= seconds_in_day:
            _7.append("24:00")
        elif int(comb_temp_ranges_in_seconds[key][3]) < seconds_in_day:
            #print '< 1 day'
            _7.append(datetime.datetime.strptime(str(datetime.timedelta(seconds=comb_temp_ranges_in_seconds[key][3])), "%H:%M:%S").strftime("%H:%M"))
        else:
            print 'uuuhhhh'

    #_7 = [datetime.datetime.strptime(str(datetime.timedelta(seconds=comb_temp_ranges_in_seconds[key][3])), "%H:%M:%S").strftime("%H:%M") for key in key_list]
    _8 = [avg_SVE_flow[key][0] for key in key_list]
    _9 = [DilAir_max[key] for key in key_list]
    _10 = [burner_on_time[key] for key in key_list]
    _11 = [blower_min_max[key][0] for key in key_list]
    _12 = [blower_min_max[key][1] for key in key_list]
    _13 = [LEL_min_max[key][0] for key in key_list]
    _14 = [LEL_min_max[key][1] for key in key_list]
    _15 = [LEL_min_max[key][2] for key in key_list]
    _16 = [LEL_min_max[key][3] for key in key_list]
    _17 = [cond_lvl_avg[key][0] for key in key_list]
    
    zero_seconds = datetime.timedelta(seconds=0)

    table = go.Table(
        columnorder=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        columnwidth=[90, 60, 60, 70, 70, 70, 70, 60, 60, 60, 60, 60, 60, 60, 60, 60, 85],
 
        header=dict(
            values=['<b><br><br><br>Date</b>',
                    '<b>  Comb<br>  Temp<br>    Min<br> (Deg. F)</b>',
                    '<b>  Comb<br>  Temp<br>    Max<br> (Deg. F)</b>',
                    '<b>  Comb<br>  Temp<br>< 1600<br>  (H:M)</b>',
                    '<b>  Comb<br>  Temp<br>> 1599<br>< 1625<br>  (H:M)</b>',
                    '<b>  Comb<br>  Temp<br>> 1624<br><= 1650<br>  (H:M)</b>',
                    '<b>  Comb<br>  Temp<br>> 1650<br>  (H:M)</b>',
                    '<b> Average<br>     SVE<br>    Flow<br>   (scfm)</b>',
                    '<b> Dilution<br>     Air<br>   Valve<br>  (scfm)</b>',
                    '<b> XV-401<br>  Open<br>  Time<br>   ( % )</b>',
                    '<b> Blower 2<br> Temp<br> Min<br>(Deg. F)</b>',
                    '<b> Blower 2<br> Temp<br> Max<br>(Deg. F)</b>',
                    '<b><br><br>LEL 132<br>    Min<br>(% LEL)</b>',
                    '<b><br><br>LEL 132<br>    Max<br>(% LEL)</b>',
                    '<b><br><br>LEL 300<br>    Min<br>(% LEL)</b>',
                    '<b><br><br>LEL 300<br>    Max<br>(% LEL)</b>',
                    '<b><br><br> Condensate<br>      Level<br>       Avg<br>       (gal)</b>',
                    ],

            align = 'center',
            line = dict(color='rgb(50, 50, 50)'),
            fill = dict(color='rgb(111, 155, 186)'),
            font = dict(
                color='rgb(50, 50, 50)',
                family="Segoe UI",
                size=14
                )
        ),    
        
        cells=dict(
            values=[_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17],
            align = 'center',
            line = dict(color='rgb(50, 50, 50)'),

            fill = dict(color=[
                            #1
                                'rgb(200,200,200)',
                            #2
                               ['rgb(255, 153, 153)' if float(val) >= 1700 else
                                'rgb(248, 222, 126)' if float(val) <= 1625 and float(val) >= 1600 else
                                'rgb(255, 153, 153)' if float(val) < 1600 else 'rgb(245,245,245)' for val in _2],
                            #3
                               ['rgb(255, 153, 153)' if float(val) >= 1750 else
                                'rgb(248, 222, 126)' if float(val) <= 1625 and float(val) >= 1600 else
                                'rgb(255, 153, 153)' if float(val) < 1600 else 'rgb(245,245,245)' for val in _3],
                            #4
                               ['rgb(255, 153, 153)' if val != '00:00' else 'rgb(245,245,245)' for val in _4],
                            #5
                               'rgb(245,245,245)',
                            #6
                               'rgb(245,245,245)',
                            #7   
                               'rgb(245,245,245)',
                            #8   
                               ['rgb(255, 153, 153)' if float(val) < 450 else
                                'rgb(255, 153, 153)' if float(val) > 550 else 'rgb(245,245,245)' for val in _8],
                            #9
                               #['rgb(248, 222, 126)' if val != 'Closed' else 'rgb(245,245,245)' for val in _9],
                                'rgb(245,245,245)',
                            #10  
                               ['rgb(255, 153, 153)' if float(val) < 100 else 'rgb(245,245,245)' for val in _10],
                            #11   
                               ['rgb(245,245,245)' if float(val) > 0 else 'rgb(255, 153, 153)' for val in _11],
                            #12
                               ['rgb(245,245,245)' if float(val) > 0 else 'rgb(255, 153, 153)' for val in _12],
                            #13
                               ['rgb(248, 222, 126)' if float(val) > 10 and float(val) <= 15 else
                                'rgb(255, 153, 153)' if float(val) > 15 else
                                'rgb(255, 153, 153)' if float(val) == 0 else 'rgb(245,245,245)' for val in _13],
                            #14
                               ['rgb(248, 222, 126)' if float(val) > 10 and float(val) <= 15 else
                                'rgb(255, 153, 153)' if float(val) > 15 else
                                'rgb(255, 153, 153)' if float(val) == 0 else 'rgb(245,245,245)' for val in _14],
                            #15
                               ['rgb(248, 222, 126)' if float(val) > 10 and float(val) <= 15 else
                                'rgb(255, 153, 153)' if float(val) > 15 else
                                'rgb(255, 153, 153)' if float(val) == 0 else 'rgb(245,245,245)' for val in _15],
                            #16
                               ['rgb(248, 222, 126)' if float(val) > 10 and float(val) <= 15 else
                                'rgb(255, 153, 153)' if float(val) > 15 else
                                'rgb(255, 153, 153)' if float(val) == 0 else 'rgb(245,245,245)' for val in _16],
                            #17
                               ['rgb(248, 222, 126)' if float(val) > 2750 and float(val) <= 3000 else
                                'rgb(255, 153, 153)' if float(val) > 3000 else 'rgb(245,245,245)' for val in _17]
                                ]
                               
                        )            
                ),
        )

    layout=dict(
        title='<b>RTO/SVE System Daily Summary</b>',
        titlefont=dict(
            family='Arial Black',
            color='black'
        ),
        width=1250,
        height=900,
        autosize=False,
        margin = dict(
            t=75,
            b=25,
            l=50,
            r=50
            )
        )

    fig = dict(data=[table], layout=layout)
    cond_lvl = cond_lvl_avg[key_list[-1]]
    cond_lvl = float(cond_lvl[0])
    approx_days = int((3500 - cond_lvl) / 60)

    fig['layout'].update(
        annotations=[
            dict(
                text=condensate_rate,
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0.5,
                y=0.1,
                yshift=-50
                )
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
        
    img_name = '{} System Daily Summary'.format(today)

    dload_path = os.path.join(dload, "{}.png".format(img_name))

    if os.path.exists(dload_path) == True:
        os.remove(dload_path)
    
    offline.plot(fig, filename='{}\_Dashboard_Reports\Report_Output\HTML\{}\{} Table_Summary.html'.format(directory, today, today), auto_open=True,
                 image='png', image_filename=img_name, image_width=1250, image_height=900)

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


if __name__ == "__main__":
    main()
