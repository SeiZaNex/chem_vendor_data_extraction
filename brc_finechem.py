#!/usr/bin/env python2.7

import re
import urllib
import StringIO

def remove_html_tags(text):
    tags = '<[^<]+?>'   
    return re.sub(tags, '', text)

def read_url_list():
    f = open('url_list.txt', 'r')
    url_list = []
    for line in f:
        if (line != '\n'):
            url_list.append(re.sub('\n', '', line))
    return url_list

def has_alphanumeric(string):
    return re.search('[a-zA-Z0-9]', string)

def is_target(line, pattern):
    return True if -1 != line.find(pattern) else False

def parse_page(page):
    buf = StringIO.StringIO(page)
    chem_cat = 'class="category-banner"'
    chem_des = 'class="note-msg"'
    page_div = '<div'
    page_undiv = '</div'
    div_count = 0
    div_parse = False
    
    for line in buf:
        if (True == div_parse):
            if (is_target(line, page_div)):
                div_count += 1
            print re.sub('\n', '', remove_html_tags(line))
        if (is_target(line, page_undiv)):
            if (div_count > 0):
                div_count -= 1
            else:
                div_parse = False
        if (is_target(line, chem_cat) or is_target(line, chem_des)):
            div_parse = True
            print "tag" 

def main():
    url_list = read_url_list()
    data = []

    ustream = urllib.urlopen(url_list[0])
    udata = ustream.read()
    data.append(udata)

    parse_page(data[0]) #print data[0]

#    ustream = urllib.urlopen("https://www.brc-finechemicals.com/")
#    udata = ustream.read()
    
#    data = remove_html_tags(udata)
#    print udata


if __name__ == '__main__':
    main()
