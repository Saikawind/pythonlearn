import time

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from scipy import stats
import os
import matplotlib.dates as mdates

# 适配中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 中文字体设置
plt.rcParams['axes.unicode_minus'] = False


# 全局变量

def draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge):
    def draw_single_y(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor,
                      predict_judge):
        global IMG_SAVE_INDEX

        # 读取数据
        data_01 = pd.read_csv(file_path, encoding='GBK')
        # 划分数据
        twist_angle = np.array(data_01[data_01.columns[1]][2:])
        torque = np.array(data_01[data_01.columns[0]][2:])

        # 确定画布大小
        # fig = plt.figure(figsize=(10, 5))
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.plot(twist_angle, torque)

        plt.xlabel("Twist angle(°)")
        plt.ylabel("Torque(N·m)")

        # 显示网格
        plt.grid(True)
        plt.title("Static torsional strength test")

        plt.xlim(left=0)
        plt.ylim(bottom=0)

        path = "data/curve-{}-EN".format(save_img_time)
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig("data/curve-{}-EN/{}.png".format(save_img_time, IMG_SAVE_INDEX))
        IMG_SAVE_INDEX += 1
        # plt.show()
        plt.close()

    def draw_double_y(file_path):
        global IMG_SAVE_INDEX
        data = pd.read_csv(file_path, encoding='GBK')

        twist_angle = np.array(data[data.columns[1]][2:])
        torque = np.array(data[data.columns[0]][2:])
        Time_ms = np.array(data[data.columns[2]][2:])

        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(111)
        # 左y轴
        l1 = ax1.plot(Time_ms, torque, 'coral', label='Torque(N·m)')

        torque_max = torque.max()
        # 设置刻度范围
        ax1.set_ylim([0, torque_max + torque_max * 0.05])
        # 设置坐标轴指标
        ax1.set_xlabel("Time(ms)")
        ax1.set_ylabel("Torque(N·m)")

        ax2 = plt.twinx()
        ax2.set_ylabel("Twist angle(°)")
        # 右y轴
        l2 = ax2.plot(Time_ms, twist_angle, label='Twist angle(°)')
        twist_angle_max = twist_angle.max()
        # 设置坐标轴刻度范围
        ax2.set_xlim(left=0)
        ax2.set_ylim([0, twist_angle_max + twist_angle_max * 0.2])
        # 设置刻度间隔
        # ax2.xaxis.set_major_locator(MultipleLocator(10000))

        ax1.grid(True)
        ax1.set_title("Static torsional strength test")

        fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1))
        plt.savefig("data/curve-{}-EN/{}.png".format(save_img_time, IMG_SAVE_INDEX))
        IMG_SAVE_INDEX += 1
        # plt.show()
        plt.close()

    draw_single_y(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor,
                  predict_judge)
    draw_double_y(file_path)


def draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge):
    def draw_single_y(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor,
                      predict_judge):
        global IMG_SAVE_INDEX

        # 读取数据
        data_01 = pd.read_csv(file_path, encoding='GBK')
        # 划分数据
        twist_angle = np.array(data_01[data_01.columns[1]][2:])
        torque = np.array(data_01[data_01.columns[0]][2:])

        # 确定画布大小
        # fig = plt.figure(figsize=(10, 5))
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.plot(twist_angle, torque)

        plt.xlabel("Twist angle(°)")
        plt.ylabel("Torque(N·m)")

        # 显示网格
        plt.grid(True)
        plt.title("Static torsional strength test")

        ax.xaxis.set_ticks_position('top')  # 将x轴的位置设置在顶部
        # ax.invert_xaxis()  # x轴反向
        ax.yaxis.set_ticks_position('right')  # 将y轴的位置设置在右边
        # ax.invert_yaxis()  # y轴反向

        plt.xlim(right=0)
        plt.ylim(top=0)

        path = "data/curve-{}-EN".format(save_img_time)
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig("data/curve-{}-EN/{}.png".format(save_img_time, IMG_SAVE_INDEX))
        IMG_SAVE_INDEX += 1
        # plt.show()
        plt.close()

    def draw_double_y(file_path):
        global IMG_SAVE_INDEX
        data = pd.read_csv(file_path, encoding='GBK')

        twist_angle = np.array(data[data.columns[1]][2:])
        torque = np.array(data[data.columns[0]][2:])
        Time_ms = np.array(data[data.columns[2]][2:])

        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(111)
        # 左y轴
        l1 = ax1.plot(Time_ms, torque, 'coral', label='Torque(N·m)')

        torque_min = torque.min()
        # 设置坐标轴指标
        ax1.set_xlabel("Time(ms)")
        ax1.set_ylabel("Torque(N·m)")
        # 反转坐标轴
        ax1.xaxis.set_ticks_position('top')  # 将x轴的位置设置在顶部
        # ax1.invert_xaxis()  # x轴反向
        ax1.yaxis.set_ticks_position('left')  # 将y轴的位置设置在右边
        # ax.invert_yaxis()  # y轴反向
        # 设置刻度范围
        ax1.set_ylim([torque_min + torque_min * 0.1, 0])
        ax1.set_xlim(left=0)

        ax2 = plt.twinx()
        ax2.set_ylabel("Twist angle(°)")
        # 右y轴
        l2 = ax2.plot(Time_ms, twist_angle, label='Twist angle(°)')
        twist_angle_min = twist_angle.min()
        # 反转坐标轴
        ax2.yaxis.set_ticks_position('right')  # 将y轴的位置设置在右边
        # 设置坐标轴刻度范围
        ax2.set_ylim([twist_angle_min + twist_angle_min * 0.1, 0])
        ax2.set_xlim(left=0)

        # 设置刻度间隔
        # ax2.xaxis.set_major_locator(MultipleLocator(10000))

        ax1.grid(True)
        ax1.set_title("Static torsional strength test")

        # fig.legend(loc='upper right', bbox_to_anchor=(0.5, 0.5))
        fig.legend(bbox_to_anchor=(0.9, 0.12))
        plt.savefig("data/curve-{}-EN/{}.png".format(save_img_time, IMG_SAVE_INDEX))
        IMG_SAVE_INDEX += 1
        # plt.show()
        plt.close()

    draw_single_y(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor,
                  predict_judge)
    draw_double_y(file_path)


def draw_heat_curve(file_path, ex_index, year, month, day):
    global IMG_SAVE_INDEX

    # 读取数据
    data_01 = pd.read_csv(file_path, encoding='GBK')
    # 划分数据
    Time = np.array(data_01[data_01.columns[0]])
    Temperature_left = np.array(data_01[data_01.columns[1]])
    Temperature_offside = np.array(data_01[data_01.columns[2]])

    # 确定画布大小
    fig, ax = plt.subplots(figsize=(10, 5))
    day_end = day + 1
    next_day = False
    for i in range(Time.size):
        if Time[i] == "0:00":
            next_day = True
        if not next_day:
            Time[i] = pd.to_datetime("{}/{}/{} {}".format(year, month, day, Time[i]))
        else:
            Time[i] = pd.to_datetime("{}/{}/{} {}".format(year, month, day_end, Time[i]))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.plot(Time, Temperature_left, label='左侧 left')
    ax.plot(Time, Temperature_offside, label='右侧 offside')

    plt.xlabel(
        "Time({year}/{month}/{day} {start}-{year}/{month}/{day_end} {end}".format(year=year, month=month, day=day,
                                                                                  day_end=day_end,
                                                                                  start=Time[0],
                                                                                  end=Time[-1]))
    plt.ylabel("Temperature(℃)")

    # 显示网格
    plt.grid(True)
    plt.title("{}升温曲线 Heating curve".format(ex_index))

    # plt.xlim(left=0)
    plt.ylim(bottom=0)

    path = "data/curve-{}-EN".format(save_img_time)
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig("data/curve-{}-EN/{}.png".format(save_img_time, IMG_SAVE_INDEX))
    IMG_SAVE_INDEX += 1
    # 设置曲线图例显示
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1))
    # plt.show()
    plt.close()


IMG_SAVE_INDEX = 1
save_img_time = time.strftime("%H-%M-%S")


def draw_curve_en(set_ex_num, set_ex_type_list_transfer):
    set_ex_type_list = []
    for ex_type_trans in set_ex_type_list_transfer:
        ex_type_trans = ex_type_trans.replace("_", "-")
        set_ex_type_list.append(ex_type_trans.replace("minus", "-"))
    for ex_num in range(1, set_ex_num + 1):
        for ex_type in set_ex_type_list:
            # 预测数值范围比例
            predict_factor = 0.15
            file_path = "data/en_ver_dat/{0}/曲线-{0}#{1}nm-53528.dat".format(ex_num, ex_type)
            predict_judge = False
            annotate_data_start = []
            annotate_data_end = []
            if (ex_type[0] == "-" and ex_type != "-1900-100") or ex_type == "1900-100":
                draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
            else:
                draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)

    for ex_num in range(1, set_ex_num + 1):
        # 01 Heating_curve
        file_path = "data/en_ver_dat/{0}/{0}#N样品升温数据.dat".format(ex_num)
        # 试验序号
        ex_index = str(ex_num) + "#"
        year = 2021
        month = 11
        day = 9
        draw_heat_curve(file_path, ex_index, year, month, day)

    # # 01 -545-10nm
    # file_path = "data/en_ver_dat/1/曲线-1#-545-10nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-545-10nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 545-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#545-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "545-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 -545-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#-545-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-545-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 1000-10nm
    # file_path = "data/en_ver_dat/1/曲线-1#1000-10nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "1000-10nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 -1000-10nm
    # file_path = "data/en_ver_dat/1/曲线-1#-1000-10nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-1000-10nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 1000-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#1000-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "1000-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 -1000-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#-1000-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-1000-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 1500-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#1500-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "1500-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 -1500-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#-1500-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-1500-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 1900-100nm 的图形数据好像反了？
    # # 01 1900-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#1900-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "1900-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    #
    # # 01 -1900-100nm
    # file_path = "data/en_ver_dat/1/曲线-1#-1900-100nm-53528.dat"
    # predict_judge = False
    # # 型号
    # ex_type = "-1900-100nm"
    # annotate_data_start = []
    # annotate_data_end = []
    # # draw_invert(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
    # draw_first(file_path, ex_type, annotate_data_start, annotate_data_end, predict_factor, predict_judge)
