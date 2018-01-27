#!/usr/bin/env python
from multiprocessing.dummy import Pool as ThreadPool
import requests
import psutil
import os
import sys
from optparse import OptionParser
import warnings


def parse_input():

    parser = OptionParser("Usage: %prog [options] <target_url>", prog=sys.argv[0])

    parser.add_option("-c", "--cookie", dest="cookie",
                      help="Set cookies for the request", metavar="COOKIE_STRING")

    parser.add_option("-e", "--extension", dest="extension",
                      help="Set extension", metavar="EXTENSION")

    parser.add_option("-o", "--output", dest="output",
                      help="Set filename output", metavar="FILENAME")

    parser.add_option("-d", "--directory", dest="directory",
                      help="Set directory", metavar="DIRECTORY")

    parser.add_option("-p", "--proxy", dest="proxy",
                      help="Set proxy", metavar="PROXY")

    parser.add_option("-u", "--user-agent", dest="user_agent",
                      help="Set User-Agent", metavar="USER_AGENT")

    parser.add_option("-m", "--min", dest="min",
                      help="Set minimum value", metavar="MIN")

    parser.add_option("-M", "--max", dest="max",
                      help="Set maximum value", metavar="MAX")
    
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)        

    return parser


def suppress_warnings():
    """
    Suppress warnings on proxy SSL certificate's validity
    """
    warnings.filterwarnings("ignore")


def setup_session(cookie, proxy, user_agent):
    """
    :return the Session Object with the cookies manually set in a dict in order to access restricted web pages
    """

    # create Session
    session_object = requests.Session()

    # set Cookie Jar
    cookies = {
        str(cookie).split(':')[0] : str(cookie).split(':')[1]
    }

    session_object.cookies = requests.utils.cookiejar_from_dict(cookies)

    # set Proxy (such as Burp)
    session_object.proxies = {"http": proxy, "https": proxy}

    # set User-Agent
    session_object.headers['User-Agent'] = user_agent

    return session_object


def save_to_file(directory, name, extension, content, index):
    """
    iterate through the incremental number in the URL in order to get the resources
    in that pages and save them into a file
    """

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = "{0}/{1}{2}.{3}".format(directory, name, index, extension)
        with open(file_path, "wb") as file_out:
            file_out.write(content)
    except Exception as ex:
        raise OSError(ex)


def task(index):
    """
    task to be executed by each thread of the pool
    :param index that is part of the Url to request
    """
    
    full_url = url_path.format(index)
    response = session.get(full_url, verify=False) # verify=False for avoid 'SSL: CERTIFICATE_VERIFY_FAILED' with proxy certificates
    save_to_file(output_directory, filename, extension, response.content, index)


if __name__ == "__main__":
    
    suppress_warnings()
    parser = parse_input()

    (options, args) = parser.parse_args()

    url_path = args[0]
    output_directory = options.directory
    extension = options.extension
    filename = options.output
    cookie = options.cookie
    proxy = options.proxy
    user_agent = options.user_agent
    min = options.min
    max = options.max
    
    session = setup_session(cookie, proxy, user_agent)

    poolSize = 4  # max 2 * number of cores of the cpu
    pool = ThreadPool(poolSize)
    # create an iterable object from the range of indexes because the {@see Pool.map} needs an Iterable as argument
    iterableIndexes = range(int(min), int(max))  # xrange is faster than range but is not available in Python 3.6
    
    try:
        pool.map(task, iterableIndexes)
    except Exception as e:
        print(e)
    finally:
        pool.close()
        pool.join()
        print("Operation ended")
