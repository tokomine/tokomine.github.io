#encoding=utf8

import sys
import time

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("需要填写文章标题")
    nowdate = time.localtime()
    dateformat = time.strftime("%Y-%m-%d", nowdate)
    timeformat = time.strftime("%Y-%m-%d %H:%M:%S", nowdate)

    title = '-'.join(sys.argv[1:])
    name = ' '.join(sys.argv[1:])
    filename = dateformat + "-" + title + ".md"
    with open("_posts/" + filename, "w") as file:
        file.write("---\n")
        file.write("title: " + name + "\n")
        file.write("date: " + timeformat + "\n")
        file.write("categories:\n")
        file.write("tags:\n")
        file.write("---\n")
