import argparse

from bot.event_handlers import EventHandler


def main():
    """CLI para procesar los commits y detectar los incidentes"""

    parser = argparse.ArgumentParser(
        description="ChatOps de incidentes:bot que gobierna Kanban y PR's",
        epilog='Uso: python bot/main.py --commit-msg "incident: API timeout"',
    )

    parser.add_argument(
        "--commit-msg", help="Mensaje de commit a procesar", required=True
    )

    args = parser.parse_args()

    # Crear handler y procesar
    handler = EventHandler()
    result = handler.handle_commit(args.commit_msg)

    if result is None:
        print(" No es un commit de incidente")
    else:
        print("[INFO] Incidente detectado:")
        print(f" Título: {result['title']}")
        print(f" Severidad: {result['severity']}")


if __name__ == "__main__":
    main()
