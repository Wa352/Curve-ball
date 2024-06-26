import math
import tkinter as t
import numpy as np
import plotly.graph_objects as go

# 入力ウィンドウを作成
inputer = t.Tk()
inputer.title("入力画面")
inputer.geometry("1000x1000")

# ラベルとエントリーウィジェットの作成と配置
rpm_label = t.Label(inputer, text="回転数[rpm]")
rpm_label.place(x=10, y=10, width=150, height=20)
rpm_entry = t.Entry(inputer)
rpm_entry.place(x=150, y=10, width=100, height=20)

speed_label = t.Label(inputer, text="速度[m/s]")
speed_label.place(x=10, y=30, width=150, height=20)
speed_entry = t.Entry(inputer)
speed_entry.place(x=150, y=30, width=100, height=20)

theta_x_label = t.Label(inputer, text="変化軸x[°]")
theta_x_label.place(x=10, y=50, width=150, height=20)
theta_x_entry = t.Entry(inputer)
theta_x_entry.place(x=150, y=50, width=100, height=20)

theta_y_label = t.Label(inputer, text="変化軸y[°]")
theta_y_label.place(x=10, y=70, width=150, height=20)
theta_y_entry = t.Entry(inputer)
theta_y_entry.place(x=150, y=70, width=100, height=20)

theta_z_label = t.Label(inputer, text="変化軸z[°]")
theta_z_label.place(x=10, y=90, width=150, height=20)
theta_z_entry = t.Entry(inputer)
theta_z_entry.place(x=150, y=90, width=100, height=20)

air_label = t.Label(inputer, text="空気密度[kg/m³]")
air_label.place(x=10, y=110, width=150, height=20)
air_entry = t.Entry(inputer)
air_entry.insert(0, "1.225")
air_entry.place(x=150, y=110, width=100, height=20)

radius_label = t.Label(inputer, text="半径[m]")
radius_label.place(x=10, y=130, width=150, height=20)
radius_entry = t.Entry(inputer)
radius_entry.insert(0, "0.037")
radius_entry.place(x=150, y=130, width=100, height=20)

mass_label = t.Label(inputer, text="質量[kg]")
mass_label.place(x=10, y=150, width=150, height=20)
mass_entry = t.Entry(inputer)
mass_entry.insert(0, "0.145")
mass_entry.place(x=150, y=150, width=100, height=20)

distance_label = t.Label(inputer, text="飛行距離[m]")
distance_label.place(x=10, y=170, width=150, height=20)
distance_entry = t.Entry(inputer)
distance_entry.insert(0, "18.44")
distance_entry.place(x=150, y=170, width=100, height=20)

point_label = t.Label(inputer, text="高さ[m]")
point_label.place(x=10, y=190, width=150, height=20)
point_entry = t.Entry(inputer)
point_entry.place(x=150, y=190, width=100, height=20)
#ボタンを押したとき、実行する関数
def start():
    try:
        #入力ウィンドウからの数値の読み込み
        rpm = float(rpm_entry.get())
        speed = float(speed_entry.get())
        theta_x = float(theta_x_entry.get())
        theta_y = float(theta_y_entry.get())
        theta_z = float(theta_z_entry.get())
        air_density = float(air_entry.get())
        radius = float(radius_entry.get())
        mass = float(mass_entry.get())
        distance = float(distance_entry.get())
        point = float(point_entry.get())
        #角速度やマグヌス効果による各軸おおもとの加速度(a_beta)の計算
        theata_speed = (rpm * 2 * math.pi) / 60
        a = math.pi * (radius ** 2)
        c = (2 * math.pi * radius * theata_speed) / 40
        f = 0.5 * air_density * a * c * (speed ** 2)
        a_beta = f / mass
        #ユーザー入力による角度による各軸加速度の計算
        ax = a_beta * math.sin(math.radians(theta_x))
        ay = a_beta * -1 * math.sin(math.radians(theta_y))
        az = a_beta * -1 * math.sin(math.radians(theta_z))
        #時間データのリスト化
        dt = 0.1
        t_max = distance / speed
        times = np.arange(0, t_max, dt)
        ball_size=radius*2
        #初速度及び初期位置データの入力
        vx0 = 0
        vy0 = 0
        vz0 = speed
        x0 = 0
        y0 = point
        z0 = 0
        #速度データのリスト化
        vx = vx0 + ax * times
        vy = vy0 + ay * times
        vz = vz0 + az * times
        #座標データのリスト化
        x = x0 + vx0 * times + 0.5 * ax * times**2
        y = y0 + vy0 * times + 0.5 * ay * times**2
        z = z0 + vz0 * times + 0.5 * az * times**2
        #アニメーションの作成
        frames = []
        for i in range(len(times)):
            frames.append(go.Frame(data=[
                go.Scatter3d(x=x[:i+1], y=z[:i+1], z=y[:i+1], mode="lines+markers", marker=dict(size=ball_size)),
            ]))

        fig = go.Figure(
            data=[
                go.Scatter3d(x=[x0], y=[z0], z=[y0], mode='lines+markers', marker=dict(size=ball_size)),
                
            ],
            layout=go.Layout(
                scene=dict(
                    xaxis=dict(range=[-max(x), max(x)], autorange=False, title="垂直方向"),
                    yaxis=dict(range=[0, distance], autorange=False, title="ベース方向"),
                    zaxis=dict(range=[0, max(y)], autorange=False, title="高さ"),
                    bgcolor="rgb(230, 230,230)",
                    aspectratio=dict(x=2*max(abs(x)), y=abs(distance), z=abs(max(y)))
                ),
                title="変化球シミュレーション",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play", method="animate", args=[None])]
                )]
            ),
            frames=frames
        )
        fig.show()
    #入力項目が足らなかった際のエラー表示
    except ValueError:
        print("無効な入力値があります。全てのフィールドに数値を入力してください。")
#計算ボタンの表示、押した場合は関数startを実行
button = t.Button(inputer, text="計算", command=start)
button.place(x=10, y=250, width=100, height=30)
#入力ウィンドウの表示
inputer.mainloop()


