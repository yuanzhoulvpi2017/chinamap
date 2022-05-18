# 获得中国地图数据

## 目的

本包主要是为了解决获得中国地图数据难的问题，这里提供一个python的解决方案。让大家用中国地图更加宽心、方便。

## 本包特点

1. 简单；
2. 高效；
3. 准确（相对网络上的数据，中国地图数据更加准确）；
4. 完整（数据完整，包括中国各个区域；并且可以让用户下钻到县区级别）


## 数据来源

本包查询到的数据全部来源于 阿里云的`DataV` http://datav.aliyun.com/portal/school/atlas/area_selector

因此数据基本上和高德地图保持一致；


## 使用声明

1. 请合理使用地图数据；数据内容和本人无关；数据具体用途也和本人无关；


## 使用方式

### 先安装本包

```bash
pip install getchinamap
```

### 下载依赖数据
1. 本仓库之前依靠的是阿里云发布的`AMap_adcode_citycode_20210406.csv`文件。这个文件被我经过修改，现在这个文件在这个仓库的`dataset`文件夹下。
2. 需要吧上面文件`AMap_adcode_citycode_20210406.csv`下载到本地。

### 导入包并且初始化包
```python

from getchinamap.getchinamap import DownloadChmap
# 把上面的文件路径放到这里
chinamap_engine = DownloadChmap(adcode_file="../datasets/AMap_adcode_citycode_20210406.csv")

```
### 获得县区级数据

目前县区级别的数据，只能获得县区的边界，不能获得县区下的街道、村内容。

只要使用chinamap_engine.download_district即可，里面的参数需要传递县区名称

```python
chinamap_engine.download_district(district_name='寿县')
chinamap_engine.download_district(district_name='余杭区')

```

### 获得市级数据

目前市级数据，只能获得市级的边界、县区，不能获得街道、村内容。

只要使用chinamap_engine.download_city函数。
需要传递两个参数：
1. city_name代表城市名称，比如杭州市，合肥市；
2. target代表下钻维度：边界, 县区。

```python

chinamap_engine.download_city(city_name='杭州市',target='边界')
chinamap_engine.download_city(city_name='杭州市',target='县区')


chinamap_engine.download_city(city_name='合肥市',target='边界')

```

### 获得省级数据

目前省级数据，只能获得省级的边界、市、县区，不能获得街道、村内容。
只要使用chinamap_engine.download_province函数。
需要传递两个参数:
1. province_name代表省的名字，比如浙江省，安徽省等；
2. target代表下钻维度：边界，市，县区。

```python
chinamap_engine.download_province(province_name='浙江省', target='边界')
chinamap_engine.download_province(province_name='浙江省', target='市')
chinamap_engine.download_province(province_name='浙江省', target='县区')

chinamap_engine.download_province(province_name='安徽省', target='边界')
chinamap_engine.download_province(province_name='安徽省', target='市')

```

### 获得国家级数据

目前国家级数据，只能获得国家级的边界、省、市、县区，不能获得街道、村内容。(默认国家为中国）。
只要使用chinamap_engine.download_country函数。
需要传递一个参数：
1. target代表下钻维度：边界，省，市，县区。

```python
chinamap_engine.download_country(target='边界')
chinamap_engine.download_country(target='省')
chinamap_engine.download_country(target='市')
chinamap_engine.download_country(target='县区') # 建议少用

```

### 获得南海九段线

如果需要添加九段线，可以使用这个函数，获得九段线数据即可。

```python

chinamap_engine.download_nine_segments()

```