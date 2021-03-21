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
FABULAE_LAT_MARK = '%{fabulae_latinae}%'
FABULAE_GR_MARK = '%{fabulae_graecae}%'
OUT_DIR = 'out'
OUT_FILE = f'{OUT_DIR}/FābulaeFranciscī.tex'
BUILD_COMMAND = 'xelatex -interaction=nonstopmode %s'

#---------- PROCEDURES ----------#

def is_greek(s: str):
    n = [0, 0]
    for c in s:
        if c in "ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω":
            n[0] += 1
        else:
            n[1] += 1

    assert n[0] + n[1] == len(s)

    return n[0] / n[1] >= 1

def get_title(title: str):
    return title.upper().replace('Ā', 'A').replace('Ē', 'E').replace('Ī', 'I').replace('Ō', 'O').replace('Ū', 'U')

def format_md_to_tex(mdtext):
    textext = ''
    for line in mdtext.splitlines(False):
        if line.startswith('#'):
            title = line.replace('# ', '')
            #if not is_greek(title):
            #    title = f"\\textbf{{{title}}}"
            textext += f"\\section{{{title}}}"
            textext += "\n\n"
        elif line.startswith('>'):
            textext += "\\begin{otherlanguage}{polytonicgreek}\n"
            textext += line.replace('> ', '') + '\n'
            textext += "\\end{otherlanguage}\n\n"
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
    
    latine_fabulae = filter(lambda kv: not is_greek(kv[0]), fabulae)
    graece_fabulae = filter(lambda kv: is_greek(kv[0]), fabulae)

    latine_fabulae = '\n\n\n'.join(map(lambda t: t[1], latine_fabulae))
    graece_fabulae = '\n\n\n'.join(map(lambda t: t[1], graece_fabulae))

    try:
        os.mkdir(OUT_DIR)
    except:
        pass
    
    with open(OUT_FILE, 'w') as f:
        content = template.replace(FABULAE_LAT_MARK, latine_fabulae).replace(FABULAE_GR_MARK, graece_fabulae)
        print(f, content)

    exit(os.system(BUILD_COMMAND % OUT_FILE))

if __name__ == '__main__':
    main(argv)
