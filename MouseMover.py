#!/usr/bin/env python3
"""
Programa para mover el ratón periódicamente y evitar la suspensión del sistema.
Diseñado para macOS.
"""

import time
import pyautogui
import argparse
import signal
import sys
from datetime import datetime


class MouseMover:
    def __init__(self, interval=60):
        self.interval = interval
        self.running = True
        self.move_count = 0

        # Configurar pyautogui
        pyautogui.FAILSAFE = True  # Mover ratón a esquina superior izquierda para detener

    def signal_handler(self, signum, frame):
        """Maneja la señal de interrupción (Ctrl+C)"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Deteniendo el programa...")
        self.running = False

    def move_mouse(self):
        """Mueve el ratón ligeramente"""
        try:
            # Obtener posición actual
            current_x, current_y = pyautogui.position()

            # Mover ligeramente (1 pixel) y volver a la posición original
            pyautogui.moveRel(1, 0, duration=0.1)  # Mover 1 pixel a la derecha
            time.sleep(0.1)
            pyautogui.moveRel(-1, 0, duration=0.1)  # Volver a la posición original

            self.move_count += 1
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] Movimiento #{self.move_count} - Posición: ({current_x}, {current_y})")

        except pyautogui.FailSafeException:
            print("\n[FAILSAFE] Mouse movido a esquina superior izquierda. Deteniendo programa.")
            self.running = False
        except Exception as e:
            print(f"Error al mover el ratón: {e}")

    def run(self):
        """Ejecuta el bucle principal"""
        # Configurar manejador de señales
        signal.signal(signal.SIGINT, self.signal_handler)

        print(f"🖱️  Iniciando MouseMover...")
        print(f"⏰ Intervalo: {self.interval} segundos")
        print(f"🛑 Para detener: Ctrl+C o mover ratón a esquina superior izquierda")
        print(f"📅 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)

        try:
            while self.running:
                self.move_mouse()

                # Esperar el intervalo especificado
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)

        except KeyboardInterrupt:
            pass

        print(f"\n✅ Programa finalizado. Total de movimientos: {self.move_count}")


def main():
    parser = argparse.ArgumentParser(
        description="Mueve el ratón periódicamente para evitar la suspensión del sistema"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        help="Intervalo en segundos entre movimientos (por defecto: 60)"
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Modo de prueba (5 movimientos con intervalo de 3 segundos)"
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Modo de prueba activado")
        mover = MouseMover(interval=3)
        # En modo test, solo hacer 5 movimientos
        original_run = mover.run

        def test_run():
            count = 0
            while mover.running and count < 5:
                mover.move_mouse()
                count += 1
                if count < 5:
                    time.sleep(3)
            print("\n✅ Prueba completada")

        mover.run = test_run
    else:
        mover = MouseMover(interval=args.interval)

    mover.run()


if __name__ == "__main__":
    main()