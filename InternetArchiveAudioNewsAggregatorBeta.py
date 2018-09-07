#this code returns a string of the page location's code

import requests
import datetime
import random

def page_to_string(url):
    page = requests.get(url).text
    return page

#this function retrieves item file names from a chunk of text

def isolate_itemname(codechnk):
    newlst = []
 
    for ctr in range(len(codechnk)):
        if codechnk[ctr] == "h" and codechnk[ctr+1] == "r" and codechnk[ctr+2] == "e" and codechnk[ctr+3] == "f":
            newchk = codechnk[ctr:]
            for ct in range(len(newchk)):
                if newchk[ct] == "t" and newchk[ct+1] == "i" and newchk[ct+2] == "t" and newchk[ct+3] == "l":
                    newnum = ct - 2
                    newstchk = newchk[:newnum]
                    numa = newstchk.count("href")
                    if numa == 1 and (len(newstchk)<75):
                        newmon = newstchk[6:]  
                        newerm = "https://archive.org" + newmon 
                        numb = newerm.count("archive")
                        if numb == 1 and "?sor" not in newerm and "title" not in newerm:                
                            newlst.append(newerm)
    return newlst

#this function sends each of the netlabel's pages to have item files retrieved and turned into a list

def retrieve_pages(labelname, pgs, schtm, schtm2):
    medfnl = []
    for num1 in range(pgs):
        catr = num1+1
        ctr = str(catr)
        if schtm == "":
            schstr = ""
        if schtm != "":
            schstr = "and%5B%5D=" + schtm
        if schtm2 != "":
            tmptm = "+" + schtm2
            schstr += tmptm
        url =  "https://archive.org/details/" + labelname + "?" + schstr + "&sort=-publicdate&page=" + ctr 
        print("Reading: " + url)  
        bigstr = (page_to_string(url))
        medstr = isolate_itemname(bigstr)
        for itm in medstr:
            if "VOA" not in itm:
                medfnl.append(itm)
    return medfnl

#this function creates urls for the item download pages

def convert_itemname_list(lst, nm):
    trnlst = []
    for item in lst:
        ast = item[:20]
        bst = "download"
        cst = item[27:]
        dst = ast + bst + cst
        trnlst.append(dst)
    print("")
    print(trnlst)
    print("")
    return trnlst

#this function makes a list of item titles

def make_itemtitle_list(last):
    nmlst = []
    for elem in last:
        atr = elem[28:]
        nmlst.append(atr)
    return nmlst

#this function retrieves mp3 file names from a chunk of text

def isolate_filename(codechnk, itmnm, typ):
    newlst = []
 
    for ctr in range(len(codechnk)):
        if codechnk[ctr] == "h" and codechnk[ctr+1] == "r" and codechnk[ctr+2] == "e" and codechnk[ctr+3] == "f":
            newchk = codechnk[ctr:]
            for ct in range(len(newchk)):
                if typ != "j" and newchk[ct] == "." and newchk[ct+1] == "m" and newchk[ct+2] == "p" and newchk[ct+3] == typ:
                    newnum = ct + 4
                    newstchk = newchk[:newnum]
                    searchstr = ".mp" + typ
                    numa = newstchk.count(searchstr)
                    numb = newstchk.count("href=")
                    ctr = 0
                    if (numa == 1) and (numb == 1) and ("_64kb" not in newstchk) and ("_vbr" not in newstchk) and (len(newstchk)<100):
                        newmon = newstchk[6:]   
                        newrl = "https://archive.org/download" + itmnm + "/" + newmon               
                        newlst.append(newrl)
                if typ == "j" and newchk[ct] == "." and newchk[ct+1] == "j" and newchk[ct+2] == "p" and newchk[ct+3] == "g":
                    newnum = ct + 4
                    newstchk = newchk[:newnum]
                    searchstr = ".jpg"
                    numa = newstchk.count(searchstr)
                    numb = newstchk.count("href=")
                    ctr = 0
                    if (numa == 1) and (numb == 1) and ("glogo" not in newstchk) and ("_thumb" not in newstchk) and (len(newstchk)<100):
                        newmon = newstchk[6:]   
                        newrl = "https://archive.org/download" + itmnm + "/" + newmon               
                        newlst.append(newrl)
    print("")
    print(newlst)
    print("")
    return newlst

#this code takes a list as an argument and removes redundant elements from that list

def remove_duplicates(x):
    y = list(set(x))
    return y

#this code writes a list into a file

def write_list_to_file(outname, lstname, typ, srch):
    if typ == "3":
        wrtstr = ".m3u"
    if typ == "4":
        wrtstr = ".txt"
    if typ == "j":
        wrtstr = ".txt"
    outnm = outname + "_" + srch + wrtstr

    outfile = open(outnm, "w")

    leng = str(len(lstname))

    outfile.write('Total Items: ' + leng + '\n')

    for elem in range(len(lstname)):
        outln = lstname[elem]
        try:
            outfile.write(outln + '\n')
        except:
            print("This item did not save due to an error:" + outln)

    outfile.close()

#this function writes a text file as a wpl

def write_wpl_code(wrtnm, conlst):
    outfile = open(wrtnm, "w")
    outfile.write("<?wpl version='1.0'?>" + '\n')
    outfile.write("<smil>" + '\n')
    outfile.write("    <head>"+ '\n')
    outfile.write("        <meta name='Generator' content='Microsoft Windows Media Player -- 12.0.17134.48'/>"+ '\n')
    outfile.write("        <meta name='ItemCount' content='0'/>"+ '\n')
    outfile.write("        <title>" + wrtnm + "</title>"+ '\n')
    outfile.write("    </head>"+ '\n')
    outfile.write("    <body>"+ '\n')
    outfile.write("        <seq>"+ '\n')
    for elem in conlst:
        outfile.write("            <media src=" + "'" + elem + "'" + "/>" + '\n')
    outfile.write("        </seq>"+ '\n')
    outfile.write("    </body>"+ '\n')
    outfile.write("</smil>"+ '\n')
    outfile.close()

#this code retrieves the date and time from the computer, to create the timestamp

def retrieve_date():
    right_now = datetime.datetime.now().isoformat()
    list = []

    for i in right_now:
        if i.isnumeric():
           list.append(i)

    tim = ("".join(list))
    return tim

#this code writes a list into a file

def write_list_to_htmlfile(outname, lstname, srch):

    outnm = outname + "_" + srch + ".html"

    outfile = open(outnm, "w")

    leng = str(len(lstname))

    outfile.write("Here are links to items from the search " + outname + " " + srch + "<br><br>" + '\n')

    outfile.write("Total Items: " + leng + "<br><br>" + '\n')

    for elem in range(len(lstname)):
        outln = lstname[elem]
        outln2 = "<a href = '" + outln + "'>" + outln + "</a><br>"
        try:
            outfile.write(outln2 + '\n')
        except:
            print("This item did not save due to an error:" + outln)

    outfile.close()

    return outnm

#this function returns a random variant of a list

def retrieve_random_elements(inlist, numoutlines):

    outlines = []

    for num1 in range(numoutlines):
        num2 = random.randrange(len(inlist))
        outlines.append(inlist[num2])
    
    return outlines

#this code writes the mp3 to a local file

def write_list_to_mp3(ur, titl):
    print("")
    print("Downloading mp3 from: " + ur)
    ur2 = ""
    urb = ur[29:]
    for elem in urb:
        if elem.isalpha() or elem.isnumeric() or elem == ".":
            ur2 += elem
    ur3 = '/Users/mysti/Downloads/' + titl + "_" + ur2
    r = requests.get(ur)
    with open(ur3, 'wb') as f:
        f.write(r.content)


# this is the main function. It gathers and sends the necessary data to proceed.

def main():
    print("")
    print("This is an original program by Thomas Park. It allows you to topical news broadcasts from collections of free media that have been posted to the Internet Archive. The archive is based on Creative Commons file protocol, so files are free to access and share. Some may not be free to sell, or to use for commercial purposes. Others may not be available to alter. All are free to play.")
    print("")
    print("To use this program, you must choose a number of pages to search (there are a maximum of 75 items per page). The search will retrieve .mp3 files.")
    print("")
    print("You may also choose up to 2 search terms to refine your search. Each must be one word, with no spaces.")
    print("")
    print("When you are finished, this program will create and store 3 files-- one will be an .m3u of links for each file found, another will be a .wpl file, which will render the files playable in a Windows Media Player. A third file will be an .html file featuring links to each .mp3")
    print("")
    print("The .m3u files should work in most players, but the other formats require the Windows Media Player.")
    print("")
    print("The purpose of this program is to provide access to free culture. Thomas Park does not necessarily own or have license for any of this culture, and he is neither altering nor making profits by creation or use of this program.")
    print("")
    sear = input("You can enter two search terms. They must be sets of characters with no spaces. What is the first? If none, press enter: ")
    print("")
    sear2 = input("You can enter two search terms. They must be sets of characters with no spaces. What is the second? If none, press enter: ")
    print("")
    ans1 = "audio"
    ans2 = int(input("How many pages shall we search? "))
    print("")
    typi = "m"
    typ = "3"
    print("")
    lstend = retrieve_pages(ans1, ans2, sear, sear2)
    print("")
    print(lstend)
    print("")
    print("Total items in collection: ")
    print("")
    totm3u = []
    lster = convert_itemname_list(lstend, ans1)
    namlst = make_itemtitle_list(lster)
    ctr = 0
    for elem in lster:
        pgchk = page_to_string(elem)
        itmnm = namlst[ctr]
        print("Reading: " + elem)
        allmp3 = isolate_filename(pgchk, itmnm, typ)
        fnlmp3 = remove_duplicates(allmp3)
        for item in fnlmp3:
            totm3u.append(item)
        ctr += 1
    print("")
    print(totm3u)
    print("")
    print("Total files written to playlist:", len(totm3u))
    timest = retrieve_date()
    serch = sear + "_" + sear2 + "_" + timest
    write_list_to_file(ans1, totm3u, typ, serch)
    nm = ans1 + "_" + serch + ".wpl"
    nm2 = ans1 + "_" + serch
    write_wpl_code(nm, totm3u)
    write_list_to_htmlfile(ans1, totm3u, serch)
    if typ == "3":
        print("")
        print("Three files have been created.  One is an .m3u, a second is a .wpl, and a third is an .html of file links. They are saved in the same directory as this program.")
        print("")
        ansn = input("Would you like to download a random set of mp3s from this batch? They will be saved to your Downloads folder. Enter y if yes: ")
        if ansn == "y":
            ansn2 = int(input("How many mp3s would you like to download?: "))
            lt2 = retrieve_random_elements(totm3u, ansn2)
            for elem in lt2:
                write_list_to_mp3(elem, nm2)
    if typ == "4" or typ == "j":   
        print("")
        print("Three files have been created.  One is a .txt, one is a .wpl, and a third is an .html of file links. They are saved in the same directory as this program.")


## THE GHOST OF THE SHADOW ##

if __name__ == "__main__":
   main()


