from FeSim.database.connection import Base, engine
from FeSim.database.entities.character import Character
from FeSim.database.entities.game_class import GameClass


def main():
    Base.metadata.create_all(engine)

    print("Database initialized.")


if __name__ == "__main__":
    main()