'''
Reads in a JSON and runs resource estimates. 
Also, records the commnands run in the terminal, as well as an "errors" file 
that tells you any errors that occured, and whether each simulation meets timing. 
The json input needs: 
"files": .futil file to estimate resource for 
"compiler_settings": the compiler settings. should be: [setting, [bound1, bound2, bound3]]
setting should be "fully-inline", "default", or "no-infer-share"
"output-dir": the output directory 
"synth-file": the synthesis file 
"device": the device to run 
'''

import shutil 
import os 
import json 
import sys 
import subprocess 
import time 
from resource_usage import simplify_file_name, write_to_file, run_command

settings_supported = ["no-infer-share", "default", "fully-inline"]
    
def run_simulation(file, input_data, compiler_settings, simulation_results, commands_file, errors_file):
  for compiler_setting in compiler_settings:
    start = time.time()
    # setting should be one of the settings_supported = ["default", "fully-inline", "no-infer-share"]
    setting = compiler_setting[0]
    assert setting in settings_supported, f"setting is not supported. Must be one of {settings_supported}"
    # group2invoke can use unnecessary registers 
    # tdst is not yet fully implemented 
    settings_flag = " -d group2invoke -d tdst "
    if setting == "no-infer-share":
      settings_flag += ' -d infer-share' 
    elif setting == "fully-inline":
      settings_flag += ' -x inline:always -x inline:new-fsms' 
    # bounds should be a 3 element list of bounds, e.g. [1,4,4]
    bounds = compiler_setting[1]
      
    futil_flags = f'-s futil.flags "{settings_flag} -x cell-share:bounds={bounds[0]},{bounds[1]},{bounds[2]}"'
    run_info = simplify_file_name(file) + "_" + setting + "_" + f"{bounds[0]}_{bounds[1]}_{bounds[2]}" 
    
    results_file = os.path.join(simulation_results, run_info + ".json")
            
    # first get synth_files (they can be helpful to look at)
    run_command(f"fud e {file} -s verilog.data {input_data} --to dat --through verilog -v -o {results_file}", commands_file, errors_file)  
    
    end = time.time()
    time_consumed=end-start
    time_str = run_info + ": " + str(time_consumed/60) + " minutes"
    write_to_file(timing_file, time_str)

if __name__ == "__main__":
  assert (len(sys.argv) == 2), "please provide an input json file name"

  # reading the json file 
  json_data = json.load(open(sys.argv[1]))
  file = json_data["file"] 
  compiler_settings = json_data["compiler-settings"]
  results_path = json_data["results-path"]
  input_data = json_data["input-data"]

  # making the output directory that stores our results 
  # (if it already exists then overwrite)
  if os.path.exists(results_path):
    shutil.rmtree(results_path)
  os.makedirs(results_path)
  
  # timing file keeps of how long each simulation takes 
  timing_file = os.path.join(results_path, "simulation-time.txt")
  # commands file is just a list of the commands that we ran in the terminal 
  # this is mostly helpful for debugging purposes
  commands_file = os.path.join(results_path, "simulation-commands.txt")
  # errors file stores any errors found while executing command line, including 
  # whether timing is met 
  errors_file = os.path.join(results_path, "simulation-errors.txt")
  
  simulation_results = os.path.join(results_path, "sim-results")
  os.makedirs(simulation_results)
  
  run_simulation(file, input_data, compiler_settings, simulation_results, commands_file, errors_file)