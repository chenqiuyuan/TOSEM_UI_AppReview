"""分析pull request的代码

Usage:
script.py main
script.py count <file_path>
script.py analyze <file_path>
"""
from docopt import docopt
import json
import pandas as pd
from pprint import pprint
from colorama import Fore, Style
import keywords_search


FILE_NAME = '/mnt/d/Onedrive/Code/UIReviewAnalysis/src/crawler/output/Fdroid_issue.txt'
LOG_PATH = '/mnt/d/Onedrive/Code/UIReviewAnalysis/src/crawler/output/Fdroid_logs.txt'
LIST_PATH = '/mnt/d/Onedrive/Code/UIReviewAnalysis/src/crawler/Fdroid_owner_repo.txt'
FDROID_README = "/mnt/d/Onedrive/Code/UIReviewAnalysis/src/crawler/output/Fdroid_readme.txt"
KEYWORDS = "/mnt/d/Onedrive/Code/UIReviewAnalysis/src/analyze/keywords.txt"



def red(msg):
    print(Fore.RED + msg + Style.RESET_ALL)


def count(file_path=None):
    file_path = FILE_NAME if not file_path else file_path
    # data = pd.read_json(file_path, lines=True)
    data, app_list = get_google_play_in_fdroid_data()
    red('数据的字段')
    pprint(data.columns.tolist())
    red('Issue + Pull Request总量')
    pprint(len(data))
    red('Pull request的数量')
    pull_request = data[data['types'] == "pull_request"]
    pprint(len(pull_request))
    red('Issue的数量')
    issue = data[data['types'] == "issue"]
    pprint(len(issue))
    red('App的数量')
    apps = list(set([x.split('issues/')[0] for x in data['issue_url']]))
    pprint(len(apps))


def process_log(log_path=None):
    log_path = LOG_PATH if not log_path else log_path
    logs = []
    with open(log_path, encoding="gbk") as f:
        for line in f.readlines():
            logs.append(line.strip())
    red("Fdroid包含的所有的（有GitHub地址的）app数量")
    pprint(len(logs))
    finished = 0
    counts_404 = 0
    for log in logs:
        if 'HttpError code 404' in log:
            counts_404 += 1
        else:
            finished += 1
    red("爬取到的项目")
    pprint(finished)
    red("不存在的项目")
    pprint(counts_404)


def process_list(list_path=None):
    list_path = LIST_PATH if not list_path else list_path
    projects = []
    with open(list_path) as f:
        for line in f.readlines():
            if "/" in line:
                projects.append(line)
    red("官方提供的（有GitHub地址的）app数量")
    pprint(len(projects))


def search_ui_issue_and_pr(keywords_file=None):
    keywords_file = KEYWORDS if not keywords_file else keywords_file
    red("搜索并分析UI相关的pull request和issue")
    data, _ = get_google_play_in_fdroid_data()
    string_concatenation(data)
    sentences = data['title'] + '\n' + data['text']
    keywords = keywords_search.get_keywords(keywords_file)
    red("UI关键词数量")
    print(len(keywords))
    data['sentences'] = sentences
    data_ui, _ = keywords_search.search_dataframe(data, 'sentences', keywords)
    red("搜索出来的UI相关的数量")
    print(len(data_ui))
    red("UI相关的占比")
    ratio = float(len(data_ui) / len(data) * 100)
    print("%.3f%%" % ratio)
    return data_ui


def count_ui_issue_and_pr(data, data_ui):
    ui_pull_request = data_ui[data_ui['types'] == "pull_request"]
    pull_request = data[data['types'] == "pull_request"]
    ui_issue = data_ui[data_ui['types'] == "issue"]
    issue = data[data['types'] == "issue"]
    red("搜索出来的UI相关的pull request数量以及占比")
    print(len(ui_pull_request))
    print("%.3f%%" % (len(ui_pull_request) / len(pull_request) * 100))
    red("Open的pull request及占比")
    open_pull_request = ui_pull_request[ui_pull_request["state"] == "open"]
    print(len(open_pull_request))
    print("%.3f%%" % (len(open_pull_request) / len(ui_pull_request) * 100))
    red("Closed的pull request及占比")
    closed_pull_request = ui_pull_request[ui_pull_request["state"] == "closed"]
    print(len(closed_pull_request))
    print("%.3f%%" % (len(closed_pull_request) / len(ui_pull_request) * 100))
    red("搜索出来的UI相关的issue数量以及占比")
    print(len(ui_issue))
    print("%.3f%%" % (len(ui_issue) / len(issue)))
    red("Open的issue及占比")
    open_issue = ui_issue[ui_issue["state"] == "open"]
    print(len(open_issue))
    print("%.3f%%" % (len(open_issue) / len(ui_issue) * 100))
    red("Closed的issue及占比")
    closed_issue = ui_issue[ui_issue["state"] == "closed"]
    print(len(closed_issue))
    print("%.3f%%" % (len(closed_issue) / len(ui_issue) * 100))
    return ui_pull_request, ui_issue


def string_concatenation(data):
    # 将titile 和内容结合一下,pd的+可以直接完成拼接。
    red("小测试：pandas中两个column的字符可以直接完成拼接")
    temp = data[:1]
    red("字符A")
    print(temp['title'][0])
    red("字符B")
    print(temp['text'][0])
    temp_sentences = temp['title'] + '\n' + temp['text']
    red("字符A+B data['title'] + '\\n' + data['text']")
    print(temp_sentences[0])


def _get_data():
    data = pd.read_json(FILE_NAME, lines=True)
    return data


def _get_google_play_in_fdroid_app_list():
    # 从爬取下来的readme中找google play关键词，确定是否也在google play中
    readme = pd.read_json(FDROID_README, lines=True)
    googles = readme[readme['content'].str.lower().str.contains("google play")]
    return googles['owner_repo'].to_list()


def get_google_play_in_fdroid_data():
    # 同时存在于google play和fdroid的app数量
    data = _get_data()
    app_list = _get_google_play_in_fdroid_app_list()
    res = data[data['owner_repo'].isin(app_list)]
    red("同时存在于Google Play和Fdroid中的app的数量")
    print(len(app_list))
    return res, app_list


def main():
    print("this is main function, test")


if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    if args['main']:
        main()
    elif args['count']:
        count(args['<file_path>'])
    elif args['analyze']:
        count_ui_issue_and_pr(args['<file_path>'])
