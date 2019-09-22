import pandas as pd
import os
import csv
import datetime
from craigslist_information import Filters as clsd #make better abbreviation later
from user_information import SelectionKeys as sk
import copy
pd.options.mode.chained_assignment = None

base_dir = os.getcwd()
os.chdir(f'{base_dir}/housing_csv/CL Files')

class StatAnalysis:
    def __init__(self, dtfm):
        self.dtfm = dtfm
    
    def omit_outlier(self):
        self.dtfm = self.dtfm.loc[self.dtfm['Price'] != 0]
        Q1 = self.dtfm['Price'].quantile(0.25)
        Q3 = self.dtfm['Price'].quantile(0.75)
        IQR = Q3 - Q1
        self.dtfm = self.dtfm.loc[self.dtfm['Price'] <= Q3 + 1.5*IQR]
        self.dtfm = self.dtfm.loc[self.dtfm['Price'] >= Q1 - 1.5*IQR]
        #a trimmed mean will cut too much data from either tail, those this can be adjusted
        #consult whether an outlier excision or trimmed mean should be used for negating outliers

    def stat_significant(self, sd_val, val_type):
        mean_price, mean_price_area = self.dtfm['Price'].mean(), self.dtfm['Price_Area'].mean()
        sd_price, sd_price_area = self.dtfm['Price'].std(), self.dtfm['Price_Area'].std()
        if val_type == 0:
            self.dtfm = self.dtfm.loc[self.dtfm['Price'] <= (mean_price - sd_val*sd_price)]
            print('%.2f' % (mean_price - sd_val*sd_price), '%.2f' % (mean_price_area - sd_val*sd_price_area))
        else:
            self.dtfm = self.dtfm.loc[self.dtfm['Price'] >= (mean_price + sd_val*sd_price)]
            print('%.2f' % (mean_price + sd_val*sd_price), '%.2f' % (mean_price_area - sd_val*sd_price_area))
        if all(isinstance(i, type(None)) for i in self.dtfm['Price_Area']):
            pass
        else:
            self.dtfm = self.dtfm.loc[self.dtfm['Price_Area'] <= (mean_price_area + sd_val*sd_price_area)] #watch for hardcoded val

    def select_districts(self, dist_list):
        return_dtfm = pd.DataFrame()
        self.dtfm.loc[:,'Location'] = self.dtfm['Location'].str.lower()
        if len(dist_list) == 0:
            return_dtfm = self.dtfm
        else:
            for i in dist_list:
                return_dtfm = return_dtfm.append(self.dtfm.loc[self.dtfm['Location'].str.contains(i.lower())])
        self.dtfm = return_dtfm

    def curate_dtfm(self, housing_dist, sd, val_type):
        self.omit_outlier()
        self.stat_significant(sd, val_type)
        self.select_districts(housing_dist)
    
    def return_dtfm(self):
        return self.dtfm

        
class DataPrep: #does this need to be a class?
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
            #os.remove(filename)
        else:
            pass
    dtfm = dtfm.drop_duplicates(subset = ['Title Key'], keep = False)
    dtfm = dtfm.drop(['Post ID', 'Repost of (Post ID)', 'Post has Image', 'Post has Geotag', 'Title Key'], axis = 1)
    return dtfm

def drop_and_sort(dtfm1, dtfm2):
    dtfm = dtfm1.append(dtfm2, ignore_index = True, sort = False)
    dtfm = dtfm.drop_duplicates(subset = ['Title Key'], keep = False)
    dtfm = dtfm.drop(['Title Key', 'Num Time'], axis = 1)
    return dtfm

def find_rooms(dtfm, sd, val_type):
    #THIS IS MESSY BUT IT WORKS - WORK ON REFACTORING CODE TO GROUP VARIOUS OPERATIONS
    cat_val = sk.selected_cat
    reg_list = dtfm['CL District'].unique()
    for_export = pd.DataFrame()
    for i in cat_val:
        if i == 'apa' or i == 'vac': #find categories where bedrooms & price/area will be important
            bed_list = list(dtfm['Bedrooms'].unique())
            try:
                bed_list.remove('None')
            except ValueError:
                pass
            temp_dtfm = dtfm.loc[dtfm['Area'].str[-3:] == 'ft2']
            temp_dtfm['Area'] = temp_dtfm['Area'].str[:-3].astype(float)
            temp_dtfm['Price_Area'] = temp_dtfm['Price'] / temp_dtfm['Area']
            for j in bed_list:
                temp_dtfm_bed = temp_dtfm.loc[(temp_dtfm['Housing Category'] == i) & (temp_dtfm['Bedrooms'] == j)]
                for k in reg_list:    
                    temp_dtfm_curate = StatAnalysis(temp_dtfm_bed.loc[temp_dtfm['CL District'] == k])
                    temp_dtfm_curate.curate_dtfm(sk.district_list, sd, val_type)
                    for_export = for_export.append(temp_dtfm_curate.return_dtfm(), ignore_index=True, sort = False)
        else:
            bed_list = []
            temp_dtfm = dtfm
            temp_dtfm['Price_Area'] = None
            temp_dtfm = dtfm.loc[dtfm['Housing Category'] == i]
            for k in reg_list:    
                temp_dtfm_curate = StatAnalysis(temp_dtfm.loc[temp_dtfm['CL District'] == k])
                temp_dtfm_curate.curate_dtfm(sk.district_list, sd, val_type)
                for_export = for_export.append(temp_dtfm_curate.return_dtfm(), ignore_index=True, sort = False)
                     
    os.chdir(f'{base_dir}/housing_csv/Significant Deals')
    old_file = pd.read_csv('significant posts.csv')
    old_file = old_file.loc[old_file['Date Posted'].isin(i for i in [str(datetime.date.today() - datetime.timedelta(days=i)) for i in range(8)])] #capture past 8 days of information
    try: 
        trimmed_file = old_file.loc[old_file['Housing Category'].isin(i for i in for_export['Housing Category'].unique())] #filter housing cat of old file
    except KeyError: #will return for_export dataframe if empty
        return for_export
    trimmed_file = trimmed_file.loc[trimmed_file['Bedrooms'].isin(str(i) for i in for_export['Bedrooms'].unique())] #filter bedrooms of old file - dtype str
    trimmed_file = trimmed_file.loc[trimmed_file['CL District'].isin(i for i in for_export['CL District'].unique())] #filter cl_dist of old file
    parse_trimmed_file = DataPrep(trimmed_file).title_key()
    parse_for_export = DataPrep(for_export).title_key()
    concat_file = drop_and_sort(parse_for_export, parse_trimmed_file)
 
    ref_file = concat_file.append(old_file, ignore_index = True, sort = False)
    ref_file.to_csv('significant posts.csv', index = False)
    concat_file.to_csv('new_post.csv', index = False)
    return concat_file