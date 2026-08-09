vi msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt msml610/lectures_source/Lesson09.7-Advanced_Bandits.txt

msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandits.md

### [x] Extract the classes from
msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandits_utils.py
that don't start with cell_... into
msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandits_sim.py

### [x] Rename

msml610/tutorials/L09_multi_armed_bandits/L09_multi_armed_bandits.01.API.simulation_classes.ipynb
msml610/tutorials/L09_multi_armed_bandits/L09_multi_armed_bandits.01.API.simulation_classes.py

-> 
msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandit_sim_API.ipynb
msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandit_sim_API.py

Update all the references

### [x] Compare the notebook outline from
msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandits.md
with the text in
msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt

For each slide, add a reference to the slides in the txt file associated to those
concepts, e.g.,
// msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt:"..."

### [x] Complete the tutorial

### [x] lint the files

### [x] Rename

msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandit_sim_API.{ipynb,py}
->
msml610/tutorials/L09_multi_armed_bandits/L09_03_01_multi_armed_bandits_sim_API.{ipynb,py}

msml610/tutorials/L09_multi_armed_bandits/L09_03_multi_armed_bandits.{ipynb,py}
->
msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.{ipynb,py}

### [ ] Add tutorial using packages


### 

is it possible to create a notebook ipynb using pywidgets to html so that the static parts work

Settings → Save Widget State Automatically), re-run all cells

> jupyter nbconvert --to html msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.ipynb

jupyter nbconvert --to html --template html_anchorfix \
  --TemplateExporter.extra_template_basedirs=<repo>/helpers_root/dev_scripts_helpers/notebooks/nbconvert_templates \
  <notebook>.ipynb

file:///Users/saggese/src/umd_classes1/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
works

https://htmlpreview.github.io/?https://github.com/gpsaggese/gpsaggese.github.io/blob/gp_scratch/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
doesn't work

https://raw.githack.com/gpsaggese/gpsaggese.github.io/gp_scratch/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
works

Serve it as g

One thing worth noting: this repo is gpsaggese.github.io, so it's already a GitHub Pages site. If that file gets merged into the branch Pages is configured to serve (usually main), it'll be live at

How to get also links to the titles
