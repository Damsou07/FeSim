import sys

from PySide6.QtWidgets import QApplication

from FeSim.controllers.character_controller import CharacterController
from FeSim.controllers.game_class_controller import GameClassController
from FeSim.database.connection import Base, engine, get_session
from FeSim.database.repositories.character_repository import CharacterRepository
from FeSim.database.repositories.game_class_repository import GameClassRepository
from FeSim.services.character_service import CharacterService
from FeSim.services.game_class_service import GameClassService
from FeSim.ui.game_class_view import GameClassView
from FeSim.ui.main_window import MainWindow
from FeSim.ui.style import DARK_THEME


def main():
    Base.metadata.create_all(engine)
    session = get_session()

    # ── Repositories ────────────────────────────────────────────────
    character_repo = CharacterRepository(session)
    game_class_repo = GameClassRepository(session)

    # ── Services ────────────────────────────────────────────────────
    character_service = CharacterService(character_repo, game_class_repo)
    game_class_service = GameClassService(game_class_repo)

    # ── Qt app ──────────────────────────────────────────────────────
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    window = MainWindow()

    # ── Game-class view (page 1 of the stack) ───────────────────────
    gc_view = GameClassView()
    window.stack.addWidget(gc_view)
    gc_ctrl = GameClassController(gc_view, game_class_service)

    # ── Character controller ────────────────────────────────────────
    char_ctrl = CharacterController(window, character_service)

    # ── Navigation ──────────────────────────────────────────────────
    window.navigate_to_classes.connect(
        lambda: (window.show_classes_view(), gc_ctrl._refresh())
    )
    window.navigate_back.connect(window.show_character_view)

    window.show()
    exit_code = app.exec()
    session.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
