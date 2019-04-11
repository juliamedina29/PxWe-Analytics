import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
import dash_html_components as html
from flask import Flask, render_template
import pandas as pd
import main
import calcs

web=Flask(__name__)

@web.route('/')
@web.route('/harvests')
def harvests():
    proj_count = str(len(main.proj_list))
    sf2 = main.sf
    return render_template('harvests.html', title = 'Home', proj_count = proj_count, sf2 = sf2)

@web.route('/project')
def project():
    project1 = {'projname': calcs.name}
    desks = {'deskcount': int(calcs.cur_proj_desk_count)} 
    cur_proj_area = sum(calcs.cur_proj_space_area_sums_list)
    proj_sf = str(int(cur_proj_area))
    floors = calcs.floor_count
    return render_template('Project.html', title = 'Project', desks=desks, project1 = project1, proj_sf=proj_sf, floors = floors)

@web.route('/graph')
def graph() :
        return render_template('graph.html')

if __name__=='__main__':
        web.run(host='127.0.0.1',port=800,debug=True)