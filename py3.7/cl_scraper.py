import csv
import copy
import datetime
import time
import logging
from craigslist import CraigslistHousing
from craigslist_information import Filters as clsd #make better abbreviation later
from craigslist_information import States as sr #make better abbreviation later
from user_information import SelectionKeys as sk

class CL_Housing_Select:
    def __init__(self, inst_site, inst_category, inst_filters, code_break,geotag=False):
        self.geotag = geotag
        self.inst_site = inst_site
        self.inst_category = inst_category
        self.inst_filters = inst_filters
        self.code_break = code_break

    def small_region(self):
        self.cl_instance = CraigslistHousing(site=self.inst_site,category=self.inst_category,filters=self.inst_filters)

    def large_region(self, inst_area):
        self.cl_instance = CraigslistHousing(site=self.inst_site,category=self.inst_category,filters=self.inst_filters,area=inst_area)

    def exec_search(self, header_list, state, region, sub_region, category):
        header_list.extend([f"{state.title()}{self.code_break}{region}{self.code_break}{sub_region}{self.code_break}{category}{self.code_break}{i['id']}{self.code_break}{i['repost_of']}{self.code_break}{i['name']}{self.code_break}{i['url']}{self.code_break}{i['datetime'][0:10]}{self.code_break}{i['datetime'][11:]}{self.code_break}{i['price']}{self.code_break}{i['where']}{self.code_break}{i['has_image']}{self.code_break}{i['geotag']}{self.code_break}{i['bedrooms']}{self.code_break}{i['area']}" for i in self.cl_instance.get_results(sort_by='newest', geotagged=self.geotag)])
        return header_list

    def write_to_file(self, write_list, inst_site_name, inst_state_name, house_filter):
        date = datetime.date.today()
        title = f'{date}_{house_filter}_in_{inst_site_name}_{inst_state_name}.csv'
        with open(title, 'w', newline = '') as rm_csv:
            writer = csv.writer(rm_csv, delimiter = ',')
            writer.writerows([i.split(self.code_break) for i in write_list])
        rm_csv.close()

def my_logger(func):
    logging.basicConfig(filename=f'{func.__name__}.log', level = logging.INFO)
    def wrapper(*args, **kwargs):
        date_time = str(datetime.datetime.now())[:-10]
        log_dict = {**clsd.distance_filters, **clsd.extra_filters}
        logging.info(
            f'Ran with filters: {log_dict} at {date_time}') #look into dict merge...
        return func(*args, **kwargs)
    return wrapper

class ExecSearch:
    def __init__(self, states, zip_list, regions, subregions, house_filter):
        self.zip_list = zip_list
        self.states = states
        self.regions = regions
        self.subregions = subregions
        self.house_filter = house_filter #this is a list of selected categories (i.e. 'apa' or 'roo')
        self.room_filter = {**clsd.extra_filters, **clsd.distance_filters} 
        self.code_break = ';n@nih;'
        self.header = [f'CL State{self.code_break}CL Region{self.code_break}CL District{self.code_break}Housing Category{self.code_break}Post ID{self.code_break}Repost of (Post ID){self.code_break}Title{self.code_break}URL{self.code_break}Date Posted{self.code_break}Time Posted{self.code_break}Price{self.code_break}Location{self.code_break}Post has Image{self.code_break}Post has Geotag{self.code_break}Bedrooms{self.code_break}Area']

    def search_package(self, state, reg, cat, area = ""):
        #if zip is filled, don't focus on focus_dict - 2019-09-19
        header_list = copy.deepcopy(self.header)
        housing_result = CL_Housing_Select(reg, cat, self.room_filter, self.code_break)
        if area == "":
            area = reg
            housing_result.small_region()
        else:
            housing_result.large_region(area)
        append_list = housing_result.exec_search(header_list, state.title(), reg, area, cat)
        housing_result.write_to_file(append_list, area, state, cat)

    @my_logger
    def cl_search(self):
        t0 = time.time()
        housing_dict = clsd.cat_dict
        if len(self.zip_list) != 0:
            self.room_filter['zip_code'] = self.zip_list[0]
            self.room_filter['search_distance'] = self.zip_list[1]
        #reg site must be included for zip_search to work outside of the bay area!! refactor refactor
        for state in self.states:
            focus_list = []
            try:
                for reg, reg_name in eval(f'sr.{state}')["focus_dist"].items():
                    if reg in self.regions:
                        is_loop = True
                        if reg == 'newyork' or reg == 'boston':
                            housing_dict = clsd.apa_dict
                        for sub_reg in reg_name:
                            for cat in housing_dict:
                                if cat not in self.house_filter:
                                    continue
                                elif self.room_filter['zip_code'] != None and self.room_filter['search_distance'] != None:
                                    self.search_package(state, reg, cat)
                                    is_loop = False
                                    break
                                else:
                                    self.search_package(state, reg, cat, sub_reg)
                            if not is_loop:
                                break
                    focus_list.append(reg)
            except KeyError:
                for reg, reg_name in eval(f'sr.{state}').items():
                    if reg in self.regions:
                        if reg in focus_list:
                            continue
                        else:
                            try:
                                for cat in housing_dict:
                                    if cat not in self.house_filter:
                                        continue
                                    else:
                                        self.search_package(state, reg, cat)
                            except ValueError:
                                print('focus_dict encountered')
                                pass
        t1 = time.time()
        print(f"Run time: {'%.2f' % (t1 - t0)} sec")