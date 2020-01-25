# FileMover
Rename &amp; move PDFs based on the content inside. To be more specific, the PDF is searched for given regex to determine how the file should be renamed.

## Requirements
* Python 2.7.13 or greater
* Apache Tika - https://tika.apache.org/
  * For converting the PDF to text for searching
  * https://tika.apache.org/1.23/gettingstarted.html
  * `brew install tika`
  
## Usage
```sh
python FileMover.py {path/to/config.json} {path/to/pdf}
```

## Configuration
Create a `config.json` file using the included sample as a starting point. For each type of file you want to process, you'll need to configure the following:
* `"type"` - Name for the fileType
* `"search"` - Regex for fileType identification
* `"dateSearch"` - Regex for date identification (ex: `"Statement Date:.*(\\d+/\\d+/\\d{4})"`)
* `"dateFormat"` - Format for the date to be used in the new file name (ex: `"%m/%d/%Y"`)
* `"fileName"` - Destination path and name for the file - (ex: `"/Documents/Bills/Company Bill - {DATE}.pdf"`)
  * `{DATE}` will be replaced by the date found using by the `dateSearch` regex

## Testing
In order to figure out the correct values for the `search` & `dateSearch` values required for the config; you may need to test parsing the file to see how the text will be output by Tika. From the terminal, run the following command to start Tika in "GUI" mode:
```sh
tika -g
```
From here, you can drag the file and see the outputted text. It may help to copy/paste the plain text output into Sublime and test the regex. Some PDFs have weird characters that are hard to find.

## Application Usage (Drag & Drop Support)
To enable drag & drop support, you can turn the script into an application using Script Editor (Mac OS).
* Using the `Recursive File Processing Droplet` as a template, save the following script in the `process_file()` sub-routine:
```applescript
	set testVar to do shell script "/fully/qualified/path/to/python /fully/qualified/path/FileMover/FileMover.py " & "/fully/qualified/path/FileMover/config.json '" & POSIX path of this_item & "'"
	display dialog testVar
```
_Be sure to use fully qualified paths_
  
[Mac OS X Hints - Create a drag and drop interface to shell scripts](http://hints.macworld.com/article.php?story=20021125060127218)

## Help & Resources
* [Python datetime Format](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)
* [Python Logging](https://docs.python.org/2/howto/logging.html#logging-basic-tutorial)
  * [Python Logging Attributes](https://docs.python.org/2/library/logging.html#logrecord-attributes)
