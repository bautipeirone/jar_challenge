"""Launch único del equipo (reglamento §9.1).

Este es el archivo que la organización lanza en la corrida:

    ros2 launch equipo_jar competencia.launch.py

Tiene que levantar TODO el software del equipo y quedarse esperando a que el
juez publique el mapa en /map. No mueve al robot ni publica reportes antes.

`victimas` es la cantidad de víctimas a buscar (N). La organización la informa en el lugar, antes de
cada corrida, y se pasa así:  ros2 launch equipo_jar competencia.launch.py victimas:=N

`use_sim_time` es false por defecto porque el robot real no publica /clock
(§7.3). En el simulador se pasa en true (lo hacen tools/correr_simulador.sh y
el CI).

`evasor` (true por defecto) permite apagar el evasor para teleoperar en las pruebas:
    ros2 launch equipo_jar competencia.launch.py evasor:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    params = os.path.join(
        get_package_share_directory('equipo_jar'), 'params', 'params.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time')
    victimas = LaunchConfiguration('victimas')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('victimas', default_value='5',
                              description='cantidad de víctimas a buscar (N)'),
        DeclareLaunchArgument('evasor', default_value='true',
                              description='false para teleoperar sin que el evasor se pelee'),
        Node(   # equipo_jar
            package='equipo_jar',
            executable='nodo_equipo',
            name='nodo_equipo',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
                'cantidad_victimas': ParameterValue(victimas, value_type=int),
            }],
        ),
        Node(   # detector_scan
            package='equipo_jar',
            executable='detector_scan',
            name='detector_scan',
            output='screen',
            parameters=[params, {
                    'use_sim_time': use_sim_time,
                }
            ],
        ),
        Node(   # localizador
            package='equipo_jar',
            executable='localizador',
            name='localizador',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(   # campo_verosimilitud
            package='equipo_jar',
            executable='campo_verosimilitud',
            name='campo_verosimilitud',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(   # detector_obstaculos
            package='equipo_jar',
            executable='detector_obstaculos',
            name='detector_obstaculos',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(   # gestor_victimas
            package='equipo_jar',
            executable='gestor_victimas',
            name='gestor_victimas',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(   # evasor
            package='equipo_jar',
            executable='evasor',
            name='evasor',
            output='screen',
            parameters=[params, {
                'use_sim_time': use_sim_time,
            }],
            condition=IfCondition(LaunchConfiguration('evasor')),
        )
    ])
