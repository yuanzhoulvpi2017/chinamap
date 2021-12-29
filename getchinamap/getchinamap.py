import geopandas as gpd
import pandas as pd
import warnings
from tqdm import tqdm
import gzip


class DownloadChmap():
    def __init__(self):
        self.raw_data = pd.read_csv(
            "https://gitee.com/yuanzhoulvpi/amap_adcode/raw/master/AMap_adcode_citycode_20210406.csv",
            dtype={'中文名': str,
                   'adcode': str,
                   'citycode': str,
                   'adcode_first': str,
                   'adcode_second': str,
                   'adcode_third': str})
        self.base_url = "https://geo.datav.aliyun.com/areas_v3/bound/geojson?code="

    def download_district(self, district_name='寿县'):
        """
        下载指定县(区) 边界数据
        """
        base_url = self.base_url
        base_data = self.raw_data.loc[self.raw_data['中文名'] == district_name].copy().reset_index(drop=True)
        if base_data.shape[0] >= 1:
            base_data = base_data.iloc[0, :]
        else:
            raise ValueError(f"$ 找不到这个县(区): {district_name} $")

        if (base_data['adcode_second'] == '00') or (base_data['adcode_third'] == '00'):
            warnings.warn(message=f"$ 你输入的地点：{district_name} 可能不是一个 县(区) $")

        district_adcode = base_data['adcode']  # .tolist()[0]
        finally_url = base_url + district_adcode
        gpd_data = gpd.read_file(filename=finally_url)
        return gpd_data

    def download_city(self, city_name='杭州市', target='边界'):
        """
        下载城市的边界或者县区
        """
        city_targetlist = ['边界', '县区']
        base_url = self.base_url
        base_data = self.raw_data.loc[self.raw_data['中文名'] == city_name].copy().reset_index(drop=True)
        if base_data.shape[0] >= 1:
            base_data = base_data.iloc[0, :]
        else:
            raise ValueError(f"$ 找不到这个城市: {city_name} $")

        if base_data['adcode_third'] != '00':
            warnings.warn(message=f"$ 你输入的地点：{city_name} 可能不是一个 城市 $")

        if city_name in ['东莞市', '中山市', '嘉峪关市']:
            target = '边界'

        district_adcode = base_data['adcode']
        if target == city_targetlist[0]:
            finally_url = base_url + district_adcode
        elif target == city_targetlist[1]:
            finally_url = base_url + district_adcode + '_full'
        else:
            raise ValueError(f"你输入的target 参数不对, 不在 {' 、'.join(city_targetlist)}")

        gpd_data = gpd.read_file(finally_url)
        return gpd_data

    def download_province(self, province_name='安徽省', target='边界'):
        province_targetlist = ['边界', '市', '县区']
        base_url = self.base_url

        if province_name == '台湾省':
            warnings.warn(message="传递的省份为 台湾省 时候 默认且只能返回 边界； 不能返回下级（市 或者 县区）")
            target = province_targetlist[0]  # 默认只能返回边界

        if province_name in ['北京市', '天津市', '上海市', '重庆市']:
            if target == province_targetlist[1]:
                warnings.warn(
                    message=f"你输入的省为：{province_name}, 属于中国4大直辖市；输入的 target为: {target} ；将target 转换为: {province_targetlist[2]}")
                target = '县区'
            return self.download_city(city_name=province_name, target=target)

        elif province_name in ['香港特别行政区', '澳门特别行政区']:
            if target == province_targetlist[1]:
                warnings.warn(
                    message=f"你输入的省为：{province_name}, 属于中国2个特别行政区；输入的 target为: {target} ；将target 转换为: {province_targetlist[2]}")
                target = '县区'
            return self.download_city(city_name=province_name, target=target)
        elif province_name in ['海南省']:
            if target == province_targetlist[1]:
                warnings.warn(
                    message=f"你输入的省为：{province_name}, 由于数据问题；输入的 target为: {target} ；将target 转换为: {province_targetlist[2]}")
                target = '县区'
            return self.download_city(city_name=province_name, target=target)

        else:

            # 找到省的数据
            base_data = self.raw_data.loc[self.raw_data['中文名'] == province_name].copy().reset_index(drop=True)

            if base_data.shape[0] >= 1:
                base_data = base_data.iloc[0, :]
            else:
                raise ValueError(f"$ 找不到这个省: {province_name} $")

            if (base_data['adcode_second'] != '00') | (base_data['adcode_third'] != '00'):
                warnings.warn(message=f"$ 你输入的地点：{province_name} 可能不是一个 省 $")

            district_adcode = base_data['adcode']

            if target == province_targetlist[0]:
                finally_url = base_url + district_adcode
                gpd_data = gpd.read_file(filename=finally_url)
                return gpd_data
            elif target == province_targetlist[1]:
                finally_url = base_url + district_adcode + '_full'
                gpd_data = gpd.read_file(filename=finally_url)
                return gpd_data
            elif target == province_targetlist[2]:
                temp_data = self.raw_data.loc[
                            (self.raw_data['adcode_first'] == base_data['adcode_first']) &
                            (self.raw_data['adcode_third'] == '00') &
                            (self.raw_data['adcode_second'] != '00'), :].copy().reset_index(drop=True)

                gpd_data = pd.concat([self.download_city(city_name=i, target='县区') for i in
                                      tqdm(temp_data['中文名'], desc=f'正在下载：{province_name} 的县区数据...')]).reset_index(
                    drop=True)

                return gpd_data

    def download_country(self, target='边界'):
        country_targetlist = ['边界', '省', '市', '县区']
        base_url = self.base_url

        if target == country_targetlist[0]:
            finally_url = base_url + '100000'
            return gpd.read_file(filename=finally_url)
        elif target == country_targetlist[1]:
            finally_url = base_url + '100000' + '_full'
            return gpd.read_file(filename=finally_url)
        elif target in country_targetlist[2:]:
            temp_data = self.raw_data.loc[
                        (self.raw_data['adcode_third'] == '00') &
                        (self.raw_data['adcode_second'] == '00') &
                        (~self.raw_data['中文名'].isin(['中华人民共和国', '外国'])), :].copy().reset_index(drop=True)

            gpd_data = pd.concat([self.download_province(province_name=i, target=target) for i in temp_data['中文名']])
            return gpd_data
        else:
            raise ValueError(f"你输入的 {target} 不在 {'、'.join(country_targetlist)} 内")

    def download_nine_segments(self):
        gpd_data = self.download_country(target='省')
        gpd_data = gpd_data.loc[gpd_data['adcode'] == '100000_JD']
        return gpd_data

    @classmethod
    def download_world(cls, filepath=None):
        """
        如果你是在中国, 不方便使用github，可以从我的gitee上下载数据,链接为：
        https://gitee.com/yuanzhoulvpi/amap_adcode/tree/master/datasets
        可以看到一个名为world_for_china.gz的文件，点击下载。
        然后可以添加路径到filepath 参数上：
        >>> data = DownloadChmap.download_world(filepath="xxxx/xxxx/xxx/world_for_china.gz")
        >>> data
        :param filepath:
        :return:
        """
        if filepath is None:
            msg = """
            如果你是在中国, 不方便使用github，可以从我的gitee上下载数据,链接为：
            https://gitee.com/yuanzhoulvpi/amap_adcode/tree/master/datasets
            可以看到一个名为world_for_china.gz的文件，点击下载。
            然后可以添加路径到filepath 参数上：
            >>> data = DownloadChmap.download_world(filepath="xxxx/xxxx/xxx/world_for_china.gz")
            >>> data
            """
            print(msg)

        else:
            with open(filepath, mode='rb') as fIn:
                data = gpd.read_file(fIn.read().decode('utf-8'))
            return data


if __name__ == '__main__':
    # test
    chinamap_engine = DownloadChmap()
    # data = chinamap_engine.download_country(target='县区')
    data = chinamap_engine.download_province(province_name='甘肃省', target='县区')
    # data = chinamap_engine.download_world()
    # data = DownloadChmap.download_world(filepath="xxxx/xxxx/xxx/world_for_china.gz")
    # print(data)
