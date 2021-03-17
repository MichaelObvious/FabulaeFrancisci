import os
from sys import argv, stdout, stderr, exit

#---------- TOOLBOX ----------#

def print(stream, content):
    stream.write(str(content))

def println(stream, content):
    print(stream, f'{content}\n')

def slurp_file(filepath):
    content = ""
    with open(filepath) as f:
        content = f.read()
    return content

#---------- CONSTANTS ----------#

TEMPLATE_FILE = 'book-template.tex'
FABULAE_DIR = 'fabulae'
FABULAE_MARK = '%{fabulae}%'
OUT_DIR = 'out'
OUT_FILE = f'{OUT_DIR}/FābulaeFranciscī.tex'
BUILD_COMMAND = 'xelatex -interaction=nonstopmode %s'

#---------- PROCEDURES ----------#

def get_title(title):
    return title.upper().replace('Ā', 'A').replace('Ē', 'E').replace('Ī', 'I').replace('Ō', 'O').replace('Ū', 'U')

def format_md_to_tex(mdtext):
    textext = ''
    for line in mdtext.splitlines(False):
        if line.startswith('#'):
            textext += f"\\section{{{line.replace('# ', '')}}}\n\n"
        elif line.startswith('>'):
            textext += "\\begin{otherlanguage}{polytonicgreek}" + f"{line.replace('> ', '')}" + "\\end{otherlanguage}\n\n"
        else:
            textext += f'{line}\n'

    #textext = textext.replace('⟨', '\\leftangle ').replace('⟩', '\\rightangle ')
    return textext

def slurp_fabulae():
    fabulae_files = os.listdir(FABULAE_DIR)
    fabulae = {}
    
    for ff in fabulae_files:
        if ff.endswith('.md'):
            ffpath = f'{FABULAE_DIR}/{ff}'
            fabulae[ff.replace('.md', '')] = format_md_to_tex(slurp_file(ffpath))
    return fabulae

#---------- MAIN ----------#

def main(args):
    template = slurp_file(TEMPLATE_FILE)

    fabulae = slurp_fabulae()
    fabulae = sorted(fabulae.items(), key=lambda kv: get_title(kv[0]))

    try:
        os.mkdir(OUT_DIR)
    except:
        pass
    
    with open(OUT_FILE, 'w') as f:
        content = template.replace(FABULAE_MARK, '\n\n\n'.join(map(lambda t: t[1], fabulae)))
        print(f, content)

    exit(os.system(BUILD_COMMAND % OUT_FILE))

if __name__ == '__main__':
    main(argv)
