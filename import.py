from flask import Flask
from flask import render_template
import pandas as pd
import main

web=Flask(__name__)

#proj name for indexing#
proj_name_hc = "51 Melcher Street"
num = main.proj_list.index(proj_name_hc)
cur_proj_df = main.proj_dfs[num]
cur_proj_desk_count = cur_proj_df['desk_count'].sum()
#set up list of space types in the project#
cur_proj_space_list = main.space_type_dict[proj_name_hc]
#set up list of area sums for each type#
cur_proj_space_area_sums_list = main.proj_areas_dict[proj_name_hc]
#create new df which only includes area sums per space type#
cur_proj_sum_df = pd.DataFrame(cur_proj_space_area_sums_list, index=cur_proj_space_list)


@web.route('/')
@web.route('/harvests')
def harvests():
    proj_count = str(len(main.proj_list))
    sf2 = main.sf
    return render_template('harvests.html', title = 'Home', proj_count = proj_count, sf2 = sf2)

@web.route('/project')
def project():
    project1 = {'projname': proj_name_hc}
    desks = {'deskcount': cur_proj_desk_count} 
    cur_proj_area = sum(cur_proj_space_area_sums_list)
    proj_sf = str(int(cur_proj_area))
    return render_template('Project.html', title = 'Project', desks=desks, project1 = project1, proj_sf=proj_sf)

if __name__=='__main__':
        web.run(host='127.0.0.1',debug=True)