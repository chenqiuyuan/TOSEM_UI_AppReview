import pandas as pd
from colorama import Fore, Style


def red(msg):
    print(Fore.RED + msg + Style.RESET_ALL)

def analyze_advice_interaction():
    red("统计Advice中interaction的数量")
    review_reply_free = pd.read_excel("review_reply_free.xlsx")
    review_reply_non_free = pd.read_excel("review_reply_non_free.xlsx")
    review_reply_all = pd.concat([review_reply_free, review_reply_non_free])
    advice = review_reply_all[review_reply_all['Reply'].str.contains("advice", na=False)]
    red("Advice的数量")
    print(len(advice))
    red("Advice中interaction的数量")
    interaction = advice[advice["Category"].str.contains("interaction", na=False)]
    print(len(interaction))
    red("Advice中interaction中navigation的数量及占比")
    navigation = interaction[interaction["Subcategory"].str.contains("navigation", na=False)]
    print(len(navigation))
    print("%.3f%%" % (len(navigation) / len(interaction) * 100))
    red("Advice中interaction中gesture的数量及占比")
    gesture = interaction[interaction["Subcategory"].str.contains("gesture", na=False)]
    print(len(gesture))
    print("%.3f%%" % (len(gesture) / len(interaction) * 100))


def analyze_advice_experience():
    red("统计Advice中experience的数量")
    review_reply_free = pd.read_excel("review_reply_free.xlsx")
    review_reply_non_free = pd.read_excel("review_reply_non_free.xlsx")
    review_reply_all = pd.concat([review_reply_free, review_reply_non_free])
    advice = review_reply_all[review_reply_all['Reply'].str.contains("advice", na=False)]
    experience = advice[advice['Category'].str.contains("experience", na=False)]

    print(len(experience))
    red("Advice中experience中customization的数量及占比")
    customization = experience[experience["Subcategory"].str.contains("customization limitation", na=False)]
    print(len(customization))
    print("%.3f%%" % (len(customization) / len(experience) * 100))

def analyze_count():
    red("以advice为例，统计不同的dialogue中，四个category和17个subcategory的各种分布")
    review_reply_free = pd.read_excel("review_reply_free.xlsx")
    review_reply_non_free = pd.read_excel("review_reply_non_free.xlsx")
    review_reply_all = pd.concat([review_reply_free, review_reply_non_free])
    advice = review_reply_all[review_reply_all['Reply'].str.contains("advice", na=False)]    
    print(advice["Category"].value_counts())
    print(advice['Subcategory'].value_counts())


    # print(free_reply)

def count_reply(data):
    print("统计各个pattern（包括多标签）")
    reply_dict = {
        "apology or appreciation": 0,
        "advice": 0,
        "information request": 0,
        "justify": 0,
        "promise": 0,
        "inform": 0,
        "unspecify": 0,
        "False": 0
    }
    total = 0
    for review in data["REPLY"]:
        for c in str(review).split("/"):
            reply_dict[c] += 1
            total += 1
    print(reply_dict)
    print("False positive的数量以及比例")
    print(reply_dict["False"])
    # print(len(all_review_reply))
    # 总共有764个数据
    print(reply_dict["False"] / (764 + reply_dict["False"]))

def count_category(data):
    print("统计各个UI category （包括多标签）")
    category_dict = {
        "appearance": 0,
        "interaction": 0,
        "experience": 0,
        "others": 0,
        "False": 0,
    }
    print(category_dict)
    for review in data["CATEGORY"]:
        for c in str(review).split("/"):
            category_dict[c] += 1
    return category_dict

if __name__ == "__main__":
    #
    analyze_count()