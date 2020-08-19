#!/usr/bin/python

# https://plot.ly/~empet/14689/table-with-cells-colored-according-to-th/#/

import datetime, sys, os

exe_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(exe_path)
grandparent_dir = os.path.dirname(parent_dir)
directory = os.path.dirname(grandparent_dir)
#\Dashboard_Reporting

#def main():


def get_condensate_rate(condensate_avg_dict): #{date str: [gal]}

    key_list = condensate_avg_dict.keys()
    for key in key_list:
        key.replace("'", '')

    key_list = sorted(key_list, key=lambda x: datetime.datetime.strptime(x, '%m-%d-%Y'))
    
#### Testing condensate tank emptying
##    last_key1 = key_list[-1]
##    last_key2 = key_list[-2]
##    last_key3 = key_list[-3]
##    condensate_avg_dict[last_key1][0] = int(1000)
##    condensate_avg_dict[last_key2][0] = int(1000)
##    condensate_avg_dict[last_key3][0] = int(1500)
#####
    
    first_index = 0
    second_index = 1
    start_rate_date = key_list[0]
    for key in key_list:
        key1 = key_list[first_index]
        key2 = key_list[second_index]
        
        if (float(condensate_avg_dict[key2][0]) - float(condensate_avg_dict[key1][0])) <= float(-25):
            start_rate_date = key2  

        if second_index == len(key_list) - 1:
            break
        else:
            first_index += 1
            second_index += 1
    

    if start_rate_date == key_list[-1]:
        rate_str = 'Approximate days until full condensate tank: Condensate tank was recently emptied.'

    else:
        rate_date_range = key_list[key_list.index(start_rate_date):]
        start_date = rate_date_range[0]
        end_date = rate_date_range[-1]
        numDays = len(rate_date_range)
        condensate_rate = int(round((condensate_avg_dict[end_date][0] - condensate_avg_dict[start_date][0]) / numDays))
        if condensate_rate > float(0):
            daystoFull = (3500 - condensate_avg_dict[end_date][0]) / condensate_rate
            start_date = datetime.datetime.strptime(start_date, "%m-%d-%Y").strftime("%#m/%#d")
            end_date = datetime.datetime.strptime(end_date, "%m-%d-%Y").strftime("%#m/%#d")
            rate_str = 'Approximate days until full condensate tank (estimated <b>{} gal/day</b> between {} - {}): <b>{} days</b>'.format(condensate_rate, start_date, end_date, daystoFull)

        else:
            rate_str = 'Approximate days until full condensate tank: Condensate tank was recently emptied.'
            
    return rate_str

def get_condensate_avg(SVE_Data):
    parameters = []
    dates = []
    condensate_avg = []
    months = []
    days = []
    years = []

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

# Combustion total list
    for cond_avg in parameters:
        condensate_avg.append(cond_avg[55])

# Remove first few values in lists
    for n in range(0, 4):
        condensate_avg.pop(0)


# create list of lists to compare values
    data_sets = zip(dates, years, months, days, condensate_avg)

# Add quarter hour temperature lists to dictionary with date as key
    cond_dict = {}
    cond_max = []

# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]


    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:

                cond_max.append(float(value_set[4]))

                index += 1

            else:
                cond_dict.update({'{}-{}-{}'.format(_month, _day, _year): [cond_max]})

                cond_max = []

                cond_max.append(float(value_set[4]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                cond_max.append(float(value_set[4]))

                cond_dict.update({'{}-{}-{}'.format(_month, _day, _year): [cond_max]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()


    cond_keys = cond_dict.keys()
    cond_keys.sort()
    cond_lvl_avg = {}

    for key in cond_keys:

        _avg = int(round(sum(cond_dict[key][0]) / len(cond_dict[key][0])))
        cond_lvl_avg.update({key: [_avg]})

    return cond_lvl_avg



def get_DilAir_max(RTOFP_Data):
    parameters = []
    dates = []
    valve_position = []

    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in RTOFP_Data:
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

# Combustion total list
    for v_position in parameters:
        valve_position.append(v_position[9])

# Remove first few values in lists
    for n in range(0, 4):
        valve_position.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, valve_position)

# Add quarter hour temperature lists to dictionary with date as key
    valve_dict = {}
    valve_max = []


# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:

                valve_max.append(float(value_set[4]))

                index += 1

            else:
                valve_dict.update({'{}-{}-{}'.format(_month, _day, _year): [valve_max]})

                valve_max = []

                valve_max.append(float(value_set[4]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                valve_max.append(float(value_set[4]))

                valve_dict.update({'{}-{}-{}'.format(_month, _day, _year): [valve_max]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()


    valve_keys = valve_dict.keys()
    valve_keys.sort()
    DilAir_max = {}

    for key in valve_keys:
        _max = max([x for x in valve_dict[key][0]])

        if _max > float(0):
            DilAir_max.update({key: [_max]})
        else:
            DilAir_max.update({key: ['Closed']})

            
    return DilAir_max



def get_combust_min_max(Stats_Data):
    parameters = []
    dates = []
    comb_total = []
    xv401_open = []
    comb_temp = []
    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in Stats_Data:
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

# Combustion total list
    for comb_tot in parameters:
        comb_total.append(comb_tot[48])
# XV-401 Open Time list (seconds)
    for open_time in parameters:
        xv401_open.append(open_time[11])
# Remove first few values in lists
    for n in range(0, 4):
        comb_total.pop(0)
        xv401_open.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, comb_total, xv401_open)

# Store all quarter hour temperatures in list for each day
    comb_temp_per_day = []
# Add quarter hour temperature lists to dictionary with date as key
    comb_temp_dict = {}
# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

# Loop through
    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                if float(value_set[5]) > 0 and float(value_set[5]) <= 900:
                    temp = ((float(value_set[4])) / (float(value_set[5])))
                    comb_temp_per_day.append(temp)
                else:
                    temp = ((float(value_set[4])) / int(900))
                    comb_temp_per_day.append(temp)
                index += 1
            else:
                comb_temp_dict.update({'{}-{}-{}'.format(_month, _day, _year): comb_temp_per_day})
                comb_temp_per_day = []
                if float(value_set[5]) > 0:
                    temp = ((float(value_set[4])) / (float(value_set[5])))
                    comb_temp_per_day.append(temp)
                else:
                    temp = ((float(value_set[4])) / int(900))
                    comb_temp_per_day.append(temp)
                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]
                index += 1
        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                temp = value_set[4]
                comb_temp_per_day.append(temp)
                comb_temp_dict.update({'{}-{}-{}'.format(_month, _day, _year): comb_temp_per_day})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()

    comb_keys = comb_temp_dict.keys()
    comb_keys.sort()
    combustion_min_max = {}
# Combustion min/max dictionary {key: [min, max]}
    for key in comb_keys:
        try:
            _min = int(min([x for x in comb_temp_dict[key] if x != 0]))
        except:
            _min = 0
        try:
            _max = int(max([x for x in comb_temp_dict[key] if x != 0]))
        except:
            _max = 0
            
        combustion_min_max.update({key: [_min, _max]})
    return combustion_min_max



def get_comb_temp_ranges(Stats_Data):
    parameters = []

    dates = []
    xv401_open = []
    comb_LT1600 = []
    comb_1599_1625 = []
    comb_1624_1650 = []
    comb_GT1650 = []
    comb_GT1650_1 = []
    comb_GT1650_2 = []
    comb_GT1650_3 = []
    comb_GT1650_4 = []
    
    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in Stats_Data:
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

    for open_time in parameters:
        xv401_open.append(open_time[11])
    for LT1600 in parameters:
        comb_LT1600.append(LT1600[53])
    for _1599_1625 in parameters:
        comb_1599_1625.append(_1599_1625[54])
    for _1624_1650 in parameters:
        comb_1624_1650.append(_1624_1650[55])
    for GT1650 in parameters:
        comb_GT1650.append(GT1650[56])
    for GT1650 in parameters:
        comb_GT1650_1.append(GT1650[57])
    for GT1650 in parameters:
        comb_GT1650_2.append(GT1650[58])
    for GT1650 in parameters:
        comb_GT1650_3.append(GT1650[59])
    for GT1650 in parameters:
        comb_GT1650_4.append(GT1650[60])

    for n in range(0, 4):
        comb_LT1600.pop(0)
        comb_1599_1625.pop(0)
        comb_1624_1650.pop(0)
        comb_GT1650.pop(0)
        comb_GT1650_1.pop(0)
        comb_GT1650_2.pop(0)
        comb_GT1650_3.pop(0)
        comb_GT1650_4.pop(0)
        xv401_open.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days,
                    comb_LT1600, comb_1599_1625, comb_1624_1650, comb_GT1650, xv401_open, comb_GT1650_1, comb_GT1650_2, comb_GT1650_3, comb_GT1650_4)

# Store all quarter hour temperatures in list for each day

# Add quarter hour temperature lists to dictionary with date as key
    temp_range_dict = {}
    comb_LT1600 = []
    comb_1599_1625 = []
    comb_1624_1650 = []
    comb_GT1650 = []
    comb_GT1650_1 = []
    comb_GT1650_2 = []
    comb_GT1650_3 = []
    comb_GT1650_4 = []
    open_time = []

# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

# comb_LT1600, comb_1599_1625, comb_1624_1650, comb_GT1650

    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                if float(value_set[4]) > 0:
                    comb_LT1600.append(float(value_set[4]))
                if float(value_set[5]) > 0:
                    comb_1599_1625.append(float(value_set[5]))
                if float(value_set[6]) > 0:
                    comb_1624_1650.append(float(value_set[6]))
                if float(value_set[7]) > 0:
                    comb_GT1650.append(float(value_set[7]))
                if float(value_set[9]) > 0:
                    comb_GT1650_1.append(float(value_set[9]))
                if float(value_set[10]) > 0:
                    comb_GT1650_2.append(float(value_set[10]))
                if float(value_set[11]) > 0:
                    comb_GT1650_3.append(float(value_set[11]))
                if float(value_set[12]) > 0:
                    comb_GT1650_4.append(float(value_set[12]))

                open_time.append(float(value_set[8]))

                index += 1

            else:
                temp_range_dict.update({'{}-{}-{}'.format(_month, _day, _year): [comb_LT1600, comb_1599_1625, comb_1624_1650, comb_GT1650, open_time, comb_GT1650_1, comb_GT1650_2, comb_GT1650_3, comb_GT1650_4]})

                comb_LT1600 = []
                comb_1599_1625 = []
                comb_1624_1650 = []
                comb_GT1650 = []
                comb_GT1650_1 = []
                comb_GT1650_2 = []
                comb_GT1650_3 = []
                comb_GT1650_4 = []
                open_time = []

                if float(value_set[4]) > 0:
                    comb_LT1600.append(float(value_set[4]))
                if float(value_set[5]) > 0:
                    comb_1599_1625.append(float(value_set[5]))
                if float(value_set[6]) > 0:
                    comb_1624_1650.append(float(value_set[6]))
                if float(value_set[7]) > 0:
                    comb_GT1650.append(float(value_set[7]))
                if float(value_set[9]) > 0:
                    comb_GT1650_1.append(float(value_set[9]))
                if float(value_set[10]) > 0:
                    comb_GT1650_2.append(float(value_set[10]))
                if float(value_set[11]) > 0:
                    comb_GT1650_3.append(float(value_set[11]))
                if float(value_set[12]) > 0:
                    comb_GT1650_4.append(float(value_set[12]))
                open_time.append(float(value_set[8]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                comb_LT1600.append(float(value_set[4]))
                comb_1599_1625.append(float(value_set[5]))
                comb_1624_1650.append(float(value_set[6]))
                comb_GT1650.append(float(value_set[7]))
                comb_GT1650_1.append(float(value_set[9]))
                comb_GT1650_2.append(float(value_set[9]))
                comb_GT1650_3.append(float(value_set[9]))
                comb_GT1650_4.append(float(value_set[9]))
                open_time.append(float(value_set[8]))

                temp_range_dict.update({'{}-{}-{}'.format(_month, _day, _year): [comb_LT1600, comb_1599_1625, comb_1624_1650, comb_GT1650, open_time, comb_GT1650_1, comb_GT1650_2, comb_GT1650_3, comb_GT1650_4]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()

    temp_keys = temp_range_dict.keys()
    temp_keys.sort()
    temp_range_seconds = {}

# Combustion min/max dictionary {key: [comb_LT1600, comb_1599_1625, comb_1624_1650, comb_GT1650]}
    for key in temp_keys:
        if len(temp_range_dict[key][0]) == 0:
            comb_LT1600_sum = 0
        else:
            comb_LT1600_sum = float(sum([x for x in temp_range_dict[key][0]]))

        if len(temp_range_dict[key][1]) == 0:
            comb_1599_1625_sum = 0
        else:
            comb_1599_1625_sum = float(sum([x for x in temp_range_dict[key][1]]))

        if len(temp_range_dict[key][2]) == 0:
            comb_1624_1650_sum = 0
        else:
            comb_1624_1650_sum = float(sum([x for x in temp_range_dict[key][2]]))

        if len(temp_range_dict[key][3]) == 0 and len(temp_range_dict[key][5]) == 0 and len(temp_range_dict[key][6]) == 0 and len(temp_range_dict[key][7]) == 0:
            comb_GT1650_sum = 0
        else:
        # Display as # of seconds
            comb_GT1650_0_sum = float(sum([x for x in temp_range_dict[key][3]]))
            comb_GT1650_1_sum = float(sum([x for x in temp_range_dict[key][5]]))
            comb_GT1650_2_sum = float(sum([x for x in temp_range_dict[key][6]]))
            comb_GT1650_3_sum = float(sum([x for x in temp_range_dict[key][7]]))
            comb_GT1650_4_sum = float(sum([x for x in temp_range_dict[key][8]]))
            comb_GT1650_sum = int(comb_GT1650_0_sum + comb_GT1650_1_sum + comb_GT1650_2_sum + comb_GT1650_3_sum + comb_GT1650_4_sum)

        temp_range_seconds.update({key: [comb_LT1600_sum, comb_1599_1625_sum, comb_1624_1650_sum, comb_GT1650_sum]})

    return temp_range_seconds



def get_avg_SVE_flow(SVE_Data):
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
        SVE_field7.append(field7_cell[7])
    for field49_cell in parameters:
        SVE_field49.append(field49_cell[49])
    for field52_cell in parameters:
        SVE_field52.append(field52_cell[52])

    for n in range(0, 4):
        SVE_field7.pop(0)
        SVE_field49.pop(0)
        SVE_field52.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, SVE_field7, SVE_field49, SVE_field52)

# Store all quarter hour temperatures in list for each day

# Add quarter hour temperature lists to dictionary with date as key
    SVE_dict = {}
    SVE_field7 = []
    SVE_field49 = []
    SVE_field52 = []

# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:

                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))

                index += 1

            else:
                SVE_dict.update({'{}-{}-{}'.format(_month, _day, _year): [SVE_field7, SVE_field49, SVE_field52]})

                SVE_field7 = []
                SVE_field49 = []
                SVE_field52 = []

                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]

                index += 1

        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                SVE_field7.append(float(value_set[4]))
                SVE_field49.append(float(value_set[5]))
                SVE_field52.append(float(value_set[6]))

                SVE_dict.update({'{}-{}-{}'.format(_month, _day, _year): [SVE_field7, SVE_field49, SVE_field52]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()

    SVE_keys = SVE_dict.keys()
    SVE_keys.sort()
    SVE_avg_per_day = {}

    for key in SVE_dict:
        SVE_field7_vals = SVE_dict[key][0]
        SVE_field49_vals = SVE_dict[key][1]
        SVE_field52_vals = SVE_dict[key][2]
        total_list = []
        i = 0


        for value in range(len(SVE_field7_vals)):
            if i < (len(SVE_field7_vals) - 1):
                total = float(SVE_field7_vals[i] + SVE_field49_vals[i] + SVE_field52_vals[i])
                if total <= 1:
                    #total_list.append(None)
                    pass
                else:
                    total_list.append(total)
                i += 1

            else:
                total = float(SVE_field7_vals[-1] + SVE_field49[-1] + SVE_field52[-1])
                if total <= 1:
                    pass
                else:
                    total_list.append(total)

                try:
                    SVE_avg = int(sum(total_list) / len(total_list))
                except:
                    SVE_avg = 0

                SVE_avg_per_day.update({key: [SVE_avg]})

                i = 0

    return SVE_avg_per_day




def get_blower_min_max(Stats_Data, SVE_Data):
    stats_parameters = []
    sve_parameters = []

    dates = []
    blower_min = []
    blower_max = []
    XV401_open_time = []

    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in SVE_Data:
        sve_parameters.append([x.strip() for x in i.split(',')])
    for i in Stats_Data:
        stats_parameters.append([x.strip() for x in i.split(',')])

# Date list
    for date in sve_parameters:
        dates.append(date[0].replace('"', ''))
    for n in range(0, 4):
        dates.pop(0)
    dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

# Month, day, and year lists
    for date in dates:
        months.append(date.strftime("%m"))
        days.append(date.strftime("%d"))
        years.append(date.strftime("%Y"))

# Combustion total list
    for _min in sve_parameters:
        # Blower 1 min
        #blower_min.append(_min[35])
        # Blower 2 min
        blower_min.append(_min[41])
# XV-401 Open Time list (seconds)
    for _max in sve_parameters:
        # Blower 1 max
        #blower_max.append(_max[36])
        # Blower 2 max
        blower_max.append(_max[42])
# Remove first few values in lists
    for xv401_time in stats_parameters:
        XV401_open_time.append(xv401_time[11])

    for n in range(0, 4):
        blower_min.pop(0)
        blower_max.pop(0)
        XV401_open_time.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, blower_min, blower_max, XV401_open_time)

# Store all quarter hour temperatures in list for each day
    blower_min_per_day = []
    blower_max_per_day = []
    xv401_open_per_day = []

# Add quarter hour temperature lists to dictionary with date as key
    blower_dict = {}
# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

# Loop through
    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:

                blower_max_per_day.append(float(value_set[5]))
                if float(value_set[6]) > 0:
                    _min = ((float(value_set[4])))
                    blower_min_per_day.append(_min)
                index += 1

            else:
                blower_dict.update({'{}-{}-{}'.format(_month, _day, _year): [blower_min_per_day, blower_max_per_day]})
                blower_min_per_day = []
                blower_max_per_day = []

                blower_max_per_day.append(float(value_set[5]))
                if float(value_set[6]) > 0:
                    _min = ((float(value_set[4])))
                    blower_min_per_day.append(_min)
                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]
                index += 1
        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                _min = value_set[4]
                _max = value_set[5]
                blower_min_per_day.append(_min)
                blower_max_per_day.append(_max)
                blower_dict.update({'{}-{}-{}'.format(_month, _day, _year): [blower_min_per_day, blower_max_per_day]})
            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()


    key_list = blower_dict.keys()
    key_list.sort()
    blower_min_max = {}

# Combustion min/max dictionary {key: [min, max]}
    for key in key_list:
        if key == "04-20-2019" or key == "04-21-2019":
            _min = 0
            _max = 0
        else:
            try:
                _min = int(min([x for x in blower_dict[key][0] if x != 0]))
            except:
                _min = 0
            try:
                _max = int(max([x for x in blower_dict[key][1] if x != 0]))
            except:
                _max = 0

        blower_min_max.update({key: [_min, _max]})


    return blower_min_max




def get_burner_on_time(Stats_Data):
    parameters = []
    dates = []
    
    burner_on = []
    xv401_open = []

    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in Stats_Data:
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

# Combustion total list
    for on_time in parameters:
        burner_on.append(on_time[2])
# XV-401 Open Time list (seconds)
    for open_time in parameters:
        xv401_open.append(open_time[11])
# Remove first few values in lists
    for n in range(0, 4):
        burner_on.pop(0)
        xv401_open.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, burner_on, xv401_open)

# Store all quarter hour temperatures in list for each day
    burner_on_per_day = []
    xv401_open_per_day = []
# Add quarter hour temperature lists to dictionary with date as key
    burner_dict = {}
# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

# Loop through
    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                xv401_open_per_day.append(int(value_set[5]))
                if float(value_set[4]) > float(value_set[5]):
                    burner_on_per_day.append(int(value_set[5]))
                else:
                    burner_on_per_day.append(int(value_set[4]))
                index += 1

            else:
                burner_dict.update({'{}-{}-{}'.format(_month, _day, _year): [burner_on_per_day, xv401_open_per_day]})
                burner_on_per_day = []
                xv401_open_per_day = []
                
                xv401_open_per_day.append(int(value_set[5]))
                if float(value_set[4]) > float(value_set[5]):
                    burner_on_per_day.append(int(value_set[5]))
                else:
                    burner_on_per_day.append(int(value_set[4]))
                    
                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]
                index += 1
        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                xv401_open_per_day.append(int(value_set[5]))
                if float(value_set[4]) > float(value_set[5]):
                    burner_on_per_day.append(int(value_set[5]))
                else:
                    burner_on_per_day.append(int(value_set[4]))
                    
                burner_dict.update({'{}-{}-{}'.format(_month, _day, _year): [burner_on_per_day, xv401_open_per_day]})

            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()


    keys = burner_dict.keys()
    keys.sort()
    burner_on_time = {}

# Combustion min/max dictionary {key: [min, max]}
    for key in keys:
        burner_on_sum = int(sum(burner_dict[key][0]))
        valve_open_sum = int(sum(burner_dict[key][1]))
        
        burner_pct = float(valve_open_sum) / float(86400) # 86400 seconds in a day
        burner_pct = burner_pct * float(100)

        if burner_pct == float(100):
            burner_pct = int(burner_pct)
        else:
            burner_pct = int(round(burner_pct))
            
        burner_on_time.update({key: burner_pct})

        
    return burner_on_time



def get_LEL_min_max(RTOFP_Data):
    parameters = []
    dates = []
    LEL132_max = []
    LEL300_max = []
    months = []
    days = []
    years = []

# Delineate data list by comma (',')
    for i in RTOFP_Data:
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

# Combustion total list
    for LEL132_value in parameters:
        LEL132_max.append(LEL132_value[21])
# XV-401 Open Time list (seconds)
    for LEL300_value in parameters:
        LEL300_max.append(LEL300_value[18])
# Remove first few values in lists
    for n in range(0, 4):
        LEL132_max.pop(0)
        LEL300_max.pop(0)

# create list of lists to compare values
    data_sets = zip(dates, years, months, days, LEL132_max, LEL300_max)

# Store all quarter hour temperatures in list for each day
    LEL132_per_day = []
    LEL300_per_day = []
# Add quarter hour temperature lists to dictionary with date as key
    LEL_dict = {}
# Keep track of how many lines/datasets have been iterated
    index = 0

    _day = data_sets[index][3]
    _month = data_sets[index][2]
    _year = data_sets[index][1]

# Loop through
    for value_set in data_sets:
        if index < len(data_sets):
            if value_set[1] == _year and value_set[2] == _month and value_set[3] == _day:
                if float(value_set[4]) > 0 and float(value_set[4]) < 90:
                    LEL132_per_day.append(float(value_set[4]))
                if float(value_set[5]) > 0 and float(value_set[5]) < 100:
                    LEL300_per_day.append(float(value_set[5]))

                index += 1

            else:
                LEL_dict.update({'{}-{}-{}'.format(_month, _day, _year): [LEL132_per_day, LEL300_per_day]})
                LEL132_per_day = []
                LEL300_per_day = []
                if float(value_set[4]) > 0 and float(value_set[4]) < 90:
                    LEL132_per_day.append(float(value_set[4]))
                if float(value_set[5]) > 0 and float(value_set[5]) < 100:
                    LEL300_per_day.append(float(value_set[5]))

                _day = data_sets[index][3]
                _month = data_sets[index][2]
                _year = data_sets[index][1]
                index += 1
        else:
            if data_sets[-1][3] == data_sets[-2][3] and data_sets[-1][2] == data_sets[-2][2] and data_sets[-1][1] == data_sets[-2][1]:
                if float(value_set[4]) > 0 and float(value_set[4]) < 90:
                    LEL132_per_day.append(float(value_set[4]))
                if float(value_set[5]) > 0 and float(value_set[5]) < 100:
                    LEL300_per_day.append(float(value_set[5]))
                LEL_dict.update({'{}-{}-{}'.format(_month, _day, _year): [LEL132_per_day, LEL300_per_day]})

            else:
                print 'Who downloads datalogger data this early...?'
                sys.exit()


    keys = LEL_dict.keys()
    keys.sort()
    LEL_min_max = {}

# Combustion min/max dictionary {key: [min, max]}
    for key in keys:
        try:
            LEL132_min = '%.1f' % float(min([x for x in LEL_dict[key][0]]))# if x != 0]))
        except:
            LEL132_min = 0.0
        try:
            LEL132_max = '%.1f' % float(max([x for x in LEL_dict[key][0]]))# if x != 0]))
        except:
            LEL132_max = 0.0
        try:
            LEL300_min = '%.1f' % float(min([x for x in LEL_dict[key][1]]))# if x != 0]))
        except:
            LEL300_min = 0.0
        try:
            LEL300_max = '%.1f' % float(max([x for x in LEL_dict[key][1]]))# if x != 0]))
        except:
            LEL300_max = 0.0

        LEL_min_max.update({key: [LEL132_min, LEL132_max, LEL300_min, LEL300_max]})

    return LEL_min_max



##if __name__ == "__main__":
##    main()
