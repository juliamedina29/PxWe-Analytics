import numpy as np
import pandas as pd
import sqlalchemy as sql
import os

#------------------stargate parameters--------------------#
star_host = 'redshift-production.weworkers.io'
star_user = str(os.environ.get('STAR_USER'))
star_pwd = str(os.environ.get('STAR_PWD'))
star_db = 'analyticdb'
star_port = '5439'
redshift_string = 'redshift+psycopg2://{}:{}@{}:5439/{}'.format(star_user, star_pwd, star_host, star_db)

#------------------postgressql strings--------------------#
PxWe_spaces= """SELECT DISTINCT
pr.address1 AS project,
fl.description AS floor,
rm.name AS room,
rm.program_type AS space_type,
rm.number AS room_number,
rm.area_sf AS sf,
rm.desk_count AS desk_count
FROM stargate_bi_tables.bi_space as rm
INNER JOIN stargate_bi_tables.bi_floor as fl ON fl.current_harvest_sync_uuid = rm.harvest_sync_log_uuid
INNER JOIN stargate_bi_tables.bi_property as pr ON pr.uuid = fl.property_uuid
INNER JOIN stargate_bi_tables.bi_project as pj ON pj.property_uuid= pr.uuid
INNER JOIN stargate_bi_tables.bi_projecttype AS t ON pj.type_id=t.id
INNER JOIN stargate_bi_tables.bi_status as pjstat ON pjstat.id = pj.status_id
WHERE pjstat.name != 'Dead' AND ((t.name = 'PxWe') OR (t.name = 'Enterprise - Custom') OR (t.name = 'Enterprise - Off the Shelf')) AND sf > 0  
ORDER BY project, room_number"""

#------------------connection and df----------------------#
def fetch(connection_string, postgresql_string):

    engine = sql.create_engine(connection_string, connect_args={'sslmode': 'prefer'})
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql(postgresql_string, conn)

    return df

#-------------Fetch Raw Data From Redshift----------------#
rooms = fetch(redshift_string, PxWe_spaces)

#-----------Function for finding avg of list--------------#
def Average(lst): 
    return sum(lst) / len(lst)

#-----------------set up color dictionary-----------------#
space_colors_dict = {
    'CIRCULATE':'#FFF7DF',
    'MEET':'#B7F0D9',
    'OPERATE': '#E2E2E2',
    'WE': '#FFD26A',
    'WASH': '#C3C3C3',
    'WORK':'#ABDDE7',
    'SERVE': '#41C0C0',
    'INFRASTRUCTURE': '#41C0C0',
    'THRIVE': '#41C0C0',
    'BASE': '#41C0C0',
    'MEETING': '#41C0C0',
    'OTHER': '#41C0C0',
    'SUPPORT': '#41C0C0',
    'TYPICAL OFFICE': '#41C0C0',
    'WORKSTATIONS': '#41C0C0',
    'EAT & DRINK': '#41C0C0',
    'PLAY': '#41C0C0',
    'HALLWAY': '#41C0C0',
    'PHONE ROOM': '#41C0C0',
    'VT': '#41C0C0',
    'BREAKOUT': '#41C0C0',
    'OUTDOOR': '#41C0C0',
}

#---------------separate projects----------------#
proj_list = []
for x in rooms['project'].unique() :
    proj_list.append(x)

proj_count = len(proj_list)

#---------------create list of dataframes-----------------#
proj_dfs = []
for x in range(0, len(proj_list)) :
    indices = rooms['project'] == proj_list[x]
    proj_dfs.append(rooms.loc[indices,["project", "space_type","sf","desk_count","floor"]])

#-----------create list of types per project--------------#
type_list = []
proj_types =[]
for x in range(0, len(proj_dfs)) :
    type_list = proj_dfs[x]['space_type'].unique()
    proj_types.append(type_list)

#----------create dict matching types to proj-------------#
keys = proj_list
values = proj_types
space_type_dict = dict(zip(keys, values))

#----create dict matching proj names to respective dfs----#
keys = proj_list
values = proj_dfs
proj_df_dict = dict(zip(keys, values))

#--------------------finding area sums--------------------#
proj_areas =[]
for y in range(0,proj_count) :
    cur_proj_name = proj_list[y]
    cur_proj_df = proj_df_dict[cur_proj_name]
    area_list = []
    for x in range(len(space_type_dict[cur_proj_name])) :
        new_area_sum = cur_proj_df.loc[cur_proj_df['space_type'] == space_type_dict[cur_proj_name][x], 'sf'].sum()
        area_list.append(new_area_sum)
    proj_areas.append(area_list)
proj_areas_dict = dict(zip(proj_list, proj_areas))

#--------------------find total area---------------------#
total_proj_areas =[]
for y in range(0,proj_count) :
    cur_proj_name = proj_list[y]
    cur_proj_df = proj_df_dict[cur_proj_name]
    total_area_sum = cur_proj_df['sf'].sum()
    total_proj_areas.append(total_area_sum)
lst = total_proj_areas    
avg = Average(lst)
sf = round(avg, 2)