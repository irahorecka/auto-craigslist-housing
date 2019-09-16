#Look for all sublets and rooms in sfbay craigslist, sort out statistically significant pricings, i.e. mean - 1sd after outlier removal
#Afterwards, only sort out districts of interest, e.g. berkeley, oakland, fremont.

import pandas as pd
import os
import csv
import datetime
import single_bedroom_01_ver as sbs
from craigslist_information import Filters as clsd #make better abbreviation later
from user_information import SelectionKeys as sk
import copy
pd.options.mode.chained_assignment = None

base_dir = os.getcwd()
os.chdir(f'{base_dir}/single_room_csv/CL Files')

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
        dtfm.loc[:,'Location'] = dtfm['Location'].str.lower()
        if len(dist_list) == 0:
            return_dtfm = dtfm
        else:
            for i in dist_list:
                return_dtfm = return_dtfm.append(dtfm.loc[dtfm['Location'].str.contains(i.lower())])
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
        dtfm = copy.deepcopy(self.dtfm)
        dtfm['Title Key'] = dtfm['Title'] + ' _ ' + dtfm['Location']
        dtfm['Num Time'] = pd.Series(cut_time())
        dtfm = dtfm.sort_values(by = ['Date Posted', 'Num Time'], ascending = [False, False], inplace = False, kind = 'quicksort')
        return dtfm

#should the functions below be made into classes?
def compile_dtfm():
    dtfm = pd.DataFrame()
    for filename in os.listdir():
        if filename[-4:] == '.csv':
            concat_dtfm = pd.read_csv(filename, sep = ',')
            #make key for title + location and remove duplicates
            concat_dtfm['Title Key'] = concat_dtfm['Title'] + ' _ ' + concat_dtfm['Location']
            concat_dtfm['Price'] = concat_dtfm['Price'].str[1:].astype(float)
            dtfm = dtfm.append(concat_dtfm, ignore_index=True, sort = False)
            #remove generated CL filenames to save space
            os.remove(filename)
        else:
            pass
    dtfm = dtfm.drop_duplicates(subset = ['Title Key'], keep = False)
    dtfm = dtfm.drop(['Bedrooms', 'Post ID', 'Repost of (Post ID)', 'Post has Image', 'Post has Geotag', 'Title Key'], axis = 1)
    return dtfm

def drop_and_sort(dtfm1, dtfm2):
    dtfm = dtfm1.append(dtfm2, ignore_index = True, sort = False)
    dtfm = dtfm.drop_duplicates(subset = ['Title Key'], keep = False)
    dtfm = dtfm.drop(['Title Key', 'Num Time'], axis = 1)
    return dtfm


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
            significant_posts = temp_dist_dtfm.stat_significant(temp_sans_outlier, 0.8)
            select_district = temp_dist_dtfm.select_districts(significant_posts, sk.district_list)
            for_export = for_export.append(select_district, ignore_index=True, sort = False)
            
    os.chdir(f'{base_dir}/single_room_csv/Significant Deals')
    old_file = pd.read_csv('significant posts.csv')
    parse_old_file = DataPrep(old_file).title_key()
    parse_for_export = DataPrep(for_export).title_key()
    concat_file = drop_and_sort(parse_for_export, parse_old_file)
 
    ref_file = concat_file.append(old_file, ignore_index = True, sort = False)
    ref_file.to_csv('significant posts.csv', index = False)
    concat_file.to_csv('new_post.csv', index = False)
    return concat_file

def execute_search():
    search_criteria = sbs.ExecSearch(sk.state_keys, sk.selected_reg, sk.district_list, sk.selected_cat)
    search_criteria.cl_search()