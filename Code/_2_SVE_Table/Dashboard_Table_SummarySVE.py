#!/usr/bin/python

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
        #print date
        if date.month == _30_days_ago.month and date.day == _30_days_ago.day:
            count += 1
            line_count = count
        else:
            count += 1

    f_path = os.path.join(directory, "CR6_TablePLC_SVE - Copy.txt")
    with open(f_path) as f:
        SVE_Data = f.readlines()
    SVE_Data = SVE_Data[-line_count:]
    SVE_flow_range_dict = get_max_SVE_flow(SVE_Data)

###
    f_path = os.path.join(directory, "CR6_TableCommStats - Copy.txt")
    with open(f_path) as f:
        Comm_Data = f.readlines()
    Comm_Data = Comm_Data[-line_count:]
    pulse_counter_dict = getBGMSpulse(Comm_Data) #[pCounter6, pVolume6, pCount7, pVolume7]
###

    create_table(SVE_flow_range_dict, pulse_counter_dict)



def create_table(SVE_flow_range_dict, pulse_counter_dict):

    key_list = SVE_flow_range_dict.keys()
    for key in key_list:
        key.replace("'", '')
    key_list = sorted(key_list, key=lambda x: datetime.datetime.strptime(x, '%m-%d-%Y'))

    pulse_keys = pulse_counter_dict.keys()
    for key in pulse_keys:
        key.replace("'", '')
    pulse_keys = sorted(pulse_keys, key=lambda x: datetime.datetime.strptime(x, '%m-%d-%Y'))


    _1 = [key for key in key_list]
    _2 = [SVE_flow_range_dict[key][0] for key in key_list]
    _3 = [SVE_flow_range_dict[key][1] for key in key_list]
    _4 = [SVE_flow_range_dict[key][2] for key in key_list]
    _5 = [SVE_flow_range_dict[key][3] for key in key_list]
    _6 = [SVE_flow_range_dict[key][4] for key in key_list]
    _7 = [SVE_flow_range_dict[key][5] for key in key_list]
    _8 = [SVE_flow_range_dict[key][6] for key in key_list]
    
    _9 = ["--" if key not in pulse_keys else round(pulse_counter_dict[key][0], 2) for key in key_list]
    _10 = ["--" if key not in pulse_keys else round(pulse_counter_dict[key][1], 2) for key in key_list]
    _11 = ["--" if key not in pulse_keys else round(pulse_counter_dict[key][2], 2) for key in key_list]
    _12 = ["--" if key not in pulse_keys else round(pulse_counter_dict[key][3], 2) for key in key_list]


    table = go.Table(
        columnorder=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        columnwidth=[90, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60],

        header=dict(
            values=['<b><br><br><br>Date</b>',
                    "<b>    Flow<br>  < 400<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br>  >= 400<br>  < 450<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br>  >= 450<br>  < 475<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br>  >= 475<br>  <= 525<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br>  > 525<br>  <= 550<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br>  > 550<br>  <= 600<br>    scfm<br>  (QH's)</b>",
                    "<b>    Flow<br> > 600<br>    scfm<br>  (QH's)</b>",
                    "<b>  BGMS 6SD<br>      Pulse<br>     Count</b>",
                    "<b>  BGMS 6SD<br>      Pulse<br>    Volume<br>      (Gal)</b>",
                    "<b>  BGMS 7SD<br>      Pulse<br>     Count</b>",
                    "<b>  BGMS 7SD<br>      Pulse<br>    Volume<br>      (Gal)</b>"],


            align = 'center',
            line = dict(color='rgb(50, 50, 50)'),
            fill = dict(color='rgb(111, 155, 186)'),
            font = dict(
                color='rgb(50, 50, 50)',
                family="Segoe UI",
                size=14
                )
        ),

       # red 211, 93, 93
       # yellow 248, 222, 126
       # green 55, 255, 55
       # white 245,245,245

        cells=dict(
            values=[_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12],
            align = 'center',
            line = dict(color='rgb(50, 50, 50)'),

            fill = dict(color=[
                            #1
                               'rgb(200,200,200)',
                            #2
                               ['rgb(248, 222, 126)' if float(val) > 1 and float(val) < 92 else
                                'rgb(255, 153, 153)' if float(val) >= 92 else 'rgb(245,245,245)' for val in _2],
                            #3
                               'rgb(245,245,245)',
                            #4
                               'rgb(245,245,245)',
                            #5
                               ['rgb(55, 255, 55)' if float(val) == 96 else 'rgb(255, 153, 153)' if float(val) == 0 else
                                'rgb(245,245,245)' for val in _5],
                            #6
                               'rgb(245,245,245)',
                            #7
                               'rgb(245,245,245)',
                            #8
                               ['rgb(248, 222, 126)' if float(val) > 1 and float(val) < 92 else
                                'rgb(255, 153, 153)' if float(val) >= 92 else 'rgb(245,245,245)' for val in _8],
                            #9
                                'rgb(245,245,245)',
                            #10
                                'rgb(245,245,245)',
                            #11
                                'rgb(245,245,245)',
                            #12
                               'rgb(245,245,245)',
                               ]
                        )
                ),
        )

    layout=dict(
        title='<b>SVE Flow Rate Daily Summary</b>',
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

    img_name = '{} SVE Flow Daily Summary'.format(today)

    dload_path = os.path.join(dload, "{}.png".format(img_name))

    if os.path.exists(dload_path) == True:
        os.remove(dload_path)

    offline.plot(fig, filename='{}\_Dashboard_Reports\Report_Output\HTML\{}\{} Table_SummarySVE.html'.format(directory, today, today), auto_open=True,
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





def getBGMSpulse(Comm_Data):
    parameters = []
    dates = []
    pCount6 = []
    pVolume6 = []
    pCount7 = []
    pVolume7 = []

    months = []
    days = []
    years = []
    
# if date < 10/11/2019 add "--" to chart
    for i in Comm_Data:
        parameters.append([x.strip() for x in i.split(',')])

    for i in parameters[0:4]:
        if ("TOA5" in parameters[0][0]) or ("TIMESTAMP" in parameters[0][0]) or ("TS" in parameters[0][0]) or ("Tot" in parameters[0][2]):
            parameters.pop(0)

# Date list
    for date in parameters:
        dates.append(date[0].replace('"', ''))
    for n in range(0, 4):
        dates.pop(0)
    dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

# Month, day, and year lists
    for date in dates:
        months.append(date.strftime("%m"))
        days.append(date.strftime("%d"))
        years.append(date.strftime("%Y"))

    for field3 in parameters:
        pCount6.append(field3[3]) # pCounter_6SD_Max = number of pulses in QH
    for field5 in parameters: 
        pVolume6.append(field5[5]) # pVolume_6SD_Tot = purge volume in QH

    for field6 in parameters:
        pCount7.append(field6[6]) # pCounter_7SD_Max = number of pulses in QH
    for field8 in parameters: 
        pVolume7.append(field8[8]) # pVolume_7SD_Tot = purge volume in QH

    data_sets = zip(dates, years, months, days, pCount6, pVolume6, pCount7, pVolume7)

    pulseDict = {}
    date_list = []
    pCount6 = []
    pVolume6 = []
    pCount7 = []
    pVolume7 = []

    index = 0
    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]


    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                date_list.append(value_set[0])
                pCount6.append(int(value_set[4]))
                pVolume6.append(float(value_set[5]))
                pCount7.append(int(value_set[6]))
                pVolume7.append(float(value_set[7]))
                index += 1
            else:
                pulseDict.update({'{}-{}-{}'.format(_month, _day, _year): [pCount6, pVolume6, pCount7, pVolume7, date_list]})
                date_list = []
                pCount6 = []
                pVolume6 = []
                pCount7 = []
                pVolume7 = []

                date_list.append(value_set[0])
                pCount6.append(int(value_set[4]))
                pVolume6.append(float(value_set[5]))
                pCount7.append(int(value_set[6]))
                pVolume7.append(float(value_set[7]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                date_list.append(value_set[0])
                pCount6.append(int(value_set[4]))
                pVolume6.append(float(value_set[5]))
                pCount7.append(int(value_set[6]))
                pVolume7.append(float(value_set[7]))

                pulseDict.update({'{}-{}-{}'.format(_month, _day, _year): [pCount6, pVolume6, pCount7, pVolume7, date_list]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()

    pulse_keys = pulseDict.keys()
    pulse_keys.sort()
    volumeDict = {}

    for key in pulse_keys:
        pVolume6 = pulseDict[key][1]
        pVolume7 = pulseDict[key][3]

        pCount6 = sum(pVolume6) / 0.08
        pCount7 = sum(pVolume7) / 0.08

        volumeDict.update({key: [pCount6, sum(pVolume6), pCount7, sum(pVolume7)]})

    return volumeDict


def get_max_SVE_flow(SVE_Data):
    parameters = []

    dates = []
    # Field = Field + 1 if looking in excel
    SVE_field7 = []
    SVE_field49 = []
    SVE_field52 = []

    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in SVE_Data:
        parameters.append([x.strip() for x in i.split(',')])
# Date list
    for date in parameters:
        dates.append(date[0].replace('"', ''))
    for n in range(0, 4):
        dates.pop(0)
    dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

# Month, day, and year lists
    for date in dates:
        months.append(date.strftime("%m"))
        days.append(date.strftime("%d"))
        years.append(date.strftime("%Y"))

    for field7_cell in parameters:
        SVE_field7.append(field7_cell[6])
    for field49_cell in parameters:
        SVE_field49.append(field49_cell[48])
    for field52_cell in parameters:
        SVE_field52.append(field52_cell[51])

    for n in range(0, 4):
        SVE_field7.pop(0)
        SVE_field49.pop(0)
        SVE_field52.pop(0)

    data_sets = zip(dates, years, months, days, SVE_field7, SVE_field49, SVE_field52)

    SVE_dict = {}
    date_list = []
    SVE_field7 = []
    SVE_field49 = []
    SVE_field52 = []

    index = 0
    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                date_list.append(value_set[0])
                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))
                index += 1

            else:
                SVE_dict.update({'{}-{}-{}'.format(_month, _day, _year): [SVE_field7, SVE_field49, SVE_field52, date_list]})
                date_list = []
                SVE_field7 = []
                SVE_field49 = []
                SVE_field52 = []

                date_list.append(value_set[0])
                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                date_list.append(value_set[0])
                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))

                SVE_dict.update({'{}-{}-{}'.format(_month, _day, _year): [SVE_field7, SVE_field49, SVE_field52, date_list]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()

    SVE_keys = SVE_dict.keys()
    SVE_keys.sort()
    SVE_flow_range = {}

    for key in SVE_dict:
        SVE_field7_vals = SVE_dict[key][0]
        SVE_field49_vals = SVE_dict[key][1]
        SVE_field52_vals = SVE_dict[key][2]
        _LT400 = []
        _400_449 = []
        _450_474 = []
        _475_525 = []
        _526_550 = []
        _551_600 = []
        _GT600 = [] 

        i = 0
        for value in range(len(SVE_field7_vals)):
            if i <= (len(SVE_field7_vals)):# - 1):
                total = float(SVE_field7_vals[i] + SVE_field49_vals[i] + SVE_field52_vals[i])

                if total < 400:
                    _LT400.append(1)
                elif total >= 400 and total < 450:
                    _400_449.append(1)
                elif total >= 450 and total < 475:
                    _450_474.append(1)
                elif total >= 475 and total <= 525:
                    _475_525.append(1)
                elif total > 525 and total <= 550:
                    _526_550.append(1)
                elif total > 550 and total <= 600:
                    _551_600.append(1)
                else:
                    _GT600.append(1)


                if len(_LT400) > 0:
                    _LT400_qh = sum(_LT400)
                else:
                    _LT400_qh = 0
                if len(_400_449) > 0:
                    _400_449_qh = sum(_400_449)
                else:
                    _400_449_qh = 0
                if len(_450_474) > 0:
                    _450_474_qh = sum(_450_474)
                else:
                    _450_474_qh = 0
                if len(_475_525) > 0:
                    _475_525_qh = sum(_475_525)
                else:
                    _475_525_qh = 0
                if len(_526_550) > 0:
                    _526_550_qh = sum(_526_550)
                else:
                    _526_550_qh = 0
                if len(_551_600) > 0:
                    _551_600_qh = sum(_551_600)
                else:
                    _551_600_qh = 0
                if len(_GT600) > 0:
                    _GT600_qh = sum(_GT600)
                else:
                    _GT600_qh = 0

                SVE_flow_range.update({key: [_LT400_qh,
                                             _400_449_qh,
                                             _450_474_qh,
                                             _475_525_qh,
                                             _526_550_qh,
                                             _551_600_qh,
                                             _GT600_qh]})

                i += 1

    return SVE_flow_range


if __name__ == "__main__":
    main()
