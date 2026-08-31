import sys

from PySide6.QtWidgets import QApplication

from FeSim.controllers.character_controller import CharacterController
from FeSim.database.connection import Base, engine, get_session
from FeSim.database.repositories.character_repository import CharacterRepository
from FeSim.database.repositories.game_class_repository import GameClassRepository
from FeSim.services.character_service import CharacterService
from FeSim.ui.main_window import MainWindow
from FeSim.ui.style import DARK_THEME


def main():
    # ------------------------------------------------------------------
    # Database initialization
    # ------------------------------------------------------------------

    Base.metadata.create_all(engine)

    session = get_session()

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------

    character_repository = CharacterRepository(session)
    game_class_repository = GameClassRepository(session)

    character_service = CharacterService(
        character_repository,
        game_class_repository,
    )

    # ------------------------------------------------------------------
    # Qt application
    # ------------------------------------------------------------------

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    window = MainWindow()

    controller = CharacterController(
        window,
        character_service,
    )

    window.show()

    # ------------------------------------------------------------------
    # Application event loop
    # ------------------------------------------------------------------

    exit_code = app.exec()

    session.close()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
