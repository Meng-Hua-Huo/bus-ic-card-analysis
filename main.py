import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']        # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False          # 正常显示负号

import pandas as pd
import numpy as np
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'ICData.csv')

def task1_preprocessing(csv_path='ICData.csv'):
    """任务1：数据预处理"""

    # 读取数据
    df = pd.read_csv(DATA_PATH, sep=',')
    print("【1. 数据读取完成】")
    print(df.head(5), "\n")  # 打印前5行

    print("【2. 数据集基本信息】")
    df.info()  # 输出行数、列数、各列数据类型
    print("-" * 50)

    # 转为datetime并提取整数小时
    df['交易时间'] = pd.to_datetime(df['交易时间'])
    df['hour'] = df['交易时间'].dt.hour.astype(int)  # 确保为整数类型
    print("【3. 时间解析完成】已新增 'hour' 列（整数型）")

    # 构造衍生字段并删除异常记录
    df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
    rows_before = len(df)
    df = df[df['ride_stops'] != 0].copy()  # 避免后续操作报警告
    rows_deleted = rows_before - len(df)
    print(f"【4. 异常清洗完成】删除 ride_stops=0 的记录共 {rows_deleted} 行")

    # 检查缺失值
    print("\n【5. 缺失值检查】")
    print(df.isnull().sum())

    missing_total = df.isnull().sum().sum()
    if missing_total > 0:
        print(f"\n>>> 处理策略：发现 {missing_total} 个缺失值，采用【直接删除含缺失值的行】策略，避免干扰后续统计。")
        df = df.dropna().reset_index(drop=True)
        print(f"处理完毕，当前剩余有效数据: {len(df)} 行")
    else:
        print("\n>>> 未发现缺失值，跳过处理步骤。")

    print("-" * 50)
    return df


def task2_time_distribution(df):
    """任务2：时间分布分析 """
    print("=" * 30 + " 开始任务 2 " + "=" * 30)

    # 筛选有效刷卡类型，并提取 hour 列转为 numpy 数组
    df_type0 = df[df['刷卡类型'] == 0].copy()
    hours_arr = df_type0['hour'].to_numpy()
    total_swipes = len(hours_arr)

    # 早晚时段刷卡量统计
    early_count = np.sum(hours_arr < 7)  # 早7点前
    late_count = np.sum(hours_arr >= 22)  # 晚22点后

    # 计算占比并打印
    early_ratio = (early_count / total_swipes) * 100 if total_swipes > 0 else 0
    late_ratio = (late_count / total_swipes) * 100 if total_swipes > 0 else 0

    print(f"【2(a) 早晚时段统计结果】")
    print(f" 早7点前刷卡量: {early_count} 次 (占比 {early_ratio:.2f}%)")
    print(f" 晚22点后刷卡量: {late_count} 次 (占比 {late_ratio:.2f}%)")
    print(f" 全天总刷卡量: {total_swipes} 次")
    print("-" * 50)

    # 构造 24 小时分布数据
    unique_hours, counts = np.unique(hours_arr, return_counts=True)
    hourly_counts = np.zeros(24, dtype=int)
    hourly_counts[unique_hours] = counts  # 将实际出现的频次映射到对应小时索引

    # 绘制 24 小时分布柱状图
    plt.figure(figsize=(12, 6))
    plt.bar(np.arange(24), hourly_counts, color='skyblue', edgecolor='black', alpha=0.8)

    # 配置坐标轴与样式
    plt.title('24小时刷卡量分布图', fontsize=15, fontweight='bold')
    plt.xlabel('小时 (0-23)', fontsize=12)
    plt.ylabel('刷卡量 (次)', fontsize=12)
    plt.xticks(np.arange(0, 24, 2))  # X轴刻度步长为2
    plt.grid(axis='y', linestyle='--', alpha=0.6)  # 开启Y轴网格线

    # 保存图像并清理画布
    plt.tight_layout()
    plt.savefig('hour_distribution.png', dpi=150, bbox_inches='tight')
    print(" 【2(b) 可视化完成】图像已保存为 hour_distribution.png")
    plt.show()
    plt.close()  # 释放内存，防止影响后续任务绘图

    print("=" * 30 + " 任务 2 结束 " + "=" * 30)


def analyze_route_stops(data_df):
    """任务3：计算各线路 ride_stops 的均值与标准差"""
    #  按线路号分组，计算均值和标准差
    route_stats = data_df.groupby('线路号')['ride_stops'].agg(['mean', 'std']).reset_index()

    # 若某线路仅1条记录，std会返回NaN，必须填充为0否则绘图报错
    route_stats['std'] = route_stats['std'].fillna(0)

    # . 按均值降序排序，使图表从上到下由高到低
    route_stats = route_stats.sort_values('mean', ascending=False).reset_index(drop=True)
    return route_stats


def plot_route_stops(route_stats_df):
    """任务3可视化：绘制带误差棒的水平条形图"""
    plt.figure(figsize=(10, 8))

    # seaborn水平条形图
    sns.barplot(data=route_stats_df, x='线路号', y='mean', hue='线路号',
                palette='viridis', errorbar='sd', legend=False)

    # 图表元素配置
    plt.title('各线路平均搭乘站点数分布', fontsize=15, fontweight='bold')
    plt.xlabel('线路号', fontsize=12)
    plt.ylabel('平均搭乘站点数', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)  # 水平条形图通常配Y轴网格辅助读数

    # 保存与释放资源
    plt.tight_layout()
    plt.savefig('route_stops.png', dpi=150, bbox_inches='tight')
    print("【任务3可视化完成】图像已保存为 route_stops.png")
    plt.show()
    plt.close()

# 执行预处理
if __name__ == "__main__":
    try:
        # 数据预处理
        df_clean = task1_preprocessing('ICData.csv')

        # 数据有效性校验 & 流程串联
        if df_clean is not None and not df_clean.empty:
            print("\n 任务1成功完成，数据已清洗。开始执行任务2...")
            task2_time_distribution(df_clean)  # 传入清洗后的DataFrame
            print("\n 任务2执行完毕！请检查根目录是否生成 hour_distribution.png")
        else:
            print(" 警告：任务1返回空数据或失败，已跳过任务2。")

        route_stats = analyze_route_stops(df_clean)
        plot_route_stops(route_stats)

    except Exception as e:
        print(f" 程序运行中断: {e}")
        print(" 建议：检查ICData.csv路径、列名是否匹配，或终端上方报错信息。")
