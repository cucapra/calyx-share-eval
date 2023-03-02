'''
Command line argument: python3 path/to/graph-gen.py <design-name> <resource-name>

See tables/full-table.csv to see the resources/design names supported 
'''

import os 
import sys 
import json 
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import pandas as pd 

sns.set_theme()

# currently supported settings 
supported_designs = ["alex", "google", "lenet", "mobile", "squeeze", "vgg"]
share_bounds = ["1,1", "4,4", "-1,-1"]
share_settings = ["no-infer-share", "default", "fully-inline"]
acronyms = ["vgg", "lut", "dsp"]

def format_word(s):
  '''
  if s in acronyms, capitalize everyting. 
  else just capitalize first letter. 
  '''
  if s in acronyms:
    return s.upper()
  else:
    return s.capitalize()

def format_design_name(s):
  if s not in acronyms:
    return f"""{s.capitalize()}Net"""
  else:
    return s.upper()

def format(s, space_replacement):
  '''
  replace space_replacement with space, then format each word according to format_word()
  '''
  s_list = s.split("-")
  final_list = [format_word(s) for s in s_list]
  return " ".join(final_list)
  
if __name__ == "__main__":
    assert (len(sys.argv) == 3), "please provide a design name and a resource name"
    assert sys.argv[1] in supported_designs, f"""design must be one of {supported_designs}"""
    design = sys.argv[1] 
    resource_name = sys.argv[2]
    df = pd.read_csv("tables/full-table.csv")
    data = []
    design_setting = df.loc[:, 'design/compiler setting']
    bound_1 = df.loc[:, f"""{resource_name}_1,1"""]
    bound_4 = df.loc[:, f"""{resource_name}_4,4"""]
    bound_none = df.loc[:, f"""{resource_name}_-1,-1"""]
    for (idx, design_setting) in enumerate(design_setting):
      for share_setting in share_settings:
        if design_setting == f"""{design}_{share_setting}""":
          data.append([format(share_setting, "-"), "1", bound_1[idx]])
          data.append([format(share_setting, "-"), "4", bound_4[idx]])
          data.append([format(share_setting, "-"), "None", bound_none[idx]])
    
    df_calyx2020 = pd.read_csv("tables/full-table-calyx2020.csv")
    designs = df_calyx2020.loc[:, "design"]
    resrc_data = df_calyx2020.loc[:, f"""{resource_name}"""]
    for (idx, dsgn) in enumerate(designs):
      if dsgn == f"""{design}""":
        data.append(['No Infer Share', 'Calyx 2020', resrc_data[idx]])
          
    df = pd.DataFrame(data, columns=['Compiler Setting', 'Share Bound', 'Usage'])
    # Set the figure size
    fig = plt.figure(figsize=(8, 8))
    fig.add_axes([0.1, 0.1, 0.65, 0.85])
    
    formatted_share_setting = [format(s, "-") for s in share_settings]

    # grouped barplot
    ax = sns.barplot(x="Compiler Setting", y="Usage", hue="Share Bound", order = formatted_share_setting, data=df, errorbar=None)
    
    ax.set(title=f"""{format(resource_name, "_")} Usage on {format_design_name(design)}""")
    
    sns.move_legend(ax, "upper right", bbox_to_anchor=(1.3, 1))
    
    # can save figure if we want 
    # fig.savefig('resource_graph', bbox_inches='tight')
    
    plt.show()
          
           
        
      

    
   
  
    
    
    
    
    
    


