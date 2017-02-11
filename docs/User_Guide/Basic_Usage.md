# Basic Usage

## Errors and Information
* All Errors are written to a log window
* A Counter of messages can be read in the main gui. If no error, occurred, there is no message
* If you hide the log completely and nothing goes wrong, you don`t need the log viewer
* If you are in batch-mode, a list of all the converted files is written to the log viewer
* Look at the log viewer, if something unexpected had happend. If you need more information,
go to the Discussion Forum on Sourceforge

## The preconfigured conversion sets

* These are the preconfigured standard converters. All documents are Standalone-Versions of the document.
* Make sure the Standard-Conversion Checkbox is marked. Otherwise you have to use the manual converter
* The Batch-Conversion Checkbox has to be unchecked
* Chose one From Format
* Chose one To Format. The formats should not be the same

## Usage of the manual converter

* The Standard – Checkbox has to be unchecked.
* The Batch-Conversion Checkbox has to be unchecked
* In the From-field you have to fill in the supported pandoc formats of
the source format. A list of all From-formats is available via the ... Button at the end of the input field.
* In the To-field you have to fill in the supported pandoc formats of the
destination format. A list of all To-formats is available via the ... Button at the end of the input field.
* In the Parameter field, all known pandoc parameters, separated via semicolon ';' can be used. A list of all options is available via the ... Button at the end of the input field.
* For some formats the Parameter field can be left blank, for others it
has to be filled. 
* To get a odt or epub file, you have to specify the name of the file. There is a working
example for odt filled in already. The file will be saved in the same directory where the panconvert directory is saved, e.g. on MacOS it will be /Applications
* The last parameter should not be closed with a ;
* If you get a pandoc error, the syntax of the Parameter field is wrong.

## Batch Conversion

* Both the Manual and the standard conversion work in batchmode. See the help sections above.
* First you have to decide if you want to convert a filelist or a directory
* A directory can be converted recursivly
* Files can be added from different locations. Only one format conversion at a time
* A Filefilter can reduce the types of the processed files. E.g. markdown;md; for all types of Markdown files.

