# ppdf

Uses [PyPDF2](https://pypi.org/project/PyPDF2/) and [pymupdf](https://pymupdf.readthedocs.io/) to `split` `merge` and `extract pages` from pdfs in a `CLI` interface.

## Examples
    
- Merging: 

To merge all pdf files in a folder into "output_file.pdf" use:

`PPDF ".*pdf" -m -f "output_file.pdf"`

- Extracting:

To extract the pages 4 to 8 with a step of 2 into a `binder.pdf` file use:

`PPDF "pdf_file_name.pdf" -e 4 2 8`

- Splitting:

To extract the pages 4 to last page with a step of 2 into separate pdf files use:

`PPDF "pdf_file_name.pdf" -s 4 0 2`

This will create files `page 4.pdf`, `page 6.pdf`, `page 8.pdf` and so on until last page.

A page rotation parameter `-r` can be used with any of the above flags.

For more details check `ppdf.py --help`.

# Dependencies

`PyPDF2` and `pymupdf`.
