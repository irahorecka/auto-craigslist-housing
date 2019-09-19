class ExecSearch:
    def __init__(self, states, zip_list, regions, subregions, house_filter, room_filter, housing_dict):
        self.zip_list = zip_list
        self.states = states
        self.regions = regions
        self.subregions = subregions
        self.house_filter = house_filter #this is a list of selected categories (i.e. 'apa' or 'roo')
        self.room_filter = room_filter #i.e. merge the two filters in execute_search.py
        self.code_break = ';n@nih;'
        self.header = [f'CL State{self.code_break}CL Region{self.code_break}CL District{self.code_break}Housing Category{self.code_break}Post ID{self.code_break}Repost of (Post ID){self.code_break}Title{self.code_break}URL{self.code_break}Date Posted{self.code_break}Time Posted{self.code_break}Price{self.code_break}Location{self.code_break}Post has Image{self.code_break}Post has Geotag{self.code_break}Bedrooms{self.code_break}Area']

    def search_package(self, state, reg, cat, area = ""):
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
    #run function without geotagged=True to save time
    def cl_search(self):
        t0 = time.time()
        #housing_dict = clsd.cat_dict
        #filter_dict = {**clsd.distance_filters, **clsd.extra_filters}
        #reg site must be included for zip_search to work outside of the bay area!! refactor refactor
        for state in self.states:
            focus_list = []
            try:
                for reg, reg_name in eval(f'sr.{state}')["focus_dist"].items():
                    if reg in self.regions:
                        if reg == 'newyork' or reg == 'boston':
                            housing_dict = clsd.apa_dict
                        for sub_reg in reg_name:
                            for cat in housing_dict:
                                if cat not in self.room_filter:
                                    continue
                                else:
                                    self.search_package(state, reg, cat, sub_reg)
                    focus_list.append(reg)
            except KeyError:
                for reg, reg_name in eval(f'sr.{state}').items():
                    if reg in self.regions:
                        if reg in focus_list:
                            continue
                        else:
                            if len(self.zip_list) != 0:
                                self.room_filter['zip_code'] = self.zip_list[0]
                                self.room_filter['search_distance'] = self.zip_list[1]
                            try:
                                for cat in housing_dict:
                                    if cat not in self.house_filter:
                                        continue
                                    else:
                                        self.search_package(state, reg, cat)
                            except ValueError:
                                print('focus_dict encountered')
                                pass



            if 'focus_dist' in eval(f'sr.{state}'):
                for reg, reg_name in eval(f'sr.{state}')["focus_dist"].items():
                    if reg in self.regions:
                        if reg == 'newyork' or reg == 'boston':
                            housing_dict = clsd.apa_dict
                        for sub_reg in reg_name:
                            for cat, cat_name in housing_dict.items():
                                header_list = copy.deepcopy(self.header)
                                if cat not in self.filter:
                                    continue
                                else:
                                    housing_result = CL_Housing_Select(reg, cat, filter_dict, self.code_break)
                                    housing_result.large_region(sub_reg)
                                    append_list = housing_result.exec_search(header_list, state.title(), reg, sub_reg, cat_name)
                                    print(state, sub_reg, cat)
                                    housing_result.write_to_file(append_list, sub_reg, state, housing_dict[cat])
                    focus_list.append(reg)
            for reg, reg_name in eval(f'sr.{state}').items():
                if reg in self.regions:
                    if reg in focus_list:
                        continue
                    else:
                        if len(self.zip_list) != 0:
                            filter_dict['zip_code'] = self.zip_list[0]
                            filter_dict['search_distance'] = self.zip_list[1]
                        try:
                            for cat, cat_name in housing_dict.items():
                                header_list = copy.deepcopy(self.header)
                                if cat not in self.filter:
                                    continue
                                else:
                                    housing_result = CL_Housing_Select(reg, cat, filter_dict, self.code_break)
                                    housing_result.small_region()
                                    append_list = housing_result.exec_search(header_list, state.title(), reg, reg, cat_name)
                                    print(state, reg, cat)
                                    housing_result.write_to_file(append_list, reg_name, state, housing_dict[cat])
                        except ValueError:
                            print('focus_dict encountered')
                            pass