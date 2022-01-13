def calculate_size(z, c, population, p=0.5):
    """
    z: 置信度
    c: 置信度
    population: 整体样本的数量
    >> calculate_size(2.58, 0.05, 9567)
    """
    # 公式来自
    # https://www.surveysystem.com/sscalc.htm#one
    # Z值和置信区间的计算
    # https://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html
    # 99%的时候用的2.58,其实也可以用2.576
    # 95%的时候用的1.96
    ss = (z ** 2) * p * (1-p) / (c ** 2)
    new_ss = ss/(1 + ((ss - 1) / population))
    return round(new_ss)

if __name__ == "__main__":
    calculate_size(2.58, 0.05, 9567)