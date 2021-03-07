#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys, traceback, os, subprocess, re, json
import logging as LOG
from datetime import datetime

# Load config file
config_file = sys.argv[1]
with open(config_file) as config_file:
    config = json.load(config_file)

# Configure Logging
LOG.basicConfig(format='%(levelname)s\t%(asctime)s,%(filename)s> %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S %Z',
    filename=config["logFile"],
    level=LOG.getLevelName(config["logLevel"]))

# Gather our code in a main() function
def main():
    for file in sys.argv[2:]:
        text = pdfToText(file)
        if text:
            LOG.debug(text)
            processFile(file, text)
        else:
            error = 'File could not be parsed...'
            LOG.error(error)
            print(error)


def processFile(file, text):
    # Loop through all the fileTypes in the config file to determine which type we have
    for fileProps in config["filePropertiesList"]:
        LOG.debug(fileProps["search"])
        match = re.search(fileProps["search"], text, re.MULTILINE)
        if match:
            # If found fileType, now find the date
            fileDate = findDate(text, fileProps)
            if fileDate:
                renameFile(file, fileProps, fileDate)

            return

    error = 'Unable to determine file type for file: %s' % (file)
    LOG.error(error)
    print(error)


def findDate(text, fileProps):
    match = re.search(fileProps["dateSearch"], text, re.MULTILINE)
    if match:
        dateObj = tryParsingDate(match.group(1))
        return dateObj.strftime(config["finalDateFormat"])
    else:
        error = "(%s) - Unable to find the date" % (fileProps["type"])
        LOG.error(error)
        print(error)
        return None

def tryParsingDate(text):
    for searchableDateFormat in config["searchableDateFormats"]:
        try:
            return datetime.strptime(text, searchableDateFormat)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def renameFile(file, fileProps, fileDate):
    newFileName = fileProps["fileName"].replace('{DATE}', fileDate)
    if not os.path.exists(newFileName):
        try:
            os.rename(file, newFileName)
        except Exception as e:
            error = "Unable to rename file from %s to %s" % (file, newFileName)
            LOG.exception(error)
            print(error)
            raise e
        else:
            logSuccess = "Successfully renamed file from %s to %s" % (file, newFileName)
            LOG.info(logSuccess)
            printSuccess = "%s\n\nSuccessfully renamed & moved file to %s" % (fileProps["type"], newFileName)
            print(printSuccess)
    else:
        error = "File already exists, will NOT overwrite : %s" % (newFileName)
        LOG.error(error)
        print(error)


# Convert PDF to text
def pdfToText(file):
    try:
        return subprocess.check_output(["/usr/local/bin/tika", "-t", file])
    except Exception as e:
        error = "Unable to parse text from PDF file - %s" % (file)
        LOG.exception(error)
        print(error)
        raise e


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()
