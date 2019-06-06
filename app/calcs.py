import main
import numpy as np
from math import pi
from bokeh.io import output_file, show, curdoc, save
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.resources import INLINE
from bokeh.util.browser import view
import pandas as pd

#proj name for indexing#
proj_name_hc = "51 Melcher Street"
num = main.proj_list.index(proj_name_hc)
num = 50
name = main.proj_list[num]
cur_proj_df = main.proj_dfs[num]
cur_proj_desk_count = cur_proj_df['desk_count'].sum()
#set up list of space types in the project#
cur_proj_space_list = main.space_type_dict[name]
#set up list of area sums for each type#
cur_proj_space_area_sums_list = main.proj_areas_dict[name]
#create new df which only includes area sums per space type#
cur_proj_sum_df = pd.DataFrame(cur_proj_space_area_sums_list, index=cur_proj_space_list)
#count the floors#
proj_floors = cur_proj_df['floor'].unique()
floor_count = str(len(proj_floors))

#set up plot#
cur_proj_sum_df.columns = ['sf']
cur_proj_color_list = []
for x in cur_proj_space_list : 
    cur_proj_color_list.append(main.space_colors_dict[x])


keys = cur_proj_space_list
values = cur_proj_space_area_sums_list
x = dict(zip(keys, values))

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'space'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = cur_proj_color_list

p = figure(plot_height=350, title="Space Ratios", toolbar_location=None,
           tools="hover", tooltips="@space: @value", x_range=(-0.5, 1.0), name="pie")

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='space', source=data)

output_file("app/templates/graph.html")
p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None
save(p)