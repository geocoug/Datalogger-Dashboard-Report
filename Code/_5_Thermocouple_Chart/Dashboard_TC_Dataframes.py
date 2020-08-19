#!/usr/bin/python
import pandas as pd

def CreateDataframes(df):
    """ TC1 """
#TC1-7
    df1_7 = df[['TC1-7 Date', 'TC1-7 Temp']].copy()
    df1_7.dropna(axis=0, inplace=True)
#TC1-14
    df1_14 = df[['TC1-14 Date', 'TC1-14 Temp']].copy()
    df1_14.dropna(axis=0, inplace=True)
#TC1-24
    df1_24 = df[['TC1-24 Date', 'TC1-24 Temp']].copy()
    df1_24.dropna(axis=0, inplace=True)
#TC1-29
    df1_29 = df[['TC1-29 Date', 'TC1-29 Temp']].copy()
    df1_29.dropna(axis=0, inplace=True)

    """ TC2 """
#TC2-16
    df2_16 = df[['TC2-16 Date', 'TC2-16 Temp']].copy()
    df2_16.dropna(axis=0, inplace=True)
#TC2-27
    df2_27 = df[['TC2-27 Date', 'TC2-27 Temp']].copy()
    df2_27.dropna(axis=0, inplace=True)
#TC2-32
    df2_32 = df[['TC2-32 Date', 'TC2-32 Temp']].copy()
    df2_32.dropna(axis=0, inplace=True)
#TC2-36
    df2_36 = df[['TC2-36 Date', 'TC2-36 Temp']].copy()
    df2_36.dropna(axis=0, inplace=True)

    """ TC3 """
#TC3-16
    df3_16 = df[['TC3-16 Date', 'TC3-16 Temp']].copy()
    df3_16.dropna(axis=0, inplace=True)
#TC3-25
    df3_25 = df[['TC3-25 Date', 'TC3-25 Temp']].copy()
    df3_25.dropna(axis=0, inplace=True)
#TC3-30
    df3_30 = df[['TC3-30 Date', 'TC3-30 Temp']].copy()
    df3_30.dropna(axis=0, inplace=True)
#TC3-37
    df3_37 = df[['TC3-37 Date', 'TC3-37 Temp']].copy()
    df3_37.dropna(axis=0, inplace=True)

    """ TC4 """
#TC4-14
    df4_14 = df[['TC4-14 Date', 'TC4-14 Temp']].copy()
    df4_14.dropna(axis=0, inplace=True)
#TC4-19
    df4_19 = df[['TC4-19 Date', 'TC4-19 Temp']].copy()
    df4_19.dropna(axis=0, inplace=True)
#TC4-24
    df4_24 = df[['TC4-24 Date', 'TC4-24 Temp']].copy()
    df4_24.dropna(axis=0, inplace=True)
#TC4-30
    df4_30 = df[['TC4-30 Date', 'TC4-30 Temp']].copy()
    df4_30.dropna(axis=0, inplace=True)

    """ TC5 """
#TC5-12
    df5_12 = df[['TC5-12 Date', 'TC5-12 Temp']].copy()
    df5_12.dropna(axis=0, inplace=True)
#TC5-21
    df5_21 = df[['TC5-21 Date', 'TC5-21 Temp']].copy()
    df5_21.dropna(axis=0, inplace=True)
#TC5-28
    df5_28 = df[['TC5-28 Date', 'TC5-28 Temp']].copy()
    df5_28.dropna(axis=0, inplace=True)
#TC5-33
    df5_33 = df[['TC5-33 Date', 'TC5-33 Temp']].copy()
    df5_33.dropna(axis=0, inplace=True)

    """ TC6 """
#TC6-12
    df6_12 = df[['TC6-12 Date', 'TC6-12 Temp']].copy()
    df6_12.dropna(axis=0, inplace=True)
#TC6-22
    df6_22 = df[['TC6-22 Date', 'TC6-22 Temp']].copy()
    df6_22.dropna(axis=0, inplace=True)
#TC6-25
    df6_25 = df[['TC6-25 Date', 'TC6-25 Temp']].copy()
    df6_25.dropna(axis=0, inplace=True)
#TC6-29
    df6_29 = df[['TC6-29 Date', 'TC6-29 Temp']].copy()
    df6_29.dropna(axis=0, inplace=True)
#TC6-36
    df6_36 = df[['TC6-36 Date', 'TC6-36 Temp']].copy()
    df6_36.dropna(axis=0, inplace=True)

    """ TC7 """
#TC7-17
    df7_17 = df[['TC7-17 Date', 'TC7-17 Temp']].copy()
    df7_17.dropna(axis=0, inplace=True)
#TC7-23
    df7_23 = df[['TC7-23 Date', 'TC7-23 Temp']].copy()
    df7_23.dropna(axis=0, inplace=True)
#TC7-26
    df7_26 = df[['TC7-26 Date', 'TC7-26 Temp']].copy()
    df7_26.dropna(axis=0, inplace=True)

    """ TC8 """
#TC8-13
    df8_13 = df[['TC8-13 Date', 'TC8-13 Temp']].copy()
    df8_13.dropna(axis=0, inplace=True)
#TC8-17
    df8_17 = df[['TC8-17 Date', 'TC8-17 Temp']].copy()
    df8_17.dropna(axis=0, inplace=True)
#TC8-26
    df8_26 = df[['TC8-26 Date', 'TC8-26 Temp']].copy()
    df8_26.dropna(axis=0, inplace=True)

    """ TC9 """
#TC9-19
    df9_19 = df[['TC9-19 Date', 'TC9-19 Temp']].copy()
    df9_19.dropna(axis=0, inplace=True)
#TC9-25
    df9_25 = df[['TC9-25 Date', 'TC9-25 Temp']].copy()
    df9_25.dropna(axis=0, inplace=True)
#TC9-29
    df9_29 = df[['TC9-29 Date', 'TC9-29 Temp']].copy()
    df9_29.dropna(axis=0, inplace=True)


    df_list = []
    df_list.extend((df1_7, df1_14, df1_24, df1_29,
                    df2_16, df2_27, df2_32, df2_36,
                    df3_16, df3_25, df3_30, df3_37,
                    df4_14, df4_19, df4_24, df4_30,
                    df5_12, df5_21, df5_28, df5_33,
                    df6_12, df6_22, df6_25, df6_29, df6_36,
                    df7_17, df7_23, df7_26,
                    df8_13, df8_17, df8_26,
                    df9_19, df9_25, df9_29))
    
    return df_list
