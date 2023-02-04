#reference: https://www.geeksforgeeks.org/create-a-grouped-bar-plot-in-matplotlib/

import os 
import sys 
import json 
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import pandas as pd 

sns.set_theme()

supported_designs = ["alex", "google", "lenet", "mobile", "squeeze", "vgg"]
share_bounds = ["1,1", "4,4", "-1,-1"]
share_settings = ["no-infer-share", "default", "fully-inline"]

if __name__ == "__main__":
    assert (len(sys.argv) == 3), "please provide a design name and a resource name"
    assert sys.argv[1] in supported_designs, f"""design must be one of {supported_designs}"""
    design = sys.argv[1] 
    resource_name = sys.argv[2]
    df = pd.read_csv("tables/full-table.csv")
    data = []
    design_setting = df.loc[:, 'setting']
    bound_1 = df.loc[:, f"""{resource_name}_1,1"""]
    bound_4 = df.loc[:, f"""{resource_name}_4,4"""]
    bound_none = df.loc[:, f"""{resource_name}_-1,-1"""]
    for (idx, design_setting) in enumerate(design_setting):
      for share_setting in share_settings:
        if design_setting == f"""{design}_{share_setting}""":
          data.append([share_setting, "1", bound_1[idx]])
          data.append([share_setting, "4", bound_4[idx]])
          data.append([share_setting, "None", bound_none[idx]])
          
    df = pd.DataFrame(data, columns=['share_setting', 'share_bound', 'usage'])
    # Set the figure size
    fig = plt.figure(figsize=(8, 8))
    fig.add_axes([0.1, 0.1, 0.65, 0.85])

    # grouped barplot
    ax = sns.barplot(x="share_setting", y="usage", hue="share_bound", order= share_settings ,data=df, errorbar=None)
    
    ax.set(title=f"""{resource_name} usage on {design}net""")
    
    sns.move_legend(ax, "upper right", bbox_to_anchor=(1.3, 1))
    
    fig.savefig('samplefigure', bbox_inches='tight')
    
    plt.show()
          
           
        
      

    
   
  
    
    
    
    
    
    


