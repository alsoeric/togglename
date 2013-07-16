Welcome to the downloads for pywin32.

The SourceForge file system is horrible, making it very painful to 
locate the latest build - please follow the instructions below.
    
To download pywin32:

* Select the "Browse All Files" link, then navigate to the "pywin32"
  folder and select the latest available build (currently Build 217)

* Select the installer executable for your system.  Note that there 
  is one download package for each supported version of Python - 
  please check what version of Python you have installed and 
  download the corresponding package.

Some packages have a 32bit and a 64bit version available - you must download
the one which corresponds to the Python you have installed.  Even if you have
a 64bit computer, if you installed a 32bit version of Python you must install
the 32bit version of pywin32.

To determine what version of Python you have, just start Python and look at the
first line of the banner.  A 32bit build will look something like:

  Python 2.7.2+ ... [MSC v.1500 32 bit (Intel)] on win32
                                ^^^^^^^^^^^^^^

While a 64bit build will look something like:

  Python 2.7.2+ ... [MSC v.1500 64 bit (AMD64)] on win32
                                ^^^^^^^^^^^^^^


If the installation process informs you that Python is not found in the 
registry, it almost certainly means you have downloaded the wrong version -
either for the wrong version of Python, or the wrong "bittedness".

A changelog can be found at http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/raw-file/tip/CHANGES.txt
