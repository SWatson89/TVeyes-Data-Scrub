# TVeyes-Data-Scrub
Data fetching project for Tveyes

This code was developed to fech data from the MediaEyes website used by CVM

The code is written using Python Version 3.9. and uses the following libraries as dependencies

      BeautifulSoup4
      Pandas
      Numpy
      MoviePy
      Openpyxl
      
      Some dependent Libraries may have codepencies which are installed with the library
      
      

The script works as follows:

It allows the user to input the location of the excel file for e.g. C:\Users\Stefan\Downloads\Broadcast Links.xlsx. The full path must be used
No space is allowed after the string

It allows the user to enter a location for the data to be stored for e.g. C:\Users\Stefan\Downloads\Broadcast The full path must be used
No space is allowed in the string or after

It creates the folder, Broadcast in this instance, creates subfolders to store the data
the subfolder is names in the format Date-Time-Station corresponding with the first the columns of the excel file
the time section has underscores instead of colons(colons cannot be in a file name)

In the subfolder the transcript timestamps as well as the video and converted audio is stored.
The transcript file is named as Transcript.txt
The timestamps file is name Timestamp.txt
The video and audio files are named based on the filenames fetched from the server.
The video and audio are also segmented as stored and fetched from the server.




