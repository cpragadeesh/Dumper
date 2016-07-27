import mechanize
from bs4 import BeautifulSoup
from lxml import etree

browser = mechanize.Browser()
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "<url redacted>"

browser.open(url)
browser.select_form(nr=0)

browser.form['username'] = '<redacted>'
browser.form['passwd'] = '<redacted>'

browser.submit()

url = "<redacted>"

fullList = etree.Element('list')
count = 0

f2 = open("<redacted>.xml", "w+")

with open('<redacted>.txt', 'r+') as f:

    for line in f:
        count = count + 1
        print count
        
        browser.open(url)

        browser.select_form(nr=0)
        browser.form['rollno'] = line[:-1]
        
        browser.submit()
        
        soup = BeautifulSoup(browser.response().read(), "lxml")
        inlist = soup.findAll('input')
        
        student = etree.SubElement(fullList, 'student')
        
        for inp in inlist:
            
            instr = str(inp)
            i = instr.find('name')
            i = instr.find('=', i + 1)
            i = i + 2
            
            inpname = instr[i:instr.find('''"''', i)]
            if inpname in ['studpassword', 'input id=', 'update', 'close']:
                continue
    
            tag = etree.SubElement(student, inpname)
            
            i = instr.find('value')
            
            namei = instr.find("=", i)
            namei = namei + 2
            
            tag.text = instr[namei : instr.find('''"''', namei + 1)]


        tag = etree.SubElement(student, 'address')
        if soup.textarea.contents:
            tag.text = soup.textarea.contents[0]
        else:
            print line
print "Contains: " + str(count) + " students"
f2.write(etree.tostring(fullList, pretty_print = True))




                    

