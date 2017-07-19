Download all papers in cvpr access

# Dependencies
    
    selenium
    chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads)

# Set up

    git clone
    cd cvpr2017
    git submodule init
    git submodule update

# How to use
    
    run main.py -b /path/to/chromedrive -u http://openaccess.thecvf.com/CVPR2017_workshops/CVPR2017_W37.py -d /where/to/save/pdf 

# Details

    -b, --browser: path to chromedriver
    -u, --url: page url that pdf are listed (for example http://openaccess.thecvf.com/CVPR2017_workshops/CVPR2017_W37.py)
    -d, --destination: path to save pdf
    -header, --header: header of href
    -thread, --thread: the number of thread for downloading
    -timeout, --timeout: timeout while downloading pdf
