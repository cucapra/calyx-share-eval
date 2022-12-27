#reference: https://www.geeksforgeeks.org/create-a-grouped-bar-plot-in-matplotlib/

import os 
import sys 
import json 
import matplotlib.pyplot as plt
import numpy as np 

supported_designs = ["alex", "google", "lenet", "mobile", "squeeze", "vgg"]
sharing_bounds = ["1,1", "4,4", "-1,-1"]
sharing_settings = ["no-infer-share", "default", "fully-inline"]

if __name__ == "__main__":
    assert (len(sys.argv) == 3), "please provide a design name and a resource name"
    assert sys.argv[1] in supported_designs, f"""design must be one of {supported_designs}"""
    design = sys.argv[1] 
    resource_name = sys.argv[2]
    file_path = os.path.join("results", design, f"""resource_numbers_{design}.json""") 
    json_data = json.load(open(file_path))
    graph_data = []
    for bound in sharing_bounds:
      bound_data = []
      for setting in sharing_settings:
        bound_data.append(json_data[setting][bound][resource_name])
      graph_data.append(bound_data)
      
    x = np.arange(len(sharing_settings))
    bound_one = graph_data[0]
    bound_four = graph_data[1]
    bound_none = graph_data[2]
    width = 0.2
  
    # plot data in grouped manner of bar type
    plt.bar(x-0.2, bound_one, width, color='cyan')
    plt.bar(x, bound_four, width, color='orange')
    plt.bar(x+0.2, bound_none, width, color='green')
    plt.xticks(x, sharing_settings)
    plt.xlabel("Setting")
    plt.ylabel("Resource Usage")
    plt.legend(["Bound 1", "Bound 4", "No Bound"])
    plt.show()

    
   
  
    
    
    
    
    
    


