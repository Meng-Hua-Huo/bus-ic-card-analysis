import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']        # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False          # 正常显示负号

import pandas as pd
import numpy as np


def task1_preprocessing(csv_path='ICData.csv'):
    """任务1：数据预处理"""

    # 读取数据
    df = pd.read_csv(r'/bus-ic-card-analysis/data/ICData.csv', sep=',')
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


# 执行预处理
if __name__ == "__main__":
    df_clean = task1_preprocessing()
    # 预览处理后的数据结构
    print("\n预处理后DataFrame结构预览：")
    print(df_clean.head())
