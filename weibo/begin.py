from scrapy import cmdline

cmd_str = "scrapy crawl weibo"
cmdline.execute(cmd_str.split(' '))