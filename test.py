import main
import pandas as pd
import calcs

#print(calcs.cur_proj_space_list)
#print(calcs.cur_proj_space_area_sums_list)

keys = cur_proj_space_list
values = cur_proj_space_area_sums_list
x = dict(zip(keys, values))
print(x)