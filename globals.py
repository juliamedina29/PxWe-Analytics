#proj name for indexing#
proj_name_hc = "51 Melcher Street"
num = main.proj_list.index(proj_name_hc)
cur_proj_df = proj_dfs[num]

print("Project address: " + proj_name_hc)
cur_proj_desk_count = cur_proj_df['desk_count'].sum()
print("Desk count: " + str((int(cur_proj_desk_count))))
#set up list of space types in the project#
cur_proj_space_list = space_type_dict[proj_name_hc]
#set up list of area sums for each type#
cur_proj_space_area_sums_list = proj_areas_dict[proj_name_hc]
#create new df which only includes area sums per space type#
cur_proj_sum_df = pd.DataFrame(cur_proj_space_area_sums_list, index=cur_proj_space_list)
#call total area#
cur_proj_area = sum(cur_proj_space_area_sums_list)
print("Total area: " + str(int(cur_proj_area)) + "sf")
#count the floors#
proj_floors = cur_proj_df['floor'].unique()
print("Number of floors: " + str(len(proj_floors)))
#create plot#
cur_proj_sum_df.columns = ['sf']
cur_proj_color_list = []
for x in cur_proj_space_list : 
    cur_proj_color_list.append(space_colors_dict[x])
cur_proj_sum_df.plot.pie(y='sf',colors=cur_proj_color_list)
plt.show()