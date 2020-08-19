import datetime, sys, os, shutil
from shutil import copyfile


def main():
    print '  ________________________________________________________________________ '
    print ' |                                                                        |'
    print ' | -Output formats include: "html", "png", and "pdf"                      |'
    print ' |                                                                        |'
    print ' | -The user will need to make multiple selections while executing.       |'
    print ' | -Do not close the program window when running.                         |'
    print ' |________________________________________________________________________|\n'
    print '\n'


    print 'IMPORTANT - PLEASE READ'
    print '******************************************************************************\n'
    print 'Make sure Thermocouple data is up to date here:'
    print '     \Loggernet\_Dashboard_Reports\Thermocouples\ALL_TC_DATA.xlsx'
    print ''
    print 'The following Thermocouples are not included:'
    remove_tc = ['TC1-7', 'TC2-16', 'TC2-36', 'TC3-37', 'TC4-19', 'TC4-30']
    print '  {}'.format(remove_tc)

    print '\n'

    while True:
        print '(Y) Continue'
        print '(N) Exit'
        user_continue = raw_input('Enter your selection: ')
        print '\n******************************************************************************\n'

        if user_continue.upper() == 'Y':
            file_management()

            while True:
                print 'Select one of the following:'
                print '  (1) Dashboard Report'
                print ''
                print '  (3) System Daily Summary *ONLY'
                print '  (4) SVE Flow Rate Summary *ONLY'
                print '  (5) Combustion Temp, LEL, Cycle Time chart *ONLY'
                print '  (6) SVE Flow, Fan Speed, PT-101 chart *ONLY'
                print '  (7) Thermocouples chart *ONLY'
                print '  (0) Exit \n'
                user_input = raw_input('Your selection: ')
                print '\n******************************************************************************\n'

                if user_input == '1':
                    print 'Generating table for "RTO/SVE System Daily Summary".\n'
                    sys.path.insert(0, '/_1_OverviewTable/')
                    from _1_OverviewTable import Dashboard_Table_Summary
                    Dashboard_Table_Summary.main()

                    print 'Generating table for "SVE Flow Rate Daily Summary".\n'
                    sys.path.insert(0, '/_2_SVE_Table/')
                    from _2_SVE_Table import Dashboard_Table_SummarySVE
                    Dashboard_Table_SummarySVE.main()
                    
                    print 'Generating chart for "Combustion Temperature, Cycle Time and LEL Data For Last Seven Days".\n'
                    sys.path.insert(0, '/_3_Combustion_Chart/')
                    from _3_Combustion_Chart import Dashboard_CombTemp_LEL
                    Dashboard_CombTemp_LEL.main()
                    
                    print 'Generating chart for "Flow, System Fan Speed and PT-101 For Last Seven Days".\n'
                    sys.path.insert(0, '/_4_Flow_Chart/')
                    from _4_Flow_Chart import Dashboard_Flow
                    Dashboard_Flow.main()
                    
                    print 'Generating chart for "Temperature by Depth for Thermocouple Locations For Last Seven Days".\n'
                    sys.path.insert(0, '/_5_Thermocouple_Chart/')
                    from _5_Thermocouple_Chart import Dashboard_TC_Subplots
                    Dashboard_TC_Subplots.main(remove_tc)
                    
                    print 'Creating Dashboard Report PDF.'
                    sys.path.insert(0, '/_6_Compile_Dashboard/')
                    from _6_Compile_Dashboard import Dashboard_CreatePDF
                    Dashboard_CreatePDF.main()
                    print '\n******************************************************************************\n'


                elif user_input == '3':
                    print 'Generating table for "RTO/SVE System Daily Summary".'
                    sys.path.insert(0, '/_1_OverviewTable/')
                    from _1_OverviewTable import Dashboard_Table_Summary
                    Dashboard_Table_Summary.main()
                    
                elif user_input == '4':
                    print 'Generating table for "SVE Flow Rate Daily Summary".'
                    sys.path.insert(0, '/_2_SVE_Table/')
                    from _2_SVE_Table import Dashboard_Table_SummarySVE
                    Dashboard_Table_SummarySVE.main()
                    
                elif user_input == '5':
                    print 'Generating chart for "Combustion Temperature, Cycle Time and LEL Data For Last Five Days".'
                    sys.path.insert(0, '/_3_Combustion_Chart/')
                    from _3_Combustion_Chart import Dashboard_CombTemp_LEL
                    Dashboard_CombTemp_LEL.main()

                elif user_input == '6':
                    print 'Generating chart for "Flow, System Fan Speed and PT-101 For Last Five Days".'
                    sys.path.insert(0, '/_4_Flow_Chart/')
                    from _4_Flow_Chart import Dashboard_Flow
                    Dashboard_Flow.main()

                elif user_input == '7':
                    print 'Generating chart for "Temperature by Depth for Thermocouple Locations".'
                    sys.path.insert(0, '/_5_Thermocouple_Chart/')
                    from _5_Thermocouple_Chart import Dashboard_TC_Subplots
                    Dashboard_TC_Subplots.main(remove_tc)

                elif user_input == '0':
                    file_management()

                else:
                    continue


            break

        elif user_continue.upper() == 'N':
            sys.exit()
        else:
            continue


def file_management():
    exe_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(exe_path)
    grandparent_dir = os.path.dirname(parent_dir)
    directory = os.path.dirname(grandparent_dir)
    backup_dir = os.path.join(directory, 'Daily Backups')

    while True:
        print '(1) Copy Loggernet files from C: to L:'
        print '(2) Create dashboard reports'
        print '(3) Create daily backup (when finished)'
        print '(0) Exit\n'
        user_input = raw_input('Your selection: ')
        print '\n******************************************************************************\n'


        if user_input == '1':
            if os.path.isfile(r"{}\CR6_TablePLC_RTOFP - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTOFP - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTOFP - Copy.txt".format(directory), directory + '\CR6_TablePLC_RTOFP.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_RTOFP.dat", r"{}\CR6_TablePLC_RTOFP.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTOFP.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTOFP.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_RTOFP.dat", r"{}\CR6_TablePLC_RTOFP.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTOFP.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTOFP.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TablePLC_RTO32 - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTO32 - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTO32 - Copy.txt".format(directory), directory + '\CR6_TablePLC_RTO32.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_RTO32.dat", r"{}\CR6_TablePLC_RTO32.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTO32.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTO32.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_RTO32.dat", r"{}\CR6_TablePLC_RTO32.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTO32.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_RTO32.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TablePLC_SVE - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_SVE - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TablePLC_SVE - Copy.txt".format(directory), directory + '\CR6_TablePLC_SVE.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_SVE.dat", r"{}\CR6_TablePLC_SVE.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_SVE.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_SVE.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLC_SVE.dat", r"{}\CR6_TablePLC_SVE.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLC_SVE.dat".format(directory))
                os.rename(r"{}\CR6_TablePLC_SVE.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TablePLCRTO16Stats - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TablePLCRTO16Stats - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TablePLCRTO16Stats - Copy.txt".format(directory), directory + '\CR6_TablePLCRTO16Stats.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLCRTO16Stats.dat", r"{}\CR6_TablePLCRTO16Stats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLCRTO16Stats.dat".format(directory))
                os.rename(r"{}\CR6_TablePLCRTO16Stats.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TablePLCRTO16Stats.dat", r"{}\CR6_TablePLCRTO16Stats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TablePLCRTO16Stats.dat".format(directory))
                os.rename(r"{}\CR6_TablePLCRTO16Stats.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TableDailyStats - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyStats - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TableDailyStats - Copy.txt".format(directory), directory + '\CR6_TableDailyStats.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableDailyStats.dat", r"{}\CR6_TableDailyStats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyStats.dat".format(directory))
                os.rename(r"{}\CR6_TableDailyStats.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableDailyStats.dat", r"{}\CR6_TableDailyStats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyStats.dat".format(directory))
                os.rename(r"{}\CR6_TableDailyStats.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TableDailyComb - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyComb - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TableDailyComb - Copy.txt".format(directory), directory + '\CR6_TableDailyComb.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableDailyComb.dat", r"{}\CR6_TableDailyComb.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyComb.dat".format(directory))
                os.rename(r"{}\CR6_TableDailyComb.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableDailyComb.dat", r"{}\CR6_TableDailyComb.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableDailyComb.dat".format(directory))
                os.rename(r"{}\CR6_TableDailyComb.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TableThermocouples - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TableThermocouples - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TableThermocouples - Copy.txt".format(directory), directory + '\CR6_TableThermocouples.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableThermocouples.dat", r"{}\CR6_TableThermocouples.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableThermocouples.dat".format(directory))
                os.rename(r"{}\CR6_TableThermocouples.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableThermocouples.dat", r"{}\CR6_TableThermocouples.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableThermocouples.dat".format(directory))
                os.rename(r"{}\CR6_TableThermocouples.dat".format(directory), pre + ' - Copy.txt')
            ####################################################################################################################################
            if os.path.isfile(r"{}\CR6_TableCommStats - Copy.txt".format(directory)) == True:
                pre, ext = os.path.splitext(r"{}\CR6_TableCommStats - Copy.txt".format(directory))
                os.rename(r"{}\CR6_TableCommStats - Copy.txt".format(directory), directory + '\CR6_TableCommStats.dat')
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableCommStats.dat", r"{}\CR6_TableCommStats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableCommStats.dat".format(directory))
                os.rename(r"{}\CR6_TableCommStats.dat".format(directory), pre + ' - Copy.txt')
            else:
                copyfile(r"C:\Campbellsci\LoggerNet\CR6_TableCommStats.dat", r"{}\CR6_TableCommStats.dat".format(directory))
                pre, ext = os.path.splitext(r"{}\CR6_TableCommStats.dat".format(directory))
                os.rename(r"{}\CR6_TableCommStats.dat".format(directory), pre + ' - Copy.txt')

                

        elif user_input == '3':
            print 'Archiving Report Output.\n'
            sys.path.insert(0, '/_7_Archive_Output/')
            from _7_Archive_Output import Dashboard_Archive_Output
            Dashboard_Archive_Output.archiveOutput()
            
            pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTOFP - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TablePLC_RTOFP - Copy.txt".format(directory), directory + '\CR6_TablePLC_RTOFP.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TablePLC_RTO32 - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TablePLC_RTO32 - Copy.txt".format(directory), directory + '\CR6_TablePLC_RTO32.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TablePLC_SVE - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TablePLC_SVE - Copy.txt".format(directory), directory + '\CR6_TablePLC_SVE.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TablePLCRTO16Stats - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TablePLCRTO16Stats - Copy.txt".format(directory), directory + '\CR6_TablePLCRTO16Stats.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TableDailyStats - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TableDailyStats - Copy.txt".format(directory), directory + '\CR6_TableDailyStats.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TableDailyComb - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TableDailyComb - Copy.txt".format(directory), directory + '\CR6_TableDailyComb.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TableThermocouples - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TableThermocouples - Copy.txt".format(directory), directory + '\CR6_TableThermocouples.dat')

            pre, ext = os.path.splitext(r"{}\CR6_TableCommStats - Copy.txt".format(directory))
            os.rename(r"{}\CR6_TableCommStats - Copy.txt".format(directory), directory + '\CR6_TableCommStats.dat')
            

            files_dat = [filename for filename in os.listdir(directory) if filename.startswith("CR6") or filename.startswith("CR6")]
            f_name = files_dat[0]
            f_path = os.path.join(directory, f_name)
            f_date = os.path.getmtime(f_path)
            file_date = datetime.datetime.fromtimestamp(f_date)
            archive_folder_name = '{dt.year}-{dt.month}-{dt.day}'.format(dt = file_date)
            archive_folder = os.path.join(backup_dir, archive_folder_name)

            if os.path.exists(archive_folder) == False:
                os.mkdir(archive_folder)
                copyfile('{}\CR6_TablePLC_RTOFP.dat'.format(directory), '{}\CR6_TablePLC_RTOFP.dat'.format(archive_folder))
                copyfile('{}\CR6_TablePLC_RTO32.dat'.format(directory), '{}\CR6_TablePLC_RTO32.dat'.format(archive_folder))
                copyfile('{}\CR6_TablePLC_SVE.dat'.format(directory), '{}\CR6_TablePLC_SVE.dat'.format(archive_folder))
                copyfile('{}\CR6_TablePLCRTO16Stats.dat'.format(directory), '{}\CR6_TablePLCRTO16Stats.dat'.format(archive_folder))
                copyfile('{}\CR6_TableDailyStats.dat'.format(directory), '{}\CR6_TableDailyStats.dat'.format(archive_folder))
                copyfile('{}\CR6_TableDailyComb.dat'.format(directory), '{}\CR6_TableDailyComb.dat'.format(archive_folder))
                copyfile('{}\CR6_TableThermocouples.dat'.format(directory), '{}\CR6_TableThermocouples.dat'.format(archive_folder))
                copyfile('{}\CR6_TableCommStats.dat'.format(directory), '{}\CR6_TableCommStats.dat'.format(archive_folder))
                

                today = datetime.datetime.now()
                m = today.strftime("%m")
                d = today.strftime("%d")
                y = today.strftime("%Y")

                if int(y) > int(2019):
                    dir_num = int(m) + (int(12) * (int(y) - int(2019)))
                else:
                    if int(m) < int(10):
                        dir_num = '0{}'.format(int(m))
                    else:
                        dir_num = int(m)
                    
                dir_month = today.strftime("%B")
                dir_year = y

                dir_name = '{} - {}{}'.format(dir_num, dir_month, dir_year)
                
                today = '{}-{}-{}'.format(y, today.strftime("%#m"), today.strftime("%#d"))

                data_folder = os.path.join(backup_dir, '{}'.format(today))
                data_archive = os.path.join(backup_dir, '{}'.format(dir_name))
    
                if os.path.exists(data_archive) == True:
                    pass
                else:
                    os.mkdir(data_archive)
                    
                if os.path.exists(os.path.join(data_archive, today)) == True:
                    pass
                else:
                    shutil.move(data_folder, data_archive)

        
            else:
                print 'Loggernet files have already been backed up.'
                print '\n******************************************************************************\n'

        elif user_input == '2':
            break

        elif user_input == '0':
            sys.exit()
        else:
            continue


if __name__ == "__main__":
    main()
