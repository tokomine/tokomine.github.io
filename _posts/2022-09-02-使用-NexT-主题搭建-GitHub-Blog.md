---
title: 使用 NexT 主题搭建 GitHub Blog
# description: 使用 NexT 主题搭建 GitHub Blog
# date: 2022-09-02
categories:
- 笔记
tags:
- 主题
---

## 教程地址
[theme-next.simpleyyt.com](http://theme-next.simpleyyt.com/getting-started.html) 

## 本地调试
```shell
bundle exec jekyll server
```

## 提交新文章
执行命令
```
python newpost.py 文 章 名 称
```

脚本
```
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

```