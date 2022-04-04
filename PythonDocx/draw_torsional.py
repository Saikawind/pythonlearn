import time

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from scipy import stats
import os

# 适配中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 中文字体设置
plt.rcParams['axes.unicode_minus'] = False


def draw_single_y(file_path, ex_index, nm_index, annotate_data_start, annotate_data_end, predict_factor,
                  predict_judge):
    global IMG_SAVE_INDEX

    def draw_annotation(annotate_data_start, annotate_data_end):
        # 330nm
        # 确定标注位置
        if nm_index == '330nm':
            intercept_startx = annotate_data_start[0] - annotate_data_start[0] * 0.4
            intercept_starty = annotate_data_start[1] + annotate_data_start[1] * 0.5

            # 确定箭头样式
            plt.annotate(str(annotate_data_start[0]) + ", " + str(annotate_data_start[1]), xy=annotate_data_start,
                         xytext=(intercept_startx, intercept_starty),
                         arrowprops=dict(arrowstyle="->", facecolor='black'))

            intercept_endx = annotate_data_end[0] - annotate_data_end[0] * 0.3
            intercept_endy = annotate_data_end[1] + annotate_data_end[1] * 0.3
            plt.annotate(str(annotate_data_end[0]) + ", " + str(annotate_data_end[1]), xy=annotate_data_end,
                         xytext=(intercept_endx, intercept_endy),
                         arrowprops=dict(arrowstyle="->", facecolor='black'))
        # 2000
        elif nm_index == '2000nm':
            intercept_startx = annotate_data_start[0] + annotate_data_start[0] * 0.5
            intercept_starty = annotate_data_start[1] - annotate_data_start[1] * 0.4
            # 确定箭头样式
            plt.annotate(str(annotate_data_start[0]) + ", " + str(annotate_data_start[1]), xy=annotate_data_start,
                         xytext=(intercept_startx, intercept_starty),
                         arrowprops=dict(arrowstyle="->", facecolor='black'))

            intercept_endx = annotate_data_end[0] + annotate_data_end[0] * 0.6
            intercept_endy = annotate_data_end[1] - annotate_data_end[1] * 0.2
            plt.annotate(str(annotate_data_end[0]) + ", " + str(annotate_data_end[1]), xy=annotate_data_end,
                         xytext=(intercept_endx, intercept_endy),
                         arrowprops=dict(arrowstyle="->", facecolor='black'))

    def draw_trendline(twist_angle, torque, ax):
        # 截取点索引
        index_start = np.where(twist_angle == annotate_data_start[0])[0][0]
        index_end = np.where(twist_angle == annotate_data_end[0])[0][0]

        x = twist_angle[index_start:index_end]
        y = torque[index_start:index_end]
        # 截取线
        plt.plot(x, y, 'coral')
        # 拟合趋势线参数
        parameter = np.polyfit(x.reshape(x.size), y.reshape(y.size), 1)  # n=1为一次函数，返回函数参数
        f = np.poly1d(parameter)  # 拼接方程
        # 计算 R^2
        slope, intercept, r_value, p_value, std_err = stats.linregress(x.reshape(x.size), y.reshape(y.size))
        # 预测趋势线
        predict_index = int(twist_angle.size * predict_factor)
        predict_start = index_start - predict_index
        predict_end = index_end + predict_index

        max_limit_index = np.where(torque == np.max(torque))[0][0]
        # 限制趋势线最大值，趋势线末端索引超过原曲线最大值索引时，末端索引改为原曲线最大值索引，防止图片比例失控
        if predict_end < max_limit_index:
            predict_x = twist_angle[predict_start:predict_end]
            predict_y = f(twist_angle[predict_start:predict_end])
        else:
            predict_x = twist_angle[predict_start:max_limit_index]
            predict_y = f(twist_angle[predict_start:max_limit_index])
            predict_end = max_limit_index

        plt.plot(predict_x, predict_y, color='coral', linestyle='--')

        # 显示趋势线函数和R值文本
        # 使用绝对值位置
        if nm_index == "330nm":
            plt.text(0.85, 1.1, "y  = {:.2f}x {:.3f}".format(slope, intercept), transform=ax.transAxes)
            plt.text(0.85, 1.05, r"R$^2$ = {:.4f}".format(r_value), transform=ax.transAxes)
        elif nm_index == "2000nm":
            plt.text(0.85, 1.1, "y  = {:.2f}x {:.3f}".format(slope, intercept), transform=ax.transAxes)
            plt.text(0.85, 1.05, r"R$^2$ = {:.4f}".format(r_value), transform=ax.transAxes)

    # 读取数据
    data_01 = pd.read_csv(file_path, encoding='GBK')
    # 划分数据
    twist_angle = np.array(data_01[[ex_index]][2:])
    torque = np.array(data_01[["UAES-车和家"]][2:])

    # 确定画布大小
    # fig = plt.figure(figsize=(10, 5))
    fig, ax = plt.subplots(figsize=(10, 5))

    plt.plot(twist_angle, torque)

    plt.xlabel("Twist angle(°)")
    plt.ylabel("Torque(N·m)")

    if predict_judge:
        # 标注
        draw_annotation(annotate_data_start, annotate_data_end)
        # 趋势线
        draw_trendline(twist_angle, torque, ax)

    # 显示网格
    plt.grid(True)
    plt.title("Stator torsional strength")

    plt.xlim(left=0)
    plt.ylim(bottom=0)

    path = "data/curve-{}".format(save_img_time)
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig("data/curve-{}/{}.png".format(save_img_time, IMG_SAVE_INDEX))
    IMG_SAVE_INDEX += 1
    # plt.show()


def draw_double_y(file_path, ex_index):
    global IMG_SAVE_INDEX
    data = pd.read_csv(file_path, encoding='GBK')

    twist_angle = np.array(data[[ex_index]][2:])
    torque = np.array(data[["UAES-车和家"]][2:])
    Time_ms = np.array(data[["1"]][2:])

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
    ax1.set_title("Stator torsional strength")

    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1))
    plt.savefig("data/curve-{}/{}.png".format(save_img_time, IMG_SAVE_INDEX))
    IMG_SAVE_INDEX += 1
    # plt.show()


IMG_SAVE_INDEX = 1
save_img_time = time.strftime("%H-%M-%S")


def draw_curve(set_ex_num, set_ex_type, predict_judge_list, predict_factor_list, annotate_data_start_list,
               annotate_data_end_list):
    # 试验数量，试验类型
    # set_ex_type = ['330', '2000']
    # ex_type_len = len(set_ex_type)
    # ex_num_index = 0
    # 试验编号
    # ex_num = 1
    # 划分数据范围
    # annotate_data_start_list = [[0.252, 130.855], [0.558, 308.7261], [0.288, 146.8931], [0.783, 378.7886]]
    # annotate_data_end_list = [[0.405, 223.0181], [1.143, 640.7573], [0.423, 226.8491], [1.197, 605.229]]
    # 是否绘制趋势线
    # predict_judge_list = [True, True, True, True]
    # 预测数值范围比例
    # predict_factor_list = [0.15, 0.15, 0.15, 0.15]
    # predict_index = 0
    # 样例数据
    # 01 330
    index = 0
    for ex_num in range(1, set_ex_num + 1):
        ex_num = str(ex_num) + "#"
        for ex_type in set_ex_type:
            predict_judge = predict_judge_list[index]
            predict_factor = predict_factor_list[index]
            # 型号
            annotate_data_start = annotate_data_start_list[index]
            annotate_data_end = annotate_data_end_list[index]
            index += 1
            # 绘图数据
            # data/dat/1#/原始数据_曲线-1#330nm-53528.dat
            file_path = "data/dat/{0}/原始数据_曲线-{0}{1}nm-53528.dat".format(ex_num, ex_type)
            draw_single_y(file_path, ex_num, ex_type, annotate_data_start, annotate_data_end, predict_factor,
                          predict_judge)
            draw_double_y(file_path, ex_num)
            # 实验编号、类型
            # ex_type = set_ex_type[ex_num_index % ex_type_len]
            # ex_num_index += 1
            # if ex_num_index == ex_type_len:
            #     ex_num += 1

    # 01 2000
    # file_path = "data/dat/1#/原始数据_曲线-1#2000nm-53528.dat"
    # predict_judge = predict_judge_list[index]
    # predict_factor = predict_factor_list[index]
    # # 实验编号、类型
    # ex_type = set_ex_type[ex_num_index % ex_type_len]
    # ex_index = str(ex_num) + "#"
    # ex_num_index += 1
    # if ex_num_index == ex_type_len:
    #     ex_num += 1
    # annotate_data_start = annotate_data_start_list[index]
    # annotate_data_end = annotate_data_end_list[index]
    # index += 1
    # draw_single_y(file_path, ex_index, ex_type, annotate_data_start, annotate_data_end, predict_factor,
    #               predict_judge)
    # draw_double_y(file_path, ex_index)
    # # 02 330
    # file_path = "data/dat/2#/原始数据_曲线-2#330nm-53528.dat"
    # predict_judge = predict_judge_list[index]
    # predict_factor = predict_factor_list[index]
    # # 实验编号、类型
    # ex_type = set_ex_type[ex_num_index % ex_type_len]
    # ex_index = str(ex_num) + "#"
    # ex_num_index += 1
    # if ex_num_index == ex_type_len:
    #     ex_num += 1
    # annotate_data_start = annotate_data_start_list[index]
    # annotate_data_end = annotate_data_end_list[index]
    # index += 1
    # draw_single_y(file_path, ex_index, ex_type, annotate_data_start, annotate_data_end, predict_factor,
    #               predict_judge)
    # draw_double_y(file_path, ex_index)
    # # 02 2000
    # file_path = "data/dat/2#/原始数据_曲线-2#2000nm-53528.dat"
    # predict_judge = predict_judge_list[index]
    # predict_factor = predict_factor_list[index]
    # # 实验编号、类型
    # ex_type = set_ex_type[ex_num_index % ex_type_len]
    # ex_index = str(ex_num) + "#"
    # ex_num_index += 1
    # if ex_num_index == ex_type_len:
    #     ex_num += 1
    # annotate_data_start = annotate_data_start_list[index]
    # annotate_data_end = annotate_data_end_list[index]
    # index += 1
    # draw_single_y(file_path, ex_index, ex_type, annotate_data_start, annotate_data_end, predict_factor,
    #               predict_judge)
    # draw_double_y(file_path, ex_index)
