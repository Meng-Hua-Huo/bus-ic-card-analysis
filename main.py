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

def calculate_phf(df):
    """任务4：高峰小时系数(PHF)计算"""
    print("=" * 30 + " 开始任务 4 " + "=" * 30)

    # 自动识别高峰小时
    hourly_volume = df.groupby('hour').size()
    peak_h = hourly_volume.idxmax()
    V60 = hourly_volume.max()  # 高峰小时总流量

    # 筛选高峰小时内的所有记录
    df_peak = df[df['hour'] == peak_h].copy()

    # 计算15分钟粒度最大流量
    df_peak['bin_15'] = df_peak['交易时间'].dt.minute // 15
    V15_max = df_peak.groupby('bin_15').size().max()

    # 计算5分钟粒度最大流量
    df_peak['bin_5'] = df_peak['交易时间'].dt.minute // 5
    V5_max = df_peak.groupby('bin_5').size().max()

    # 代入PHF公式计算
    phf_15 = V60 / (4 * V15_max) if V15_max > 0 else 1.0
    phf_5 = V60 / (12 * V5_max) if V5_max > 0 else 1.0

    # 格式化输出
    print(f"【4. 高峰小时系数计算结果】")
    print(f" 高峰时段: {peak_h}:00 - {peak_h}:59")
    print(f" 高峰小时总流量(V60)   : {V60} 次")
    print(f" 最大15分钟流量(V15_max): {V15_max} 次")
    print(f" 最大5分钟流量(V5_max) : {V5_max} 次")
    print(f" PHF15 (15分钟粒度)   : {phf_15:.3f}")
    print(f" PHF5  (5分钟粒度)    : {phf_5:.3f}")
    print("-" * 50)

    return {"peak_hour": peak_h, "PHF15": phf_15, "PHF5": phf_5}

def export_route_driver_info(df, output_dir='线路驾驶员信息', target_count=20):
    """批量导出线路-车辆-驾驶员关系"""

    # 防止空表传入
    if df.empty:
        raise ValueError("❌ 数据为空！请检查任务1/2是否误删了全部记录。")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 统一列名与数据类型
    df_exp = df.copy()
    # 将关键列统一转为字符串并去除首尾空格
    for col in ['线路号', '车辆编号', '驾驶员编号']:
        if col in df_exp.columns:
            df_exp[col] = df_exp[col].astype(str).str.strip()
        else:
            # 兼容不同CSV列名写法
            alt_names = {'线路号': ['线路', 'RouteID'], '车辆编号': ['车号', 'VehicleID'],
                         '驾驶员编号': ['司机', 'DriverID']}
            for alt in alt_names.get(col, []):
                if alt in df_exp.columns:
                    df_exp.rename(columns={alt: col}, inplace=True)
                    df_exp[col] = df_exp[col].astype(str).str.strip()
                    break

    # 获取目标线路
    all_routes = sorted(df_exp['线路号'].unique())
    target_routes = all_routes[:target_count]
    print(f" 数据集中共 {len(all_routes)} 条线路，本次将导出前 {target_count} 条: {target_routes}")

    export_count = 0
    # 遍历生成TXT
    for route_id in target_routes:
        group = df_exp[df_exp['线路号'] == route_id]
        # 提取唯一对应关系
        mapping = group[['车辆编号', '驾驶员编号']].drop_duplicates()

        if mapping.empty:
            print(f" 跳过线路 {route_id}：无有效车辆/驾驶员数据")
            continue

        # 严格命名与写入
        file_path = os.path.join(output_dir, f"{route_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"线路号: {route_id}\n")
            f.write("车辆编号\t驾驶员编号\n")
            for _, row in mapping.iterrows():
                f.write(f"{row['车辆编号']}\t{row['驾驶员编号']}\n")
        export_count += 1

    print(f"【任务5完成】在 '{output_dir}'生成 {export_count} 个txt文件。")
    return export_count

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
        calculate_phf(df_clean)
        export_route_driver_info(df_clean)


    except Exception as e:
        print(f" 程序运行中断: {e}")
        print(" 建议：检查ICData.csv路径、列名是否匹配，或终端上方报错信息。")
