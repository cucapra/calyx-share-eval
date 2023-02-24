'''
Reads in a JSON and runs resource estimates. 
Also, records the commnands run in the terminal, as well as an "errors" file 
that tells you any errors that occured, and whether each simulation meets timing. 
The json input needs: 
"files": list of files 
"bounds": list of bounds. 
"settings": list of settings 
"output-dir": the output directory 
"synth-file": the synthesis file 
'''

import shutil 
import os 
import json 
import sys 
import subprocess 
import time 

supported_files = ["google", "lenet", "alex", "squeeze", "vgg", "mobile"]
settings_supported = ["no-infer-share", "default", "fully-inline"]

def simplify_file_name(old_file_name):
  '''
  renames compilcated file names for nn designs to simpler ones. 
  e.g. "nn-designs_alex_futil" -> "alex"
  '''
  for possible_new_name in supported_files:
    if possible_new_name in old_file_name:
      return possible_new_name 
  return old_file_name.replace("/","_").replace(".", "_") 

def write_to_file(file_dest, s):
  '''
  writes string s to file_dest
  '''
  with open(file_dest, "a") as fd:
    fd.write(s)
    fd.write("\n")

def run_command(command, commands_file):
  '''
  runs command on terminal, and writes the command it ran to file 
  '''
  try: 
    write_to_file(commands_file, command + "\n")
    subprocess.check_output(command, shell=True)
  except subprocess.CalledProcessError as exc:
    error_str = "Status : FAIL " + str(exc.returncode) + " "+ str(exc.output)
    write_to_file(errors_file, error_str)

def run_synthesis(files, settings, bounds, output_dir, synth_file_flag, device_flag):
  # f is the futil file that we run resource estimations on. 
  for f in files:
    # big_json is a json that stores all of the resource estimates for this design 
    big_json = {}
    for s in settings:
      assert s in settings_supported, f"setting is not supported. Must be one of {settings_supported}"
      settings_flag = ""
      if s == "no-infer-share":
        settings_flag = '-d infer-share' 
      elif s == "fully-inline":
        settings_flag = '-x inline:always -x inline:new-fsms  -d group2invoke -d tdst' 
      big_json[s] = {}
      for b in bounds:
        start = time.time() 
        futil_flags = f'-s futil.flags "{settings_flag} -x cell-share:bounds=1,{b},{b}"'
        run_info = simplify_file_name(f) + "_" + str(b) + "_" + s
        # where to put the full synth-files directory 
        synth_files_directory = os.path.join(output_dir,run_info) 
        # where to put the resource estimates json 
        resource_estimates_file = os.path.join(resource_files_path, run_info + ".json")

        # first get synth_files (they can be helpful to look at)
        run_command(f"fud e --to synth-files {f} -o {synth_files_directory} {synth_file_flag} {device_flag} {futil_flags}", commands_file)
        
        # next get resource estimates from synth files 
        run_command(f"fud e --to resource-estimate --from synth-files {synth_files_directory} > {resource_estimates_file}", commands_file)

        # loading the data we just got and putting into one big json file. 
        # So for each neural network (e.g., LeNet) we have a big json with 
        # all the data we want in it 
        json_data = json.load(open(resource_estimates_file))
        big_json[s][f"{b},{b}"] = json_data
        if json_data["meet_timing"] != 1:
          write_to_file(errors_file,f"""{run_info} does not meet timing""")
        
        end = time.time()
        time_consumed=end-start
        time_str = run_info + ": " + str(time_consumed/60) + " minutes"
        write_to_file(timing_file, time_str)
    
    full_resource_file = os.path.join(output_dir,"resource_numbers_" + simplify_file_name(f) + ".json")
    write_to_file(full_resource_file, json.dumps(big_json))

if __name__ == "__main__":
  assert (len(sys.argv) == 2), "please provide an input json file name"

  # reading the json file 
  json_data = json.load(open(sys.argv[1]))
  files = json_data["files"] 
  bounds = json_data["bounds"]
  settings = json_data["settings"]
  output_dir = json_data["output-dir"]
  synth_file = json_data["synth-file"]
  device_file = json_data["device"]

  # setting the synth file flag for when we do fud commands 
  synth_file_flag = f"-s synth-verilog.tcl {synth_file}"
  device_flag = f"-s synth-verilog.constraints {device_file}"

  # making the output directory that stores our results 
  # (if it already exists then overwrite)
  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir)
  resource_files_path = os.path.join(output_dir, "resource-estimates")
  os.makedirs(resource_files_path)
  
  # timing file keeps of how long each simulation takes 
  timing_file = os.path.join(output_dir, "time.txt")
  # commands file is just a list of the commands that we ran in the terminal 
  # this is mostly helpful for debugging purposes
  commands_file = os.path.join(output_dir, "commands_run.txt")
  # errors file stores any errors found while executing command line, including 
  # whether timing is met 
  errors_file = os.path.join(output_dir, "errors.txt")
  
  run_synthesis(files, settings, bounds, output_dir, synth_file_flag, device_flag)