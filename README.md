# calyx-share-eval
Resource Usage for Calyx designs. 

Currently, I have some bad python scripts (I will improve them). 

I ran these scripts to get some preliminary resource numbers for LeNet, SqueezeNet, and MobileNet (we have only verified correctness of LeNet). The summary folder just extracts the most important information from the results folder. 

To understand what the tables mean: 
"no-infer-share" means running Calyx with the infer share pass disabled. 
"default" means running Calyx normally (i.e., with infer share enabled). 

For these resource estimates, combinational components are never shared. 
"x,y" menas that registers are shared x times and other types of cells are shared y times. -1 means that cells are always shared. 
