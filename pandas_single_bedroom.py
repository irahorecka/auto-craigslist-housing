#Look for all sublets and rooms in sfbay craigslist, sort out statistically significant pricings, i.e. mean - 1sd after outlier removal
#Afterwords, only sort out districts of interest, e.g. berkeley, oakland, fremont.
#NEXT: Sort the dataframe to return only columns of interest - complete

import pandas as pd
import os
import csv
import datetime
import single_bedroom_01_ver as sbs
import cl_search_dict as clsd
import selection_key as sk
import matplotlib.pyplot as plt
os.chdir('/Users/irahorecka/Desktop/Harddrive_Desktop/Python/Auto_CL_Housing/single_room_csv/CL Files')

class StatAnalysis:
    def __init__(self, dtfm):
        self.dtfm = dtfm
    
    def omit_outlier(self):
        Q1 = self.dtfm['Price'].quantile(0.25)
        Q3 = self.dtfm['Price'].quantile(0.75)
        IQR = Q3 - Q1
        self.dtfm = self.dtfm.loc[self.dtfm['Price'] <= Q3 + 1.5*IQR]
        self.dtfm = self.dtfm.loc[self.dtfm['Price'] >= Q1 - 1.5*IQR]
        return self.dtfm

    def stat_significant(self, dtfm, sd_val):
        mean = dtfm['Price'].mean()
        sd = dtfm['Price'].std()
        return dtfm.loc[dtfm['Price'] <= (mean - sd_val*sd)]

    def select_districts(self, dtfm, dist_list):
        return_dtfm = pd.DataFrame()
        dist_list = [i.lower() for i in dist_list]
        for i in dist_list:
            for index,row in dtfm.iterrows():
                if i in row['Location'].lower():
                    return_dtfm = return_dtfm.append(row)
        return return_dtfm

class DataPrep:
    def __init__(self, dtfm):
        self.dtfm = dtfm
    
    def title_key(self):
        def cut_time():
            append_list = list()
            for index,row in self.dtfm.iterrows():
                if len(row['Time Posted']) == 5:
                    append_list.append(int(row['Time Posted'][:2]))
                elif len(row['Time Posted']) == 4:
                    append_list.append(int(row['Time Posted'][:1]))
            return append_list
        self.dtfm['Title Key'] = self.dtfm['Title'] + ' _ ' + self.dtfm['Location']
        self.dtfm['Num Time'] = pd.Series(cut_time())
        return self.dtfm


    def drop_and_sort(self):
        #set time posted as numeric - bonus see if you can make it a one-liner
        self.dtfm.sort_values(by = ['Date Posted', 'Num Time'], ascending = [False, False], inplace = True, kind = 'quicksort')
        #self.dtfm.sort_values(by = 'Num Time', ascending = False, inplace = True, kind = 'quicksort')
        self.dtfm = self.dtfm.drop(['Title Key', 'Num Time'], axis = 1)
        return self.dtfm

def compile_dtfm():
    dtfm = pd.DataFrame()
    for filename in os.listdir():
        if filename[-4:] == '.csv':
            concat_dtfm = pd.read_csv(filename, sep = ',')
            #make key for title + location and remove duplicates
            concat_dtfm['Title Key'] = concat_dtfm['Title'] + ' _ ' + concat_dtfm['Location']
            #change price to float64
            concat_dtfm['Price'] = concat_dtfm['Price'].str[1:].astype(float)
            dtfm = dtfm.append(concat_dtfm, ignore_index=True)
            dtfm = dtfm.drop_duplicates(subset = ['Title Key'])
            os.remove(filename)
        else:
            pass
    dtfm = dtfm.drop(['Bedrooms', 'Post ID', 'Repost of (Post ID)', 'Post has Image', 'Post has Geotag', 'Title Key'], axis = 1)
    return dtfm
#print(dtfm['Price'].describe())

def find_rooms(dtfm):
    cat_val = list()
    for i in sk.selected_cat:
        cat_val.append(clsd.cat_dict[i])

    for_export = pd.DataFrame()
    for i in cat_val:
        temp_dtfm = dtfm.loc[dtfm['Housing Category'] == i]
        reg_list = dtfm['CL District'].unique()
        for j in reg_list:    
            temp_dist_dtfm = StatAnalysis(temp_dtfm.loc[temp_dtfm['CL District'] == j])
            temp_sans_outlier = temp_dist_dtfm.omit_outlier()
            significant_posts = temp_dist_dtfm.stat_significant(temp_sans_outlier, 1)
            select_district = temp_dist_dtfm.select_districts(significant_posts, sk.district_list)
            for_export = for_export.append(select_district, ignore_index=True)
        #outlier_data = temp_sans_outlier['Price']
        '''plt.hist(outlier_data)
        plt.title(i)
        plt.show()'''
            
    os.chdir('/Users/irahorecka/Desktop/Harddrive_Desktop/Python/Auto_CL_Housing/single_room_csv/Significant Deals')
    old_file = pd.read_csv('significant posts.csv')

    old_file = DataPrep(old_file).title_key()
    for_export = DataPrep(for_export).title_key()

    for_export = for_export.append(old_file, ignore_index=True) 
    for_export = for_export.drop_duplicates(subset = ['Title Key'])

    old_file = DataPrep(old_file).drop_and_sort()
    for_export = DataPrep(for_export).drop_and_sort()
    new_find = for_export.append(old_file, ignore_index = True)
    new_find = new_find.drop_duplicates(subset = ['Title', 'Location'], keep = False)

    for_export.to_csv('significant posts.csv', index = False)
    new_find.to_csv('new_post.csv', index = False)
    return new_find

def execute_search():
    sbs.exec_search()

#data = compile_dtfm()
#find_rooms(data)