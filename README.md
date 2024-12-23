# ppdf

Uses [PyPDF2](https://pypi.org/project/PyPDF2/) and [pymupdf](https://pymupdf.readthedocs.io/) to `split` `merge` and `extract pages` from pdfs in a `CLI` interface.

## Examples
    
- Merging: 

To merge all pdf files in a folder into "output_file.pdf" use:

`PPDF ".*pdf" -m -f "output_file.pdf"`

- Splitting:

To extract the 4th page of a PDF file use:

`PPDF "pdf_file_name.pdf" -s 4 4 1`
