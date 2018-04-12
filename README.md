# changeImagePixel
随机修改图片像素，改变图片哈希值

随机选取若干个点，将rgb值+1/-1，重新保存。（会记录本次修改结果，后面可恢复成原来的rgb值）。
每次修改均会恢复上一次修改的值，然后重新修改，避免多次修改后，rgb值和原值差距太大。

1.安装python3
  https://www.python.org
2.安装库Pillow
  pip3 install Pillow

3.修改文件
imgPath = "目录／文件"  # 要修改的目录／文件
restoreAndModify = 1  # 1：恢复之前的像素值，并修改   0：只恢复
modifyNum = 5         # 随机选取像素点的个数
