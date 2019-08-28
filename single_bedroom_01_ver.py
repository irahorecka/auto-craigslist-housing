#2019-08-22 A refined single bedroom search on craigslist for actual housing help
#Goal: move away from creating .csv files, rather make a pandas dataframe to pipe to data analysis file
import os
import csv
from craigslist import CraigslistHousing
import datetime
import time
import logging
import cl_search_dict as clsd
import state_reg as sr
import selection_key as sk
#os.chdir('/Users/irahorecka/Desktop/Harddrive_Desktop/Python/Craigslist_project/Data/From Python/Single rooms')
date_time = str(datetime.datetime.now())[:-10]
date = datetime.date.today()
 
code_break = ';n@nih;'

class CL_Housing_Select:
    def __init__(self, inst_site, inst_category, inst_filters):
        self.inst_site = inst_site
        self.inst_category = inst_category
        self.inst_filters = inst_filters

    def small_region(self):
        return CraigslistHousing(site=self.inst_site,category=self.inst_category,filters=self.inst_filters)

    def large_region(self, inst_area):
        return CraigslistHousing(site=self.inst_site,category=self.inst_category,filters=self.inst_filters,area=inst_area)

    def write_to_file(self, write_list, inst_site_name, inst_state_name):
        title = f'{date} rooms and sublets in {inst_site_name}_{inst_state_name.title()}.csv'
        with open(title, 'w', newline = '') as rm_csv:
            writer = csv.writer(rm_csv, delimiter = ',')
            writer.writerows([i.split(code_break) for i in write_list])
        rm_csv.close()


def my_logger(func):
    logging.basicConfig(filename=f'{func.__name__}.log', level = logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(
            f'Ran with filters: {clsd.room_filters} at {date_time}')
        return func(*args, **kwargs)

    return wrapper

@my_logger
def exec_search():
    t0 = time.time()
    for state in sk.state_keys:
        focus_list = [] 
        if 'focus_dist' in eval(f'sr.{state}'):
            for reg, reg_name in eval(f'sr.{state}')["focus_dist"].items():
                if reg in sk.selected_reg:
                    if reg == 'newyork' or reg == 'boston':
                        for sub_reg in reg_name:
                            header_list = [f'CL State{code_break}CL Region{code_break}CL District{code_break}Housing Category{code_break}Post ID{code_break}Repost of (Post ID){code_break}Title{code_break}URL{code_break}Date Posted{code_break}Time Posted{code_break}Price{code_break}Location{code_break}Post has Image{code_break}Post has Geotag{code_break}Bedrooms{code_break}Area']
                            for cat, cat_name in clsd.apa_dict.items():
                                if cat in sk.selected_cat:
                                    housing_result = CL_Housing_Select(reg, cat, clsd.room_filters)
                                    large_region = housing_result.large_region(sub_reg)
                                    header_list.extend([f"{state.title()}{code_break}{reg}{code_break}{sub_reg}{code_break}{cat_name}{code_break}{i['id']}{code_break}{i['repost_of']}{code_break}{i['name']}{code_break}{i['url']}{code_break}{i['datetime'][0:10]}{code_break}{i['datetime'][11:]}{code_break}{i['price']}{code_break}{i['where']}{code_break}{i['has_image']}{code_break}{i['geotag']}{code_break}{i['bedrooms']}{code_break}{i['area']}" for i in large_region.get_results(sort_by='newest')])
                                    print(state, sub_reg, cat)
                            housing_result.write_to_file(header_list, sub_reg, state)
                            focus_list.append(reg)
                    else:
                        for sub_reg in reg_name:
                            header_list = [f'CL State{code_break}CL Region{code_break}CL District{code_break}Housing Category{code_break}Post ID{code_break}Repost of (Post ID){code_break}Title{code_break}URL{code_break}Date Posted{code_break}Time Posted{code_break}Price{code_break}Location{code_break}Post has Image{code_break}Post has Geotag{code_break}Bedrooms{code_break}Area']    
                            for cat, cat_name in clsd.cat_dict.items():
                                if cat in sk.selected_cat:
                                    housing_result = CL_Housing_Select(reg, cat, clsd.room_filters)
                                    large_region = housing_result.large_region(sub_reg)
                                    header_list.extend([f"{state.title()}{code_break}{reg}{code_break}{sub_reg}{code_break}{cat_name}{code_break}{i['id']}{code_break}{i['repost_of']}{code_break}{i['name']}{code_break}{i['url']}{code_break}{i['datetime'][0:10]}{code_break}{i['datetime'][11:]}{code_break}{i['price']}{code_break}{i['where']}{code_break}{i['has_image']}{code_break}{i['geotag']}{code_break}{i['bedrooms']}{code_break}{i['area']}" for i in large_region.get_results(sort_by='newest')])
                                    print(state, sub_reg, cat)
                            housing_result.write_to_file(header_list, sub_reg, state)
                            focus_list.append(reg)
        for reg, reg_name in eval(f'sr.{state}').items():
            if reg in sk.selected_reg:
                if reg in focus_list:
                    continue
                else:
                    try:
                        header_list = [f'CL State{code_break}CL Region{code_break}CL District{code_break}Housing Category{code_break}Post ID{code_break}Repost of (Post ID){code_break}Title{code_break}URL{code_break}Date Posted{code_break}Time Posted{code_break}Price{code_break}Location{code_break}Post has Image{code_break}Post has Geotag{code_break}Bedrooms{code_break}Area']    
                        for cat, cat_name in clsd.cat_dict.items():
                            if cat in sk.selected_cat:
                                housing_result = CL_Housing_Select(reg, cat, clsd.room_filters)
                                small_region = housing_result.small_region()
                                header_list.extend([f"{state.title()}{code_break}{reg}{code_break}{reg_name}{code_break}{cat_name}{code_break}{i['id']}{code_break}{i['repost_of']}{code_break}{i['name']}{code_break}{i['url']}{code_break}{i['datetime'][0:10]}{code_break}{i['datetime'][11:]}{code_break}{i['price']}{code_break}{i['where']}{code_break}{i['has_image']}{code_break}{i['geotag']}{code_break}{i['bedrooms']}{code_break}{i['area']}" for i in small_region.get_results(sort_by='newest')])
                                print(state, reg, cat)
                        housing_result.write_to_file(header_list, reg_name, state)
                    except ValueError:
                        pass

    t1 = time.time()
    print(f"Run time: {'%.2f' % (t1 - t0)} sec")
    