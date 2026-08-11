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
  msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.ipynb

Scripting
from ipywidgets.embed import embed_minimal_html

embed_minimal_html('export.html', views=[my_vbox], title='Analysis')

file:///Users/saggese/src/umd_classes1/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
works

https://htmlpreview.github.io/?https://github.com/gpsaggese/gpsaggese.github.io/blob/gp_scratch/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
doesn't work

https://raw.githack.com/gpsaggese/gpsaggese.github.io/gp_scratch/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html
works

Serve it as g

One thing worth noting: this repo is gpsaggese.github.io, so it's already a GitHub Pages site. If that file gets merged into the branch Pages is configured to serve (usually main), it'll be live at

How to get also links to the titles

https://raw.githack.com/gpsaggese/gpsaggese.github.io/gp_scratch/msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.html#Cell-1:-Introduction---Casino-Slot-Machines

quarto

### jupyter book

source ~/src/venv/client_venv.jupyter_book2/bin/activate
cd msml610/jupyter_book
jupyter-book start   # http://localhost:3000
or jupyter-book build --html for static output only (no server).

Need the widget to be rendered

It looks better than a bunch of notebooks, has links and it can be rendered on
github

### Extracting the pictures from Notebook

helpers_root/dev_scripts_helpers/notebooks/extract_notebook_images.py \
    --in_notebook_filename msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.ipynb \
    --out_image_dir msml610/tutorials/L09_multi_armed_bandits/screenshots

helpers_root/dev_scripts_helpers/notebooks/extract_notebook_images.py \
    --in_notebook_filename msml610/tutorials/L09_multi_armed_bandits/L09_03_02_multi_armed_bandits.ipynb \
    --out_image_dir msml610/tutorials/L09_multi_armed_bandits/screenshots \
    --extract_all_cells

There is a problem with Docker
- Add the ability to run on host or in a dockerized environment

# Problems

- Link the notebook cells to the slides
- Link the Python code to the notebook cells
- Link the slides to the notebook cells
- Render the notebooks to the web
  - Use jupyter book
  - Render with github
- Add a link back from jupyter book to Jupyter code to run locally
- Extract images from the notebook so they can be inlined in the slides
- Add links to the tutorials
- Add examples in the book with picture and comment (from the slide) and then a
  pointer to the Jupyter tutorial / Jupyter book (e.g., L03.04.05)
