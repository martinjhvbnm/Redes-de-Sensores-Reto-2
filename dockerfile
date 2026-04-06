FROM osrf/ros:jazzy-desktop

# 1. Instalación de dependencias (Pasos 3-5)
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# 2. Espacio de trabajo (Paso 6)
WORKDIR /ros2_ws/src

# 3. CREACIÓN DEL PAQUETE (Paso 7)
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && \
    ros2 pkg create --build-type ament_python sensor_program --license MIT"

# 4. COPIAR TUS SCRIPTS
COPY ./carpetacomp/*.py /ros2_ws/src/sensor_program/sensor_program/

# 5. REEMPLAZAR EL SETUP.PY
RUN echo "from setuptools import find_packages, setup\n\
package_name = 'sensor_program'\n\
setup(\n\
    name=package_name,\n\
    version='0.0.0',\n\
    packages=find_packages(exclude=['test']),\n\
    data_files=[\n\
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),\n\
        ('share/' + package_name, ['package.xml']),\n\
    ],\n\
    install_requires=['setuptools'],\n\
    zip_safe=True,\n\
    entry_points={\n\
        'console_scripts': [\n\
            'sensor_node = sensor_program.sensor_node:main',\n\
            'reader_node = sensor_program.reader_node:main',\n\
            'plotter_node = sensor_program.plotter_node:main',\n\
        ],\n\
    },\n\
)" > /ros2_ws/src/sensor_program/setup.py

# 6. COMPILACIÓN AUTOMÁTICA (Paso 8)
WORKDIR /ros2_ws
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

# 7. SOURCE AUTOMÁTICO
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]