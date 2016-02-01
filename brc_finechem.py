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

    parse_sec = 0

    text = ""
    iupac = ""
    cas = ""
    mol_mass = ""
    mol_form = ""
    
    for line in buf:
        if (True == div_parse):
            if (is_target(line, page_div)):
                div_count += 1
            if ("" != remove_html_tags(line)):
                form = remove_html_tags(line)
                form = re.sub('\r\n', '', form)
                if (is_target(form, "IUPAC")):
                    iupac = re.sub("IUPAC: ", '', form)
                if (is_target(form, "CAS#")):
                    cas = re.sub("CAS#: ", '', form)
                if (is_target(form, "Molecular Mass")):
                    mol_mass = re.sub("Molecular Mass: ", '', form)
                if (is_target(form, "Molecular Formula")):
                    mol_form = re.sub("Molecular Formula: ", '', form)
                if (1 == parse_sec and has_alphanumeric(form)):
                    text += form
        if (is_target(line, page_undiv)):
            if (div_count > 0):
                div_count -= 1
            else:
                div_parse = False
        if (is_target(line, chem_des)):
            div_parse = True
            parse_sec += 1
    array = [iupac, cas, mol_mass, mol_form, text]
    print array
    return array

def main():
    output = open("brc_output.txt", 'w+')

    url_list = read_url_list()

    for url in url_list:
        print "Opening: " + url
        ustream = urllib.urlopen(url)
        udata = ustream.read()
        array = parse_page(udata)
        ofstr = url + '\t'
        for i in array[:-1]:
            ofstr += i + '\t'
        ofstr += array[-1] + '\n'
        output.write(ofstr)
        print "Page has been formated and written" + '\n'
    output.close()

if __name__ == '__main__':
    main()
