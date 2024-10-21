from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel
import sys


combo_box_style = """
    QComboBox {
        background-color: #1E1E1E; /* Dark background */
        color: #FFFFFF; /* White text */
        border: 1px solid #555555; /* Subtle border */
        border-radius: 4px; /* Rounded corners */
        padding: 5px; /* Padding for better aesthetics */
        font-size: 14px; /* Font size */
        min-width: 150px; /* Minimum width */
    }

    QComboBox::drop-down {
        border: none; /* Remove dropdown border */
        background: transparent; /* Keep dropdown transparent */
    }

    QComboBox::indicator {
        width: 20px; /* Width for dropdown arrow */
        height: 20px; /* Height for dropdown arrow */
    }

    QComboBox::item {
        background-color: #1E1E1E; /* Dark background for items */
        color: #FFFFFF; /* White text for items */
        padding: 5px 10px; /* Padding for items */
    }

    QComboBox::item:selected {
        background-color: #007ACC; /* Selected item background color */
        color: #FFFFFF; /* Selected item text color */
    }

    QComboBox::item:hover {
        background-color: #007ACC; /* Hover color for items */
        color: #FFFFFF; /* Text color on hover */
    }

    QComboBox::focus {
        border: 1px solid #007ACC; /* Focus border color */
    }

    /* Disable animation when opening the dropdown */
    QComboBox QAbstractItemView {
        background: #1E1E1E; /* Dark background for the dropdown */
        color: #FFFFFF; /* White text for dropdown items */
        selection-background-color: #007ACC; /* Selected item background */
        selection-color: #FFFFFF; /* Selected item text color */
        border: 1px solid #555555; /* Border for the dropdown */
    }
"""


class ComboBoxDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Dark Themed QComboBox Demo")
        self.setGeometry(100, 100, 300, 150)

        # Set up layout
        layout = QVBoxLayout()

        # Create a combobox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])



        # Apply the custom stylesheet
        self.combo_box.setStyleSheet(combo_box_style)

        # Connect the combobox signal to a slot
        self.combo_box.currentTextChanged.connect(self.update_label)

        # Add label to show the selected option
        self.label = QLabel("Selected: Option 1")
        
        # Add widgets to layout
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label)

        # Set the main layout
        self.setLayout(layout)

    def update_label(self, text):
        self.label.setText(f"Selected: {text}")

if __name__ == "__main__":
    from PySide6.QtCore import Qt
    app = QApplication(sys.argv)

    QApplication.setEffectEnabled(Qt.UI_AnimateCombo, False)

    demo = ComboBoxDemo()
    demo.show()
    sys.exit(app.exec())
