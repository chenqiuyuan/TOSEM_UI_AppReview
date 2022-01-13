"""分析ui reivew的代码

Usage:
script.py main
script.py count <file_path>
script.py analyze <file_path>
script.py analyze_ui
"""

from docopt import docopt
import pandas as pd
from colorama import Fore, Style


APP_DATA = "/mnt/d/Onedrive/Paper/UI/PaperUI/Apps_Data.csv"
APP_LIST = "/mnt/d/Onedrive/Code/UIReviewAnalysis/src/analyze/GooglePlay_app_name.txt"
ALL_UI = "/mnt/d/OneDrive - business/UI_Review/data/ALL_UI.csv"

def red(msg):
    print(Fore.RED + msg + Style.RESET_ALL)

def _get_app_data():
    # 获得app的list
    return pd.read_csv(APP_DATA)


def write_app_list(list_file=None):
    app_data = _get_app_data()
    google_apps = app_data['APP_TITLE'].str.lower()
    with open(APP_LIST, "w") as f:
        for name in google_apps:
            f.write(name + "\n")
    print("输出文件路径")
    print(APP_LIST)


def red(msg):
    print(Fore.RED + msg + Style.RESET_ALL)


def _get_ui_review():
    ui_review = pd.read_csv(ALL_UI)

    print(ui_review.columns)

    free_ui = pd.read_csv(FREE_UI)
    non_free_ui = pd.read_csv(NON_FREE_UI)
    red("Free app中的UI review的数量")
    print(len(free_ui))
    red("Non-free app中的UI review的数量")
    print(len(non_free_ui))

    all_ui = pd.concat([free_ui, non_free_ui])
    return all_ui

def is_free():
    app_data = pd.read_csv(APP_DATA)

def count_category(data):
    print("统计各个UI category （包括多标签）")
    category_dict = {
        "appearance": 0,
        "interaction": 0,
        "experience": 0,
        "others": 0,
        "FALSE": 0,
    }
    for review in data["CATEGORY"]:
        for c in str(review).split("/"):
            category_dict[c] += 1
    print(category_dict)


def count_subcategory(data):
    print("统计各个UI types（包括多标签）")
    subcategory_dict = {
        "layout": 0,
        "color": 0,
        "typography": 0,
        "iconography": 0,
        "image": 0,
        "navigation": 0,
        "notification": 0,
        "motion": 0,
        "gesture": 0,
        "accessibility": 0,
        "redundancy": 0,
        "customization limitation": 0,
        "advertisement": 0,
        "feedback": 0,
        "generic evaluation": 0,
        "comparative review": 0,
        "material": 0,
        "FALSE": 0,
    }
    total = 0
    for review in data["SUBCATEGORY"]:
        for c in str(review).split("/"):
            subcategory_dict[c] += 1
            total += 1
    print(subcategory_dict)
    print("False positive的数量以及比例")
    print(subcategory_dict["FALSE"])
    # 总共有1447
    print(subcategory_dict["FALSE"] / (subcategory_dict["FALSE"] + 1447))


if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
