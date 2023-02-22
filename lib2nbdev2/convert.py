# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_convert.ipynb.

# %% auto 0
__all__ = ['export_names', 'code_cell', 'nbglob', 'write_module_cell', 'init_nb', 'write_cell', 'write_nb', 'convert_lib']

# %% ../nbs/00_convert.ipynb 3
import json
import os

from fastcore.basics import Path
from fastcore.xtras import is_listy
from fastcore.foundation import Config
from fastcore.script import call_parse

from fastprogress.fastprogress import progress_bar

# from nbdev.export import nbglob, export_names, _re_class_func_def, _re_obj_def
# from nbdev.sync import _split
from nbdev.config import *
from .generators import generate_ci, generate_doc_foundations, generate_setup
from fastcore.all import *

# %% ../nbs/00_convert.ipynb 5
_re_class_func_def = re.compile(r"""
# Catches any 0-indented function or class definition with its name in group 1
^              # Beginning of a line (since re.MULTILINE is passed)
(?:async\sdef|def|class)  # Non-catching group for def or class
\s+            # One whitespace or more
([^\(\s]+)     # Catching group with any character except an opening parenthesis or a whitespace (name)
\s*            # Any number of whitespace
(?:\(|:)       # Non-catching group with either an opening parenthesis or a : (classes don't need ())
""", re.MULTILINE | re.VERBOSE)

# %% ../nbs/00_convert.ipynb 6
_re_obj_def = re.compile(r"""
# Catches any 0-indented object definition (bla = thing) with its name in group 1
^                          # Beginning of a line (since re.MULTILINE is passed)
([_a-zA-Z]+[a-zA-Z0-9_\.]*)  # Catch a group which is a valid python variable name
\s*                        # Any number of whitespace
(?::\s*\S.*|)=  # Non-catching group of either a colon followed by a type annotation, or nothing; followed by an =
""", re.MULTILINE | re.VERBOSE)

# %% ../nbs/00_convert.ipynb 7
_re_class_func_def = re.compile(r"""
# Catches any 0-indented function or class definition with its name in group 1
^              # Beginning of a line (since re.MULTILINE is passed)
(?:async\sdef|def|class)  # Non-catching group for def or class
\s+            # One whitespace or more
([^\(\s]+)     # Catching group with any character except an opening parenthesis or a whitespace (name)
\s*            # Any number of whitespace
(?:\(|:)       # Non-catching group with either an opening parenthesis or a : (classes don't need ())
""", re.MULTILINE | re.VERBOSE)

# %% ../nbs/00_convert.ipynb 8
_re_cell = re.compile(r'^# Cell|^# Internal Cell|^# Comes from\s+(\S+), cell')

# %% ../nbs/00_convert.ipynb 9
def _split(code):
    lines = code.split('\n')
    nbs_path = get_config().path("nbs_path").relative_to(get_config().config_file.parent)
    prefix = '' if nbs_path == Path('.') else f'{nbs_path}/'
    default_nb = re.search(f'File to edit: {prefix}(\S+)\s+', lines[0]).groups()[0]
    s,res = 1,[]
    while _re_cell.search(lines[s]) is None: s += 1
    e = s+1
    while e < len(lines):
        while e < len(lines) and _re_cell.search(lines[e]) is None: e += 1
        grps = _re_cell.search(lines[s]).groups()
        nb = grps[0] or default_nb
        content = lines[s+1:e]
        while len(content) > 1 and content[-1] == '': content = content[:-1]
        res.append((nb, '\n'.join(content)))
        s,e = e,e+1
    return res
     

# %% ../nbs/00_convert.ipynb 11
def export_names(code, func_only=False):
    "Find the names of the objects, functions or classes defined in `code` that are exported."
    #Format monkey-patches with @patch
    def _f(gps):
        nm, cls, t = gps.groups()
        if cls is not None: return f"def {cls}.{nm}():"
        return '\n'.join([f"def {c}.{nm}():" for c in re.split(', *', t[1:-1])])

# %% ../nbs/00_convert.ipynb 12
def code_cell(code:str=None) -> str:
    """
    Returns a Jupyter cell with potential `code`
    """
    cell = {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
    "source": []
    }
    if is_listy(code): 
        for i, c in enumerate(code):
            if i < len(code)-1:
                cell["source"].append(c+'\n')
            else:
                cell["source"].append(c)
    elif code: cell["source"].append(code)
    return cell

# %% ../nbs/00_convert.ipynb 13
def nbglob(fname=None, recursive=None, extension='.ipynb', config_key='nbs_path') -> L:
    "Find all files in a directory matching an extension given a `config_key`."
    print('Running NBGlob')
    fname = Path(fname or get_config().path(config_key))
    print('fname', fname)
    if fname.is_file(): return [fname]
    if recursive == None: recursive=get_config().get('recursive', 'False').lower() == 'true'
    if fname.is_dir(): pat = f'**/*{extension}' if recursive else f'*{extension}'
    else: fname,_,pat = str(fname).rpartition(os.path.sep)
    if str(fname).endswith('**'): fname,pat = fname[:-2],'**/'+pat
    fls = L(Path(fname).glob(pat)).map(Path)
    return fls.filter(lambda x: x.name[0]!='_' and '/.' not in str(x))

# %% ../nbs/00_convert.ipynb 16
def write_module_cell() -> str:
    """
    Writes a template `Markdown` cell for the title and description of a notebook
    """
    return {
   "cell_type": "markdown",
   "metadata": {},
    "source": [
        "# Default Title (change me)\n", 
        "> Default description (change me)"
    ]
    }

# %% ../nbs/00_convert.ipynb 17
def init_nb(module_name:str) -> str:
    """
    Initializes a complete blank notebook based on `module_name`

    Also writes the first #| default_exp cell and checks for a nested module (moduleA.moduleB)
    """
    if module_name[0] == '.': module_name = module_name.split('.')[1]
    if '.ipynb' in module_name: module_name = module_name.split('.ipynb')[0]
        
    return {"cells":[code_cell(f"#| default_exp {module_name}"), write_module_cell()], 
            "metadata":{
                "jupytext":{"split_at_heading":True},
                "kernelspec":{"display_name":"Python 3", "language": "python", "name": "python3"}
            },
           
           "nbformat":4,
           "nbformat_minor":4}

# %% ../nbs/00_convert.ipynb 19
def write_cell(code:str, is_public:bool=False) -> str:
    """
    Takes source `code`, adds an initial `#| export` or `#| exporti` tag, and writes a Jupyter cell
    """
    if is_public is None: export = ''
    export = '#| export' if is_public else '#| exporti'
    source = [f"{export}"] + code.split("\n")
    return code_cell(source)

# %% ../nbs/00_convert.ipynb 21
def write_nb(cfg_path:str, cfg_name:str, splits:list, num:int, parent:str=None, private_list:list=[]) -> str:
    """
    Writes a fully converted Jupyter Notebook based on `splits` and saves it in `Config`'s `nbs_path`.

    The notebook number is based on `num`

    `parent` denotes if the current notebook module is based on a parent module
    such as `moduleA.moduleB`
    
    `private_list` is a by-cell list of `True`/`False` for each block of code of whether it is private or public
    """
    # Get filename
    fname = splits[0][0]
    if fname[0] == '.': fname = fname[1:]
    if parent is not None: fname = f'{parent}.{fname}'
    print(splits)
    print(private_list)
    # Initialize and write notebook
    nb = init_nb(fname)
    for i, (_, code) in enumerate(splits):
        c = write_cell(code, private_list[i])
        nb["cells"].append(c)

    # Figure out the notebook number
    if num < 10:
        fname = f'0{num}_{fname}'
    else:
        fname = f'{num}_{fname}'

    # Save notebook in `nbs_path`
    with open(f'{Config(cfg_path, cfg_name).path("nbs_path")/fname}', 'w+') as source_nb:
        source_nb.write(json.dumps(nb))

# %% ../nbs/00_convert.ipynb 22
def _not_private(n):
    "Checks if a func is private or not, alternative to nbdev's"
    for t in n.split('.'):
        if (t.startswith('_') and not t.startswith('__')): return False
    return '\\' not in t and '^' not in t and t != 'else'

# %% ../nbs/00_convert.ipynb 24
@call_parse
def convert_lib():
    """
    Converts existing library to an nbdev one by autogenerating notebooks.
    
    Optional prerequisites:
      - Make a nbdev settings.ini file beforehand
      - Optionally you can add `# Cell` and `# Internal Cell` tags in the source files where you 
        would like specific cells to be
    
    Run this command in the base of your repo
    
    **Can only be run once**
    """
    print('Checking for a settings.ini...')
    cfg_path, cfg_name = '.', 'settings.ini'
    if not Path(cfg_name).exists():
        nbdev_create_config()
    # generate_settings()
    print('Gathering files...')
    files = nbglob(extension='.py', config_key='lib_path', recursive=True)
    print(f'Gathered files {files}')
    if len(files) == 0: 
        raise ValueError("No files were found, please ensure that `lib_path` is configured properly in `settings.ini`")
    print(f'{len(files)} modules found in the library')
    num_nbs = len(files)
    
    nb_path = Config(cfg_path, cfg_name).path('nbs_path')
    nb_path.mkdir(exist_ok=True)
    print(f'Writing notebooks to {nb_path}...')
    if nb_path.name == Config(cfg_path, cfg_name).lib_name:
        nb_path = Path('')
        slash = ''
        
    else:
        nb_path = Path(nb_path.name)
        slash = '/'

    for num, file in enumerate(progress_bar(files)):
        if (file.parent.name != Config(cfg_path, cfg_name).lib_name) and slash is not None:
            parent = file.parent.name
        else:
            parent = None
        fname = file.name.split('.py')[0] + '.ipynb'
        if fname[0] == '.': fname = fname[1:]
        # Initial string in the .py
        init_str = f"# AUTOGENERATED! DO NOT EDIT! File to edit: {nb_path}{slash}{fname} (unless otherwise specified).\n\n# Cell\n"

        # Override existing code to include nbdev magic and one code cell
        with open(file, encoding='utf8') as f: code = f.read()

        if "AUTOGENERATED" not in code:
            code = init_str + code

        # Check to ensure we haven't tried exporting once yet
        if "# Cell" and "# Internal Cell" not in code and '__all__' not in code:
            split_code = code.split('\n')
            private_list = [True]
            _do_pass, _private, _public = False, '# Internal Cell\n', '# Cell\n'
            for row, line in enumerate(split_code):
                if _do_pass: _do_pass = False; continue
                # Deal with decorators
                if '@' in line:
                    code = split_code[row+1]
                    if code[:4] == 'def ': code = code[4:]
                    if 'patch' in line or 'typedispatch' in line or not line[0].isspace():
                        is_private = _not_private(code.split('(')[0])
                        private_list.append(is_private)
                        split_code[row] = f'{_public}{line}' if is_private else f'{_private}{line}'
                    _do_pass = True
                # Deal with objects
                elif _re_obj_def.match(line) and not _do_pass:
                    is_private = _not_private(line.split('(')[0])
                    private_list.append(is_private)
                    split_code[row] = f'{_public}{line}' if is_private else f'{_private}{line}'
                # Deal with classes or functions
                elif _re_class_func_def.match(line) and not _do_pass:
                    is_private = _not_private(line.split(' ')[1].split('(')[0])
                    private_list.append(is_private)
                    split_code[row] = f'{_public}{line}' if is_private else f'{_private}{line}'

            code = '\n'.join(split_code)
        
            # Write to file
            with open(file, 'w', encoding='utf8') as f: f.write(code)

            # Build notebooks
            splits = _split(code)
            write_nb(cfg_path, cfg_name, splits, num, parent, private_list)

            # Generate the `__all__` in the top of each .py
            if '__all__' not in code:
                c = code.split("(unless otherwise specified).")
                code = c[0] + "(unless otherwise specified).\n" + f'\n__all__ = {export_names(code)}\n\n# Cell' + c[1]
                with open(file, 'w', encoding='utf8') as f: f.write(code)
        else:
            print(f"{file.name} was already converted.")
    generate_doc_foundations()
    print(f"{Config(cfg_path, cfg_name).lib_name} successfully converted!")
    # _setup = int(input("Would you like to setup this project to be pip installable and configure a setup.py? (0/1)"))
    # if _setup: 
    #     generate_setup()
    #     print('Project is configured for pypi, please see `setup.py` for any advanced configurations')
    # _workflow = int(input("Would you like to setup the automated Github workflow that nbdev provides? (0/1)"))
    # if _workflow: 
    #     generate_ci()
    #     print("Github actions generated! Please make sure to include .github/actions/main.yml in your next commit!")
