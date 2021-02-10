import csv
import os
import urllib.request
from threading import Thread


def img_link_dw(folder_name, file_name):
    # this function will take the input of the .csv file containing the img links, download the imgs
    # then store them in the folder with the input folder name in the same directory of the script.
    # may need some modification for different situation inside the .csv files.
    # in this example, I used the exported .csv file of the Web Scraper chrome extension.
    # it has web-scraper-order,web-scraper-start-url,img-src as the three columns inside the csv file

    f = open(file_name)
    csv_f = csv.reader(f)

    img_links = []
    for row in csv_f:
        ori_lin = row[2]
        new_lin = 'https://'+ori_lin
        img_links.append(ori_lin)
    img_links.remove(img_links[0])

    # enter current dir and create a folder
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, folder_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    os.chdir(final_directory)


    # save 2 dir, links need to be list; 2 inputs in tot
    def save2dir(links):
        for jj in links:
            ind = 0
            for ii in range(len(jj)):
                if jj[ii] == '/':
                    ind = ii
            local = str(jj[ind+1:]) + '.jpg'
            print(local)
            urllib.request.urlretrieve(jj, local)


    # divide up the total targets into all cores in computer
    cpu_num = os.cpu_count()
    por_num = 1
    if len(img_links) < cpu_num:
        por_num = len(img_links)
        por_qua = 1
        remainder = 0
    else:
        por_num = cpu_num
        por_qua = len(img_links) // (cpu_num - 1)
        remainder = len(img_links) % (cpu_num - 1)

    # create multiple processes to get links faster
    threads = []
    for i in range(por_num):
        if remainder == 0:
            t = Thread(target=save2dir, args=(img_links[(i * por_qua):((i + 1) * por_qua)],))
        else:
            if i != por_num - 1:
                t = Thread(target=save2dir, args=(img_links[(i * por_qua):((i + 1) * por_qua)],))
            else:
                t = Thread(target=save2dir, args=(img_links[(i * por_qua):(i * por_qua) + remainder],))
        t.start()
        threads.append(t)
    for j in threads:
        j.join()

    os.chdir(current_directory)
    print('Everything finished lol')