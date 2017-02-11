# General Problems
## Path detection problems

- Autodetection of the converters fail in the binary version of Panconvert
- Sometimes, after the path has been filled in manually, Panconvert has to be restarted
- The path problem only happens for the first initialisation of Panconvert or when the settings
are manually deleted

## Binary problems

- Windows: the binary version only works for 32bit systems
- Linux: On older Systems there are needen glibs missing (The installed ones are outdated)

# Manual Converter
## Options Field

- The last parameter may not be endet with an ;
- No Blanks may be used in parameters
- Wrong spelling leeds to pandoc errors

## Batch Conversion
of the Manual Converter

- If you use binary files like docx, and you have textfiles with an binary extension,
panconvert will fail
- The file filter can not distingush between .md and md.html
- If you used batchconversion with binary files, you have to move all non-binary
files with extensions like .docx.html or docx.md

# Update Problems
If you encounter problems after an update:

- There are known problems in the update process
- See the Update help for more information

