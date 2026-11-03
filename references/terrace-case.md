# Sainte-Adresse 案例

## 图源与适用范围
作品为莫奈 1867 年《Terrace at Sainte-Adresse》，馆藏名称为 Garden at Sainte-Adresse。参考图来自 https://commons.wikimedia.org/wiki/File:Garden_at_Sainte-Adresse_MET_DT48.jpg 。

脚本以此副本的完整画幅为坐标依据。输入须为相同构图、相同边界的图像。更换为裁切图、带画框照片或另一幅画时必须重做所有坐标和遮罩。原图副本未打包。

## 已有反馈
旗帜和海浪的幅度获得认可，第五版花草获得认可。用户继续要求人物更生动、右下男性增加动作、云明显向右飘动、烟雾避免波纹式扭曲、移除两侧留边。第七版仅代表最近交付，尚未获得最终验收。

## 复现
依赖 Python、NumPy、Pillow、opencv-python。FFmpeg 可通过 --ffmpeg 指定，或安装 imageio-ffmpeg 供自动查找。按当前环境的安装权限配置依赖，优先复用已安装工具。

在 skill 目录运行下面命令，替换输入和输出路径。

    python scripts/render_terrace.py --input /path/to/reference.jpg --output /path/to/wallpaper.mp4 --ffmpeg /path/to/ffmpeg

输出为 10 秒、1430 × 1080、30 fps、无声 H.264 MP4，完整画幅无额外侧边。先编码至 .partial.mp4，完整解码通过后替换最终输出。请使用新版本文件名以保留旧版。

## 实现与边界
脚本使用第七版的花草与环境参数、人物多边形轮廓和支点旋转。人物保持二维轮廓，背景露出区域采用局部修补。其完整骨骼、三维转头、手指握持及精确投影尚未实现。云烟采用顺风平移与叠化，可能出现叠影。花草仍是局部约束变形，未逐根精细分割。

脚本不代表通用油画自动分层器。SKILL.md 中的关节绑定、接触约束和严格视觉验收是制作目标，应按新画作与实际工具落实。复现结果需要视觉预览，完整解码与循环首尾断言不足以证明自然程度。
