from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(name='getchinamap',  # 包名
      version='1.0.5',  # 版本号
      description='get china map data from Amap',
      long_description=long_description,
      author='yuanzhoulvpi2017',
      author_email='1582034172@qq.com',
      url='https://github.com/yuanzhoulvpi2017/chinamap',
      install_requires=['tqdm', 'pandas', 'geopandas'],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )
