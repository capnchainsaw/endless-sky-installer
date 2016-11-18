del EndlessSky.msi
del EndlessSky.wxs
del EndlessSky.wixobj
del EndlessSky.wixpdb
python populate_wxs.py
candle EndlessSky.wxs
light EndlessSky.wixobj
@pause