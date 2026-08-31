from PySide6.QtWidgets import QMessageBox


def confirm_delete(parent=None, name: str = "") -> bool:
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle("Supprimer le personnage")
    box.setText(f"Voulez-vous vraiment supprimer « {name} » ?")
    box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    box.setDefaultButton(QMessageBox.StandardButton.No)
    return box.exec() == QMessageBox.StandardButton.Yes
