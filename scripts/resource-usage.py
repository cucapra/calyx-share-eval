import shutil 
import os 
import json 
import sys 
import subprocess 
import time 
'''
Reads in a JSON and runs resource estimates. 
I also tried to get it to write the error message, commands run, and time taken, 
into .txt files, but it doesn't work currently since I am just overwriting 
what was previously in the file each time I try to write. 
However, the resource usage runs correctly. 
The json input needs: 
"files": list of files 
"bounds": list of bounds. 
"settings": list of settings 
"output-dir": the output directory 
"synth-file": the synthesis file 
'''

settings_supported = ["no-infer-share", "default"]

def write_to_file(file_dest, s):
  '''
  writes s to file_dest
  '''
  with open(file_dest, "w") as fd:
    fd.write(s)

def run_command(command, commands_file):
  '''
  runs command on terminal, and writes to file 
  '''
  try: 
    output = subprocess.check_output(command, shell=True)
    write_to_file(commands_file, command + "\n")
  except subprocess.CalledProcessError as exc:
    error_str = "Status : FAIL " + str(exc.returncode) + " "+ str(exc.output)
    write_to_file(errors_file,error_str)

if __name__ == "__main__":
  assert (len(sys.argv) == 2), "please provide an input json file name"

  # reading the json file 
  json_data = json.load(open(sys.argv[1]))
  files = json_data["files"] 
  bounds = json_data["bounds"]
  settings = json_data["settings"]
  output_dir = json_data["output-dir"]
  synth_file = json_data["synth-file"]

  # setting the synth file flag for when we do fud commands 
  synth_file_flag = f"-s synth-verilog.tcl {synth_file}"

  # making the output directory that stores our results 
  # if it already exists then overwrite 
  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir)
  resource_files_path = os.path.join(output_dir, "resource-estimates")
  os.makedirs(resource_files_path)
  timing_file = os.path.join(output_dir, "time.txt")
  commands_file = os.path.join(output_dir, "commands_run.txt")
  errors_file = os.path.join(output_dir, "errors.txt")

  for f in files:
    start = time.time() 
    big_json = {}
    for s in settings:
      assert s in settings_supported, f"setting is not supported. Must be one of {settings_supported}"
      settings_flag = ""
      if s == "no-infer-share":
        settings_flag = '-d infer-share'   
      big_json[s] = {}
      for b in bounds:
        futil_flags = f'-s futil.flags "{settings_flag} -x cell-share:bounds=1,{b},{b}"'
        run_info = f.replace(".","_") + "_" + str(b) + "_" + s
        synth_files_directory = os.path.join(output_dir,run_info) 
        resource_estimates_file = os.path.join(resource_files_path, run_info + ".json")

        # first get synth_files (they can be helpful to look at)
        run_command(f"fud e --to synth-files {f} -o {synth_files_directory} {synth_file_flag} {futil_flags}", commands_file)
        
        # next get resource estimates from synth files 
        run_command(f"fud e --to resource-estimate --from synth-files {synth_files_directory} > {resource_estimates_file}", commands_file)

        # loading the data we just got and putting into one big json file. 
        # So for each neural network (e.g., LeNet) we have a big json with 
        # all the data we want in it 
        json_data = json.load(open(resource_estimates_file))
        big_json[s][f"{b},{b}"] = json_data

    full_resource_file = os.path.join(output_dir,"resource_numbers_" + f + ".json")
    write_to_file(full_resource_file, json.dumps(big_json))
    
    end = time.time()
    time_consumed=end-start
    write_to_file(timing_file, str(time_consumed) + "\n")


        





  

        