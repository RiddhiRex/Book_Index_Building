import re
import subprocess


def index_gen(predicted_indices,input_file,output_file):
  #add \usepackage{makeidx}  \makeindex in the preamble
  #add \printindex at the end. This is where the list will be placed.

  #Steps for generating the latex source
  #latex filename.tex
  #makeindex filename


  with open(input_file) as f:
      data = f.read()
      for word in predicted_indices:
          data = re.sub(r'\b%s\b'%(word),'%s\index{%s}'%(word,word),data)

  with open(output_file,"w") as f:
      f.write(data)

  process = subprocess.Popen(["latex", output_file], stdout=subprocess.PIPE)
  process = subprocess.Popen(["makeindex",output_file.replace('.tex','')],stdout=subprocess.PIPE)
  process = subprocess.Popen(["latex", output_file], stdout=subprocess.PIPE)
  
