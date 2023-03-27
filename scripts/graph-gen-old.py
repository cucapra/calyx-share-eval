'''
Command line argument: python3 path/to/graph-gen.py <design-name> <resource-name>
See tables/full-table.csv to see the resources/design names supported 
'''

import os 
import sys 
import json 
import matplotlib.pyplot as plt
import matplotlib
import numpy as np 
import seaborn as sns
import pandas as pd 

sns.set_theme()
# font = {'family' : 'sans-serif',
#         'weight' : 'bold',
#         'size'   : 20}

# matplotlib.rc('font', **font)
plt.rcParams['legend.title_fontsize'] = 24

# currently supported settings 
supported_designs = ["alex", "google", "lenet", "mobile", "squeeze", "vgg"]
acronyms = ["vgg", "lut", "dsp"]
bounds = ["1        ", "8       ", "Unbounded"]
compiler_settings = ["No Component Sharing", "Component Sharing", "Fully Inline"]

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

def add_data(data, row, design):
  global bounds 
  data.append([compiler_settings[0], bounds[0], row[1]])
  data.append([compiler_settings[0], bounds[1], row[2]])
  data.append([compiler_settings[0], bounds[2], row[3]])
  data.append([compiler_settings[1], bounds[0], row[4]])
  data.append([compiler_settings[1], bounds[1], row[5]])
  data.append([compiler_settings[1], bounds[2], row[6]])
  data.append([compiler_settings[2], bounds[0], row[7]])
  data.append([compiler_settings[2], bounds[1], row[8]])
  data.append([compiler_settings[2], bounds[2], row[9]])
  
if __name__ == "__main__":
    assert (len(sys.argv) == 3), "please provide a design name and a resource name"
    assert sys.argv[1] in supported_designs, f"""design must be one of {supported_designs}"""
    design = sys.argv[1] 
    resource = sys.argv[2]
    df = pd.read_csv("tables/all-stats-table.csv")
    data = []
    for _,row in df.iterrows():
      design_name = row[0].split("_")[0]
      resource_name = "_".join(row[0].split("_")[1:])
      if design == design_name and resource == resource_name: 
        add_data(data, row, format_design_name(design_name))
        
    
    resource_formatted = format(resource, "_")
          
    df = pd.DataFrame(data, columns=['Compiler Setting', 'Share Bound', f"{resource_formatted} Usage"])
    # Set the figure size
    fig = plt.figure(figsize=(9, 8))
    fig.add_axes([0.1, 0.1, 0.65, 0.85])
    
    # order = compiler_settings,

    # grouped barplot
    ax = sns.barplot(x="Compiler Setting", y=f"""{resource_formatted} Usage""", hue="Share Bound", order = compiler_settings, data=df, errorbar=None)
    
    # ax.set(title=f"""{resource_formatted} Usage on {format_design_name(design)}""")
    legend = False 
    if legend:
      #sns.move_legend(ax, "upper right", bbox_to_anchor=(1.4, 1), fontsize = 24)
      plt.legend(title="Sharing Bound", fontsize=24, bbox_to_anchor=(1.4, 1))
    else:
      plt.legend([],[], frameon=False)
    
    plt.xlabel("Compiler Setting", fontsize = 24)
    plt.ylabel(f"""{resource_formatted} Usage""", fontsize = 24)
    
    
    # can save figure if we want 
    fig.savefig(f"""graphs-bounded-sharing-vert/{format_design_name(design)}_{format(resource, "_")}_usage""", bbox_inches='tight')
    
    plt.show()
          