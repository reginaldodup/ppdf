# !/usr/bin/python

# Author: Reginaldo MARINHO
# Date:   11-20-19
# email:  reginaldomsj@gmail.com

from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import re
import os
import argparse
import fitz

"""
    This script merges, split or extracts pdf pages.
    
    positional arguments:
                            search_patern: regex expression of files to be merged
    
    optional arguments:
    -h, --help            show this help message and exit
    -f [OUTPUT_FILE_NAME], --output_file_name [OUTPUT_FILE_NAME]
                            output file name
    -p [FOLDER_PATH], --folder_path [FOLDER_PATH]
                            folder containing files to be renamed
    -r [PAGE_ROTATION], --page_rotation [PAGE_ROTATION]
                            rotation to be applied to each page
    -v, --verbose         Print verbose
    -c, --check_output    Check outputs
    -s SPLIT [SPLIT ...], --split SPLIT [SPLIT ...]
                            split to individual files: page sequence start number,
                            end page, increment
    -e EXTRACT [EXTRACT ...], --extract EXTRACT [EXTRACT ...]
                            extract to single files: page sequence start number,
                            increment
    -m, --merge           merge files
    -o, --odd             extract odd pages to single file
    -n, --even            extract even pages to single file
    
    Examples
    
    Merging: 
        To merge all pdf files in a folder into "output_file.pdf" use:
        PPDF ".*pdf" -m -f "output_file.pdf"
    
    Splitting:
        To extract the 4th page of a PDF file use:
        PPDF "pdf_file_name.pdf" -s 4 4 1
"""

parser = argparse.ArgumentParser(
    description="This script merges, split or extracts pdf pages."
)

parser.add_argument(
    "search_patern",
    metavar="",
    help="search_patern: regex expression of files to be merged",
)

parser.add_argument(
    "-g", "--engine", nargs="?", default="2", help="1: PyPDF2; 2:pymupdf"
)

parser.add_argument(
    "-f", "--output_file_name", nargs="?", default="binder.pdf", help="output file name"
)
parser.add_argument(
    "-p",
    "--folder_path",
    nargs="?",
    default=False,
    help="folder containing files to be renamed",
)
parser.add_argument(
    "-r",
    "--page_rotation",
    type=int,
    nargs="?",
    default=0,
    help="rotation to be applied to each page",
)

parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose")
parser.add_argument("-c", "--check_output", action="store_true", help="Check outputs")

group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-s",
    "--split",
    type=int,
    nargs="+",
    help="split to individual files: page sequence start number, end page, increment",
)
group.add_argument(
    "-e",
    "--extract",
    type=int,
    nargs="+",
    help="extract to single files: page sequence start number, increment",
)

group.add_argument("-m", "--merge", action="store_true", help="merge files")
group.add_argument(
    "-o", "--odd", action="store_true", help="extract odd pages to single file"
)
group.add_argument(
    "-n", "--even", action="store_true", help="extract even pages to single file"
)


args = parser.parse_args()


if args.folder_path:
    cwd = args.folder_path
else:
    cwd = os.getcwd()


def merge_pdf_files(file_list, output_file_name):

    # engine = input("\nPlease choose an engine\n1: PyPDF2 (with bookmarks-slow)\n2: pymupdf (no bookmarks-faster)\n> ")
    if args.engine == "1":
        # Old way, not working for some cases
        # ----
        print("Binding with PyPDF2...")
        merger = PdfMerger()
        page_count = 0
        for filename in file_list:
            with open(filename, "rb") as f:
                reader = PdfReader(f)
                merger.append(reader)
                merger.add_outline_item(filename, page_count)
                page_count = page_count + len(reader.pages)

        merger.write(output_file_name)
    else:
        # new way with pymupdf
        print("Binding with pymupdf...")
        doc = fitz.open()
        for file in file_list:
            doc.insert_file(file, annots=True)

        doc.save(output_file_name)
        doc.close()
    print("Done!")


def extract_page(page_number):

    output_file_name = "page " + str(page_number) + ".pdf"

    with open(input_file_name, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()

        writer.add_page(reader.pages[page_number])

        with open(output_file_name, "wb") as wf:
            writer.write(wf)


def extract_pages(
    input_file_name, output_file_name, start_page, last_page, step, page_rotation
):

    with open(input_file_name, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()

        if last_page + 1 > len(reader.pages) or last_page == 0:
            last_page = len(reader.pages)

        for i in range(start_page - 1, last_page, step):

            if page_rotation == 0:
                writer.add_page(reader.pages[i])
            else:
                writer.add_page(reader.pages[i].rotate(page_rotation))

        with open(output_file_name, "wb") as wf:
            writer.write(wf)


def extract_pages_to_individual_files(
    start_page, end_page, input_file_name, step, page_rotation
):

    with open(input_file_name, "rb") as f:
        reader = PdfReader(f)
        outlines = reader.outline

        if end_page == 0:
            end_page = len(reader.pages)

        for i in range(start_page - 1, end_page, step):

            writer = PdfWriter()
            if page_rotation == 0:
                writer.add_page(reader.pages[i])

            else:
                writer.add_page(reader.pages[i].rotate(page_rotation))

            with open("page " + str(i + 1) + ".pdf", "wb") as wf:
                # with open(outlines[i]['/Title'] + '.pdf','wb') as wf:
                writer.write(wf)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]


def rotate_pdf_pages(input_file_name, rotation):

    with open(input_file_name, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()

        for pagenum in range(len(reader.pages)):
            page = reader.pages[pagenum]
            page.rotate(rotation)
            writer.add_page(page)

    with open(input_file_name, "wb") as wf:
        writer.write(wf)


if __name__ == "__main__":

    # MERGING
    if args.merge:
        # make sure match is case insensitive
        ignorecase = re.compile(args.search_patern, re.IGNORECASE)
        # Create file list
        # file_list = [f for f in os.listdir(cwd) if re.match(args.search_patern, f, flags=0)]
        file_list = [f for f in os.listdir(cwd) if ignorecase.match(f)]
        file_list.sort(key=natural_keys)  # sort file list
        if args.check_output:
            print("Files to be merged:\n---")
            for f in file_list:
                print(f)
            print("---\noutput file name: " + args.output_file_name)
            print("Page rotation: " + str(args.page_rotation))
        else:
            merge_pdf_files(file_list, args.output_file_name)
            if args.verbose:
                print("Files to be merged:\n---")
                for f in file_list:
                    print(f)
                print("---\noutput file name: " + args.output_file_name)
                print("Page rotation: " + str(args.page_rotation))

            if args.page_rotation != 0:
                rotate_pdf_pages(args.output_file_name, args.page_rotation)

    # SPLITING
    elif args.split:
        if args.split[0] == -1:
            split_seq = [1, 0, 1]
        else:
            split_seq = args.split

        # Modify to do the same action for all matched PDFs
        file_list = args.search_patern
        if args.check_output:
            print("File to be splitted: " + args.search_patern)
            print("start page: " + str(split_seq[0]))
            last_page = "last" if split_seq[1] == 0 else str(split_seq[1])
            print("end page:   " + last_page)
            print("step:       " + str(split_seq[2]))
            print("Page rotation: " + str(args.page_rotation))
        else:
            if args.verbose:
                print("File to be splitted: " + args.search_patern)
                print("start page: " + str(split_seq[0]))
                last_page = "last" if split_seq[1] == 0 else str(split_seq[1])
                print("end page:   " + last_page)
                print("step:       " + str(split_seq[2]))
                print("Page rotation: " + str(args.page_rotation))

            extract_pages_to_individual_files(
                split_seq[0], split_seq[1], file_list, split_seq[2], args.page_rotation
            )
    # EXTRACTING RAGE
    elif args.extract:
        if args.extract[0] == -1:
            extract_seq = [0, 0, 1]
        else:
            extract_seq = args.extract

        file_list = args.search_patern
        if args.check_output:
            print("File to extract from: " + args.search_patern)
            print("output file name: " + args.output_file_name)
            print("start page: " + str(extract_seq[0]))
            last_page = "last" if extract_seq[1] == 0 else str(extract_seq[1])
            print("end page:   " + last_page)
            print("step:       " + str(extract_seq[2]))
            print("Page rotation: " + str(args.page_rotation))
        else:
            if args.verbose:
                print("File to extract from: " + args.search_patern)
                print("start page: " + str(extract_seq[0]))
                last_page = "last" if extract_seq[1] == 0 else str(extract_seq[1])
                print("end page:   " + last_page)
                print("step:       " + str(extract_seq[2]))
                print("Page rotation: " + str(args.page_rotation))
            extract_pages(
                file_list,
                args.output_file_name,
                extract_seq[0],
                extract_seq[1],
                extract_seq[2],
                args.page_rotation,
            )
    # EXTRACTING ODD
    elif args.odd:
        extract_seq = [1, 0, 2]
        file_list = args.search_patern
        if args.check_output:
            print("File to extract from: " + args.search_patern)
            print("output file name: " + args.output_file_name)
            print("Extract odd pages")
            print("Page rotation: " + str(args.page_rotation))
        else:
            if args.verbose:
                print("File to extract from: " + args.search_patern)
                print("Extract odd pages")
                print("Page rotation: " + str(args.page_rotation))

            extract_pages(
                file_list,
                args.output_file_name,
                extract_seq[0],
                extract_seq[1],
                extract_seq[2],
                args.page_rotation,
            )

    # EXTRACTING EVEN
    elif args.even:
        extract_seq = [2, 0, 2]
        file_list = args.search_patern
        if args.check_output:
            print("File to extract from: " + args.search_patern)
            print("output file name: " + args.output_file_name)
            print("Extract even pages")
            print("Page rotation: " + args.page_rotation)
        else:
            if args.verbose:
                print("File to extract from: " + args.search_patern)
                print("start page: " + str(extract_seq[0]))
                print("Page rotation: " + str(args.page_rotation))

            extract_pages(
                file_list,
                args.output_file_name,
                extract_seq[0],
                extract_seq[1],
                extract_seq[2],
                args.page_rotation,
            )
