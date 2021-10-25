import os
import sys

from pylatex import *
from pylatex.base_classes.command import *
from pylatex.utils import *



def main(argv):
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options,document_options="a5paper")
    doc.preamble.append(Package('pdfpages'))
    doc.preamble.append(Package('multicol'))
    doc.preamble.append(Package('babel','czech'))
    doc.preamble.append(Command('AtEndDocument',NoEscape("\\addtocontents{toc}{\\protect\\begin{multicols}{3}}")))
    # doc.preamble.append(Command('AtEndDocument',NoEscape('\\addtocontents{toc}{\\protect\\end{multicols}}')))
    doc.preamble.append(Command('makeatletter'))
    doc.preamble.append(Command('renewcommand',Arguments(NoEscape('\\@dotsep'),'10000') ))
    doc.preamble.append(Command('makeatother'))
    doc.preamble.append(Command('renewcommand*',arguments=NoEscape('\\contentsline'),options='3',extra_arguments=NoEscape('\\csname l@#1\\endcsname{#2}{}')))
    doc.preamble.append(Command('pagenumbering','gobble'))

    doc.preamble.append(Command('title', 'Zpěvník'))
    doc.preamble.append(Command('author', ''))
    doc.preamble.append(Command('date', NoEscape(r'\today')))



    doc.append(NoEscape(r'\maketitle'))

    doc.append(NewPage())


    dirs = os.listdir('.')
    for d in dirs:
        if not os.path.isdir(d) or d == '.git':
            continue
        songs = os.listdir('./'+d)
        songs.sort()
        #doc.append(Section(d))
        #doc.append(NewPage())
        for s in songs:
            if '.pdf' not in s:
                continue
            s_nopdf = os.path.splitext(s)[0]
            try:
                f = open('./'+d+'/'+s_nopdf+'.txt','r', encoding=sys.stdin.encoding)
                tit = f.readline()
            except:
                tit = ''
                for i in range(len(s_nopdf)):
                    if s_nopdf[i] == '_':
                        tit+=' '
                    else:
                        tit+=s_nopdf[i].encode().decode(sys.stdin.encoding)
            print(tit)
            doc.append(Command('addcontentsline',Arguments('toc','subsection',tit)))
            doc.append(Command('includepdf',NoEscape('./'+d+'/'+s),'scale=1'))
        doc.append(NewPage())
    doc.append(Command('tableofcontents'))
    doc.append(NewPage())


    doc.generate_pdf('zpevnik', clean_tex=False,compiler='pdfLaTeX')
    return 0


if __name__ == "__main__":
    main(sys.argv)
