'''
Command line argument: python3 path/to/graph-gen.py <resource-name>

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
share_settings = ["no-infer-share", "default", "fully-inline"]
acronyms = ["vgg", "lut", "dsp"]
bounds = [1,8,32,128,-1]

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
  s_list = s.split(space_replacement)
  final_list = [format_word(s) for s in s_list]
  return " ".join(final_list)

def add_data(data, row):
  count = 0
  for add_bound in bounds:
    for reg_bound in bounds:
      data.append([add_bound, reg_bound, row[count+1]])
      count += 1
  
if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide a resource name"
    resource_name = sys.argv[1]
    df = pd.read_csv("synth-exp-tables/no-const-table.csv")
    data = []
    for _,row in df.iterrows():
      if resource_name in row[0]:
        add_data(data, row)
        
    print(data)
    
    
    df = pd.DataFrame(data, columns=['Adder Bound', 'Register Bound', 'Usage'])
    # Set the figure size
    fig = plt.figure(figsize=(8, 8))
    fig.add_axes([0.1, 0.1, 0.65, 0.85])
    
    #order = ["No Sharing", "Share Registers and Combinational", "Share All Primitives", "Share All Components", "Fully Inline and Share"]

    # grouped barplot
    ax = sns.barplot(x="Register Bound", y="Usage", hue="Adder Bound", data=df, errorbar=None, order = bounds, hue_order = bounds)
    
    ax.set(title=f"""{format(resource_name, "_")} Usage""")
    
    sns.move_legend(ax, "upper right", bbox_to_anchor=(1.3, 1))
    
    # if not os.path.exists("graphs"):
      # os.makedirs("graphs") 
    # can save figure if we want 
    # fig.savefig(f"""graphs/{format(resource_name, "_")}_usage""", bbox_inches='tight')
    
    plt.show()
    
          
           
        
      

    
   
  
    
    
    
    
    
    


