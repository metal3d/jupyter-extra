import subprocess
from IPython.display import HTML, display

name = "jpyextra"


def datadoc(data):
    """ Display sklearn dataset DESCR in well formed Markdown

    You need "pandoc" tool. Install it with conda, or with your
    package manager.
    """
    doc = data.DESCR.replace('%PLU', '')
    pdc = subprocess.Popen([
        'pandoc',
        '-t',
        'html',
        '-f',
        'rst',
        '--eol', 'lf'
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
    md, _ = pdc.communicate(bytes(doc, 'utf-8'))
    md = md.decode()
    display(HTML(data=md))
