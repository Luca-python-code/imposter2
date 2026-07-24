import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QLineEdit, QListWidget, QStackedWidget, 
    QFrame, QMessageBox, QGraphicsDropShadowEffect, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# Begriffspools mit Kategorien für die Imposter-Hinweis-Option
BEGRIFFE_MIT_KATEGORIEN = {
    "Obst & Essen": ["Banane", "Pizza", "Wassermelone", "Eiscreme", "Ananas"],
    "Geräte & Technik": ["Kaffeemaschine", "Kühlschrank", "Zahnbürste"],
    "Sommer & Strand": ["Fallschirm", "Sonnenbrille", "Strand", "Pool", "Hängematte", "Surfbrett"],
    "Fahrzeuge & Orte": ["U-Boot", "Gitarre", "Sommer", "Taucherbrille"]
}

STYLESHEET = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                stop:0 #0052D4, 
                                stop:0.4 #4364F7, 
                                stop:0.8 #00D2FF, 
                                stop:1 #00F2FE);
}

/* Nutzt die universelle Standard-Systemschriftart */
QWidget {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Glassmorphism Card Container */
QFrame#Card {
    background-color: rgba(10, 25, 50, 0.35);
    border: 2px solid rgba(0, 242, 254, 0.5);
    border-radius: 30px;
}

QLabel {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: bold;
}

QLabel#TitleLabel {
    font-size: 38px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: 2px;
}

QLabel#SubtitleLabel {
    font-size: 15px;
    color: #A0E9FF;
    font-weight: bold;
}

QLabel#SecretWordLabel {
    font-size: 34px;
    font-weight: 900;
    color: #00F2FE;
    background-color: rgba(5, 15, 35, 0.6);
    border: 2px solid rgba(0, 242, 254, 0.6);
    border-radius: 20px;
    padding: 18px;
}

QLabel#ImposterLabel {
    font-size: 32px;
    font-weight: 900;
    color: #FF416C;
    background-color: rgba(30, 0, 10, 0.65);
    border: 2px solid rgba(255, 65, 108, 0.7);
    border-radius: 20px;
    padding: 18px;
}

QLineEdit {
    background-color: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(0, 242, 254, 0.4);
    border-radius: 16px;
    padding: 12px 18px;
    font-size: 16px;
    color: #FFFFFF;
    font-weight: bold;
}

QLineEdit::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

QLineEdit:focus {
    border: 2px solid #00F2FE;
    background-color: rgba(255, 255, 255, 0.25);
}

QCheckBox {
    color: #E0F7FA;
    font-size: 15px;
    font-weight: bold;
    spacing: 10px;
}

QCheckBox::indicator {
    width: 24px;
    height: 24px;
    border-radius: 8px;
    border: 2px solid rgba(0, 242, 254, 0.6);
    background-color: rgba(0, 0, 0, 0.2);
}

QCheckBox::indicator:checked {
    background-color: #00F2FE;
    border: 2px solid #FFFFFF;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00C6FF, stop:1 #0072FF);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 22px;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: 900;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00F2FE, stop:1 #4364F7);
    border: 2px solid #FFFFFF;
}

QPushButton:pressed {
    background-color: #0052D4;
}

QPushButton#SecondaryBtn {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.4);
    color: #E0F7FA;
}

QPushButton#SecondaryBtn:hover {
    background: rgba(255, 255, 255, 0.3);
    color: #FFFFFF;
}

QListWidget {
    background-color: rgba(5, 15, 35, 0.5);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 18px;
    padding: 10px;
    font-size: 16px;
    color: #FFFFFF;
    font-weight: bold;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid rgba(0, 242, 254, 0.15);
    border-radius: 10px;
}

QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00C6FF, stop:1 #0072FF);
    color: #FFFFFF;
}
"""

def add_glow(widget, color_hex="#00F2FE", radius=25):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    qcolor = QColor(color_hex)
    qcolor.setAlpha(120)
    shadow.setColor(qcolor)
    widget.setGraphicsEffect(shadow)

class ImposterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMPOSTER")
        # 9:16 Format
        self.resize(405, 720)
        self.setMinimumSize(405, 720)
        
        self.players = []
        self.secret_word = ""
        self.current_category = ""
        self.imposter = ""
        self.imposter_gets_clue = False
        
        self.current_player_idx = 0
        self.current_clue_idx = 0
        
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(STYLESHEET)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Screens
        self.setup_screen = self.create_setup_screen()
        self.pass_screen = self.create_pass_screen()
        self.reveal_screen = self.create_reveal_screen()
        self.clue_screen = self.create_clue_screen()
        self.vote_screen = self.create_vote_screen()
        self.guess_screen = self.create_guess_screen()
        self.result_screen = self.create_result_screen()
        
        self.stacked_widget.addWidget(self.setup_screen)
        self.stacked_widget.addWidget(self.pass_screen)
        self.stacked_widget.addWidget(self.reveal_screen)
        self.stacked_widget.addWidget(self.clue_screen)
        self.stacked_widget.addWidget(self.vote_screen)
        self.stacked_widget.addWidget(self.guess_screen)
        self.stacked_widget.addWidget(self.result_screen)
        
    def create_card(self):
        card = QFrame()
        card.setObjectName("Card")
        add_glow(card, color_hex="#000000", radius=35)
        return card

    # --- 1. SETUP SCREEN ---
    def create_setup_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 25, 22, 25)
        
        title = QLabel("IMPOSTER")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("by Luca")
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        
        input_layout = QHBoxLayout()
        self.player_input = QLineEdit()
        self.player_input.setPlaceholderText("Spielername...")
        self.player_input.returnPressed.connect(self.add_player)
        
        add_btn = QPushButton("+")
        add_btn.setFixedWidth(55)
        add_btn.clicked.connect(self.add_player)
        add_glow(add_btn, "#00C6FF", 15)
        
        input_layout.addWidget(self.player_input)
        input_layout.addWidget(add_btn)
        
        self.player_list = QListWidget()
        
        remove_btn = QPushButton("Ausgewählten entfernen")
        remove_btn.setObjectName("SecondaryBtn")
        remove_btn.clicked.connect(self.remove_player)
        
        # Checkbox für Imposter-Hinweis
        self.clue_checkbox = QCheckBox("Imposter erhält Kategorie-Hinweis")
        self.clue_checkbox.setChecked(False)
        
        start_btn = QPushButton("SPIEL STARTEN 🚀")
        start_btn.clicked.connect(self.start_game)
        add_glow(start_btn, "#00F2FE", 25)
        
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(12)
        card_layout.addLayout(input_layout)
        card_layout.addWidget(self.player_list)
        card_layout.addWidget(remove_btn)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.clue_checkbox)
        card_layout.addSpacing(12)
        card_layout.addWidget(start_btn)
        
        layout.addWidget(card)
        return widget

    def add_player(self):
        name = self.player_input.text().strip()
        if name:
            if name in self.players:
                QMessageBox.warning(self, "Fehler", "Name ist bereits vorhanden!")
            else:
                self.players.append(name)
                self.player_list.addItem(name)
                self.player_input.clear()

    def remove_player(self):
        selected_items = self.player_list.selectedItems()
        for item in selected_items:
            self.players.remove(item.text())
            self.player_list.takeItem(self.player_list.row(item))

    def start_game(self):
        if len(self.players) < 3:
            QMessageBox.warning(self, "Zu wenige Spieler", "Ihr braucht mindestens 3 Spieler!")
            return
        
        self.current_category = random.choice(list(BEGRIFFE_MIT_KATEGORIEN.keys()))
        self.secret_word = random.choice(BEGRIFFE_MIT_KATEGORIEN[self.current_category])
        
        self.imposter = random.choice(self.players)
        self.imposter_gets_clue = self.clue_checkbox.isChecked()
        self.current_player_idx = 0
        
        self.show_pass_screen()

    # --- 2. PASS PHONE SCREEN ---
    def create_pass_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        icon_label = QLabel("📱")
        icon_label.setStyleSheet("font-size: 65px;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        self.pass_label = QLabel("")
        self.pass_label.setObjectName("TitleLabel")
        self.pass_label.setWordWrap(True)
        self.pass_label.setAlignment(Qt.AlignCenter)
        
        sub = QLabel("Stelle sicher, dass niemand sonst auf den Bildschirm schaut!")
        sub.setWordWrap(True)
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #B0BEC5;")
        
        ready_btn = QPushButton("ICH BIN BEREIT")
        ready_btn.clicked.connect(self.show_reveal_screen)
        add_glow(ready_btn, "#00F2FE", 25)
        
        card_layout.addWidget(icon_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.pass_label)
        card_layout.addWidget(sub)
        card_layout.addStretch()
        card_layout.addWidget(ready_btn)
        
        layout.addWidget(card)
        return widget

    def show_pass_screen(self):
        player_name = self.players[self.current_player_idx]
        self.pass_label.setText(f"Gib das Gerät an\n{player_name}")
        self.stacked_widget.setCurrentWidget(self.pass_screen)

    # --- 3. REVEAL ROLE SCREEN ---
    def create_reveal_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        self.reveal_player_title = QLabel("")
        self.reveal_player_title.setObjectName("TitleLabel")
        self.reveal_player_title.setAlignment(Qt.AlignCenter)
        
        self.role_box = QLabel("")
        self.role_box.setAlignment(Qt.AlignCenter)
        self.role_box.setWordWrap(True)
        
        self.role_desc = QLabel("")
        self.role_desc.setWordWrap(True)
        self.role_desc.setAlignment(Qt.AlignCenter)
        
        next_btn = QPushButton("VERSTANDEN & WEITER")
        next_btn.clicked.connect(self.next_player_role)
        add_glow(next_btn, "#00F2FE", 25)
        
        card_layout.addWidget(self.reveal_player_title)
        card_layout.addStretch()
        card_layout.addWidget(self.role_box)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.role_desc)
        card_layout.addStretch()
        card_layout.addWidget(next_btn)
        
        layout.addWidget(card)
        return widget

    def show_reveal_screen(self):
        player_name = self.players[self.current_player_idx]
        self.reveal_player_title.setText(f"Hallo {player_name}!")
        
        if player_name == self.imposter:
            self.role_box.setObjectName("ImposterLabel")
            self.role_box.setText("🤫 DU BIST DER\nIMPOSTER!")
            add_glow(self.role_box, "#FF416C", 30)
            
            if self.imposter_gets_clue:
                self.role_desc.setText(
                    f"💡 Dein Hinweis: Die Kategorie ist '{self.current_category}'.\n\nHöre genau zu und tarn dich!"
                )
            else:
                self.role_desc.setText("Du kennst das Geheimwort nicht.\nHöre den anderen gut zu und tarn dich!")
        else:
            self.role_box.setObjectName("SecretWordLabel")
            self.role_box.setText(f"Geheimwort:\n{self.secret_word}")
            add_glow(self.role_box, "#00F2FE", 30)
            self.role_desc.setText("Gib später einen Hinweis, der nicht zu offensichtlich ist!")
            
        self.role_box.setStyleSheet("")
        self.stacked_widget.setCurrentWidget(self.reveal_screen)

    def next_player_role(self):
        self.current_player_idx += 1
        if self.current_player_idx < len(self.players):
            self.show_pass_screen()
        else:
            self.start_clue_round()

    # --- 4. CLUE ROUND SCREEN ---
    def create_clue_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        title = QLabel("HINWEISRUNDE")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        sub = QLabel("Jeder Spieler nennt reihum genau EINEN Begriff als Hinweis!")
        sub.setWordWrap(True)
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #B0BEC5;")
        
        self.clue_player_label = QLabel("")
        self.clue_player_label.setObjectName("SecretWordLabel")
        self.clue_player_label.setAlignment(Qt.AlignCenter)
        add_glow(self.clue_player_label, "#00F2FE", 20)
        
        next_clue_btn = QPushButton("NÄCHSTER HINWEIS ➔")
        next_clue_btn.clicked.connect(self.next_clue_turn)
        add_glow(next_clue_btn, "#00F2FE", 25)
        
        card_layout.addWidget(title)
        card_layout.addWidget(sub)
        card_layout.addStretch()
        card_layout.addWidget(self.clue_player_label)
        card_layout.addStretch()
        card_layout.addWidget(next_clue_btn)
        
        layout.addWidget(card)
        return widget

    def start_clue_round(self):
        self.current_clue_idx = 0
        self.update_clue_screen()
        self.stacked_widget.setCurrentWidget(self.clue_screen)

    def update_clue_screen(self):
        player_name = self.players[self.current_clue_idx]
        self.clue_player_label.setText(f"👉 {player_name}")

    def next_clue_turn(self):
        self.current_clue_idx += 1
        if self.current_clue_idx < len(self.players):
            self.update_clue_screen()
        else:
            self.show_vote_screen()

    # --- 5. VOTING SCREEN ---
    def create_vote_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 25, 20, 25)
        
        title = QLabel("ABSTIMMUNG")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        sub = QLabel("Diskutiert & zeigt auf 3 gleichzeitig auf den Verdächtigen!\n\nWen habt ihr gewählt?")
        sub.setWordWrap(True)
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #B0BEC5;")
        
        self.vote_list = QListWidget()
        
        confirm_vote_btn = QPushButton("ABSTIMMUNG BESTÄTIGEN")
        confirm_vote_btn.clicked.connect(self.process_vote)
        add_glow(confirm_vote_btn, "#00F2FE", 25)
        
        card_layout.addWidget(title)
        card_layout.addWidget(sub)
        card_layout.addWidget(self.vote_list)
        card_layout.addSpacing(10)
        card_layout.addWidget(confirm_vote_btn)
        
        layout.addWidget(card)
        return widget

    def show_vote_screen(self):
        self.vote_list.clear()
        for p in self.players:
            self.vote_list.addItem(p)
        self.stacked_widget.setCurrentWidget(self.vote_screen)

    def process_vote(self):
        selected = self.vote_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Auswahl fehlt", "Bitte wählt den verdächtigten Spieler aus!")
            return
        
        voted_player = selected[0].text()
        
        if voted_player == self.imposter:
            self.show_guess_screen()
        else:
            self.show_result_screen(
                winner="IMPOSTER",
                message=f"Der Imposter wurde NICHT entdeckt!\n\nImposter war: {self.imposter}\nGewählt wurde: {voted_player}"
            )

    # --- 6. IMPOSTER GUESS SCREEN ---
    def create_guess_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        title = QLabel("ENTLARVT!")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        self.guess_subtitle = QLabel("")
        self.guess_subtitle.setWordWrap(True)
        self.guess_subtitle.setAlignment(Qt.AlignCenter)
        
        self.guess_input = QLineEdit()
        self.guess_input.setPlaceholderText("Geheimwort erraten...")
        
        submit_guess_btn = QPushButton("RATEN")
        submit_guess_btn.clicked.connect(self.check_guess)
        add_glow(submit_guess_btn, "#00F2FE", 25)
        
        card_layout.addWidget(title)
        card_layout.addWidget(self.guess_subtitle)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.guess_input)
        card_layout.addStretch()
        card_layout.addWidget(submit_guess_btn)
        
        layout.addWidget(card)
        return widget

    def show_guess_screen(self):
        self.guess_subtitle.setText(
            f"🚨 Der Imposter {self.imposter} wurde entdeckt!\n\n"
            f"{self.imposter}, du hast eine letzte Chance: Errätst du das Geheimwort?"
        )
        self.guess_input.clear()
        self.stacked_widget.setCurrentWidget(self.guess_screen)

    def check_guess(self):
        guess = self.guess_input.text().strip()
        if not guess:
            QMessageBox.warning(self, "Eingabe fehlt", "Bitte gib dein geratenes Wort ein!")
            return
            
        if guess.lower() == self.secret_word.lower():
            self.show_result_screen(
                winner="IMPOSTER",
                message=f"🎉 DER IMPOSTER GEWINNT TROTZDEM!\n\n{self.imposter} hat das Wort '{self.secret_word}' richtig erraten!"
            )
        else:
            self.show_result_screen(
                winner="CREW",
                message=f"🏆 DIE GRUPPE GEWINNT!\n\n{self.imposter} hat falsch geraten ('{guess}').\n\nDas Geheimwort war: {self.secret_word}"
            )

    # --- 7. RESULT SCREEN ---
    def create_result_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 30, 25, 30)
        
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        self.result_title = QLabel("SIEG!")
        self.result_title.setObjectName("TitleLabel")
        self.result_title.setAlignment(Qt.AlignCenter)
        
        self.result_text = QLabel("")
        self.result_text.setWordWrap(True)
        self.result_text.setAlignment(Qt.AlignCenter)
        
        play_again_btn = QPushButton("NOCH EINE RUNDE 🔄")
        play_again_btn.clicked.connect(self.reset_to_setup)
        add_glow(play_again_btn, "#00F2FE", 25)
        
        card_layout.addWidget(self.result_title)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.result_text)
        card_layout.addStretch()
        card_layout.addWidget(play_again_btn)
        
        layout.addWidget(card)
        return widget

    def show_result_screen(self, winner, message):
        if winner == "IMPOSTER":
            self.result_title.setText("😈 IMPOSTER SIEG!")
        else:
            self.result_title.setText("🎉 DIE GRUPPE GEWINNT!")
            
        self.result_text.setText(message)
        self.stacked_widget.setCurrentWidget(self.result_screen)

    def reset_to_setup(self):
        self.stacked_widget.setCurrentWidget(self.setup_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImposterApp()
    window.show()
    sys.exit(app.exec_())