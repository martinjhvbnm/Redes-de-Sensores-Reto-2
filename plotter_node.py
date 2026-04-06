import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import matplotlib.pyplot as plt
import re
import os

class PlotterNode(Node):

    def __init__(self):
        super().__init__('plotter_node')

        print("Plotter iniciado")

        # Suscripción al topic
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.listener_callback,
            10
        )

        # Lista de datos
        self.temps = []

        # Contador de mensajes
        self.msg_count = 0

        # Carpeta donde se guardará la imagen
        self.save_path = '/ros2_ws/src/sensor_program/sensor_program'
        os.makedirs(self.save_path, exist_ok=True)

        # Timer cada 5 segundos
        self.timer = self.create_timer(5.0, self.save_plot)

    def listener_callback(self, msg):
        self.msg_count += 1

        self.get_logger().info(f"Mensaje #{self.msg_count}: {msg.data}")
        print(f" Mensaje #{self.msg_count}: {msg.data}")

        try:
            # Extraer número del mensaje
            numbers = re.findall(r'\d+\.\d+|\d+', msg.data)

            if numbers:
                temp = float(numbers[0])
                self.temps.append(temp)

        except Exception as e:
            self.get_logger().error(f"Error al procesar dato: {e}")
            print(f" Error: {e}")

    def save_plot(self):
        print("Guardando...")

        if len(self.temps) < 2:
            self.get_logger().info("Esperando más datos...")
            print("Esperando más datos...")
            return

        try:
            plt.figure()
            plt.plot(self.temps)

            plt.title("Temperatura")
            plt.xlabel("Muestras")
            plt.ylabel("Valor")

            #  Nombre FIJO → se sobrescribe siempre
            filename = 'sensor_plot.png'
            full_path = os.path.join(self.save_path, filename)

            plt.savefig(full_path)
            plt.close()

            self.get_logger().info(f"Mensajes recibidos: {self.msg_count}")
            self.get_logger().info(f"Gráfico actualizado en {full_path}")

            print(f"Mensajes recibidos: {self.msg_count}")
            print(f"Gráfico actualizado en {full_path}")

        except Exception as e:
            self.get_logger().error(f"Error al guardar gráfico: {e}")
            print(f" Error guardando gráfico: {e}")


def main(args=None):
    rclpy.init(args=args)

    node = PlotterNode()

    print("Nodo en ejecución...")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()