from setuptools import find_packages, setup

package_name = 'yolodetect'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shoaib-ubuntu',
    maintainer_email='mohammad.shoaib3786@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "imgpublish_node=yolodetect.imgPublish_node:main",
            "imgdisplay_node=yolodetect.imgDisplay_node:main"
        ],
    },
)
