# BiliPixelDrawer

Bilibili夏日绘板活动的BS架构多人协作脚本

## 服务端的安装

后台采用Django，请自行创建pixelapp应用，然后将pixelapp文件夹内容导入即可

## 客户端的使用

1. 先去服务器填写用户名和项目申请token
1. 进入活动页面，在脚本中填写对应服务器地址和token，开始即可

## Utils

- bitmap.py:下载当前bitmap
- checkpixel.py:检查是否有像素点被污染（写成cron即为自动脚本）
- img2bmp.py:将一张图转换成对应的pixel图片（可能出现（严重的）失真）