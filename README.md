There's a lot of fortran code still used today that was written decades ago in fortran 77. Sometimes you don't want to mess with the legacy code base but if one realy wants to convert the old 77 fixed source code to modern free form source Fortran, the job becomes really tedious and annoying. This script aims to automate the process to produce Fortran 90 code from 77 one.


### How to use:
Just run the python script with your FORTRAN 77 file name as argument
```bash
python <file_name>.f
```
It will output a file named `<file_name>.f90`. You can control the conversion by modifying the flags placed at the top of the python script. Check the example folder for some examples


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
10. Fixes openmp multiline directive


### What it can't do:
1. Replacing go to statements.
2. Changeing variable declaration i.e implicit declaration, common statements etc.
3. Removing block data
4. Removing arithmatic if statements
5. Handling preprocessing commands.


### Where it fails:
The script removes numbered do loop and any label associated with it, so if a numbereddo loop shares its label with anyother goto or arithmatic if statements, this sctipt will break the code. If your script contains such cases you must turn off the numbered do loop check.


### What's the catch:
To make things easier this script convert evrything to lowercase.