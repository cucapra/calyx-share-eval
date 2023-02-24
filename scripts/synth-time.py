import time
import os 
import sys 

''' 
Short script that times how long it takes to turn a .futil file into synth files 
Mostly used to get an estimate of how long things will take when we try to 
get resource numbers. 
Run scripts/synth-time.py <input.futil>, and we it will write into a txt file 
recording how many seconds it took to get the synth files. 
'''

start = time.time() 

assert (len(sys.argv) == 2), "please provide an input futil file name"

futil_file = sys.argv[1]

file_id = futil_file.replace("/", "_").replace(".","_")

os.system(f"""fud e --to synth-files {futil_file} -o {file_id} -s synth-verilog.tcl synth.tcl""")

end = time.time()
time_consumed=end-start

with open(f"""{file_id}-time.txt""", "w") as file:
    file.writelines(str(time_consumed))
