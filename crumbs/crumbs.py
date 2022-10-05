from encodings.utf_8_sig import encode
from tkinter import *
from tkinter import filedialog
import os
import shutil
from bs4 import BeautifulSoup as bs
import json

# gui_win = Tk()
# gui_win.geometry('500x250')
# gui_win.grid_rowconfigure(0, weight = 1)
# gui_win.grid_columnconfigure(0, weight = 1)

# def directory():
#     # get a directory path by user
#     filepath=filedialog.askdirectory(initialdir=r"~", title="Dialog box")
#     label_path=Label(gui_win,text=filepath,font=('italic 14'))
#     label_path.pack(pady=20)

# dialog_btn = Button(gui_win, text='Select folder', command = directory)
# dialog_btn.pack(pady=20)

# gui_win.mainloop()

dir=filedialog.askdirectory(initialdir=r"C:\xampp\htdocs\sandbox\py\crumbs\ERR", title="フォルダー選択")

# ToDo: Check the "converted" directory exists and is empty
if os.path.isdir('converted'):
    shutil.rmtree('converted')
os.makedirs('converted')

# ToDo: Test on server path

# ToDo: get user input for the output directory

# ToDo: Initialize logging and add outputs to code
# https://realpython.com/python-logging/

# template for the script tag content
tpl = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': [],
}

# loop over all files in the directory
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    print(f)
    if os.path.isfile(f):
        # if filename.endswith('m0400.html'):
        if filename.endswith('.html'):
            # create the bs4 object
            fp = open(f, encoding='utf-8')
            soup = bs(fp, 'html.parser')

            # check if script already exists
            script_exists = soup.find('script', type='application/ld+json')

            # process file if script is not already present
            if script_exists is None:
                results = []
                print("===")
                print(f'File: {f}')

                # get the topic path content
                topicpath = soup.find("ol", {"class": "topic_path"})

                if topicpath is not None:
                    listitems = topicpath.find_all("li")
                    for idx, li in enumerate(listitems, start=1):
                        txt = li.text
                        # print("Text #" + str(idx) + ": " + txt)
                        hrf = li.find('a', href=True)
                        if hrf is not None:
                            # print("href: " + hrf['href'])
                            hrf = hrf['href']
                        else:
                            # print("href: " + filename)
                            hrf = filename
                        itemdetails = {}
                        itemdetails['@id'] = hrf
                        itemdetails['name'] = txt

                        item = {}
                        item['item'] = itemdetails

                        newitem = {}
                        newitem['@type'] = 'ListItem'
                        newitem['position'] = idx

                        newitem.update(item)
                        results.append(newitem)

                else:
                    print("No topicpath found")

                # add the results to the tempalte
                tpl['itemListElement'] = results

                # add script tag to the file
                new_script = soup.new_tag('script', type='application/ld+json')
                new_script.string = json.dumps(tpl, indent=4)
                soup.html.head.append(new_script)

                # ToDo: change direectory to user specified directory if set
                with open("converted/" + filename, "w", encoding='utf-8') as file:
                    # ToDo: retain the original indentation in the html
                    # file.write(str(soup.prettify()))
                    file.write(str(soup))

            else:
                # copy the file to the converted folder
                # ToDo: change direectory to user specified directory if set
                shutil.copy2(f, "converted/" + filename)
