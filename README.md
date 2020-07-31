There's a lot of fortran code still used today that was written decades ago in fortran 77. Sometimes you don't want to mess with the legacy code base but if one realy wants to convert the old 77 fixed source code to modern free form source Fortran, the job becomes really tedious and annoying. This script aims to automate the process to easily produce formatted free form code.


### How to use:
Just run the python script with your FORTRAN 77 file name as argument
```bash
python convert.py <file_name>.f
```
It will output a file named `<file_name>.f90`. All avilavle options,
```
>python convert.py -h
usage: convert.py [-h] [-o PATH] [-maxcol MAXCOL] [-indent INDENT] [-numbereddo] [-keepblank] [-progstate] PATH

Convert fixed source FORTRAN 77 code to indented modern free form Fortran 90 code

positional arguments:
  PATH            Name of the input file

optional arguments:
  -h, --help      show this help message and exit
  -o PATH         Name of the output file
  -maxcol MAXCOL  Maximum allowed column
  -indent INDENT  Length of indentation of each labels
  -numbereddo     Convert numbered do blocks
  -keepblank      Keep blank lines
  -progstate      Insert a `program` statement at the top
```


### What it can do:
1. Convert comment style
2. Convert line continuation
3. Removes numbered do loop
4. Removes format labels and move them inside respective write statements
5. Indent the code
6. Removes unwanted blank lines
7. Converts to lower case
8. Replaces things like '.ge.', '.le.', '.gt', '.lt.' etc
9. Removes return and stop before end statements
10. Fixes OpenMP multiline directives


### What it can't do:
1. Replacing go to statements.
2. Changeing variable declaration i.e implicit declaration, common statements etc.
3. Removing block data
4. Removing arithmatic if statements
5. Handling preprocessing commands.


### Where it fails:
The script removes numbered do loop and any label associated with it, so if a numbered do loop shares its label with any other goto or arithmatic if statements, the sctipt will break the code. If your script contains such cases you must diable the numbered do loop conversion.


### What's the catch:
To make things easier the script converts evrything to lowercase. The script doesn't guarentee to covert any error. User must check the resulted code before running.