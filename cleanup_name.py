"""
Script Name: Cleanup Name
Written By: Kieran Hanrahan

Script Version: 1.0.0
Flame Version: 2025

URL: http://github.com/khanrahan/cleanup-name

Creation Date: 06.23.23
Update Date: 08.27.24

Description:

    Cleanup selected clip names.  Remove all symbols and convert all spaces to
    underscores.

Menus:

    Right-click selected clips on the Desktop -> Edit... -> Cleanup Name
    Right-click selected clips in the Media Panel -> Edit... -> Cleanup Name

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

from functools import partial

import flame
from PySide6 import QtCore, QtGui, QtWidgets

TITLE = 'Cleanup Name'
VERSION_INFO = (1, 0, 0)
VERSION = '.'.join([str(num) for num in VERSION_INFO])
VERSION_TITLE = f'{TITLE} v{VERSION}'

MESSAGE_PREFIX = '[PYTHON]'


class FlameButton(QtWidgets.QPushButton):
    """Custom Qt Flame Button Widget v2.1

    button_name: button text [str]
    connect: execute when clicked [function]
    button_color: (optional) normal, blue [str]
    button_width: (optional) default is 150 [int]
    button_max_width: (optional) default is 150 [int]

    Usage:

        button = FlameButton(
            'Button Name', do_something__when_pressed, button_color='blue')
    """

    def __init__(self, button_name, connect, button_color='normal', button_width=150,
                 button_max_width=150):
        super().__init__()

        self.setText(button_name)
        self.setMinimumSize(QtCore.QSize(button_width, 28))
        self.setMaximumSize(QtCore.QSize(button_max_width, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(connect)
        if button_color == 'normal':
            self.setStyleSheet("""
                QPushButton {
                    color: rgb(154, 154, 154);
                    background-color: rgb(58, 58, 58);
                    border: none;
                    font: 14px 'Discreet'}
                QPushButton:hover {
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:pressed {
                    color: rgb(159, 159, 159);
                    background-color: rgb(66, 66, 66);
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:disabled {
                    color: rgb(116, 116, 116);
                    background-color: rgb(58, 58, 58);
                    border: none}
                QToolTip {
                    color: rgb(170, 170, 170);
                    background-color: rgb(71, 71, 71);
                    border: 10px solid rgb(71, 71, 71)}""")
        elif button_color == 'blue':
            self.setStyleSheet("""
                QPushButton {
                    color: rgb(190, 190, 190);
                    background-color: rgb(0, 110, 175);
                    border: none;
                    font: 12px 'Discreet'}
                QPushButton:hover {
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:pressed {
                    color: rgb(159, 159, 159);
                    border: 1px solid rgb(90, 90, 90)
                QPushButton:disabled {
                    color: rgb(116, 116, 116);
                    background-color: rgb(58, 58, 58);
                    border: none}
                QToolTip {
                    color: rgb(170, 170, 170);
                    background-color: rgb(71, 71, 71);
                    border: 10px solid rgb(71, 71, 71)}""")


class FlameLabel(QtWidgets.QLabel):
    """Custom Qt Flame Label Widget v2.1

    label_name:  text displayed [str]
    label_type:  (optional) select from different styles:
                 normal, underline, background. default is normal [str]
    label_width: (optional) default is 150 [int]

    Usage:

        label = FlameLabel('Label Name', 'normal', 300)
    """

    def __init__(self, label_name, label_type='normal', label_width=150):
        super().__init__()

        self.setText(label_name)
        self.setMinimumSize(label_width, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet("""
                QLabel {
                    color: rgb(154, 154, 154);
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}""")
        elif label_type == 'underline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {
                    color: rgb(154, 154, 154);
                    border-bottom: 1px inset rgb(40, 40, 40);
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}""")
        elif label_type == 'background':
            self.setStyleSheet("""
                QLabel {
                    color: rgb(154, 154, 154);
                    background-color: rgb(30, 30, 30);
                    padding-left: 5px;
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}""")


class FlameListWidget(QtWidgets.QListWidget):
    """Custom Qt Flame List Widget

    Usage:
        list_widget = FlameListWidget(window)
    """

    def __init__(self, parent_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(500, 250)
        self.setParent(parent_window)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSpacing(3)
        self.setAlternatingRowColors(True)
        self.setUniformItemSizes(True)
        self.setStyleSheet("""
            QListWidget {
                color: #9a9a9a;
                background-color: #2a2a2a;
                alternate-background-color: #2d2d2d;
                outline: none;
                font: 14px 'Discreet'}
            QListWidget::item:selected {
                color: #d9d9d9;
                background-color: #474747}""")


class FlamePushButtonMenu(QtWidgets.QPushButton):
    """Custom Qt Flame Menu Push Button Widget v3.1

    button_name: text displayed on button [str]
    menu_options: list of options show when button is pressed [list]
    menu_width: (optional) width of widget. default is 150. [int]
    max_menu_width: (optional) set maximum width of widget. default is 2000. [int]
    menu_action: (optional) execute when button is changed. [function]

    Usage:

        push_button_menu_options = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        menu_push_button = FlamePushButtonMenu(
            'push_button_name', push_button_menu_options)

        or

        push_button_menu_options = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        menu_push_button = FlamePushButtonMenu(
            push_button_menu_options[0], push_button_menu_options)

    Notes:
        Started as v2.1
        v3.1 adds a functionionality to set the width of the menu to be the same as the
        button.
    """

    def __init__(self, button_name, menu_options, menu_width=240, max_menu_width=2000,
                 menu_action=None):
        super().__init__()

        self.button_name = button_name
        self.menu_options = menu_options
        self.menu_action = menu_action

        self.setText(button_name)
        self.setMinimumHeight(28)
        self.setMinimumWidth(menu_width)
        self.setMaximumWidth(max_menu_width)  # is max necessary?
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""
            QPushButton {
                color: rgb(154, 154, 154);
                background-color: rgb(45, 55, 68);
                border: none;
                font: 14px 'Discreet';
                padding-left: 9px;
                text-align: left}
            QPushButton:disabled {
                color: rgb(116, 116, 116);
                background-color: rgb(45, 55, 68);
                border: none}
            QPushButton:hover {
                border: 1px solid rgb(90, 90, 90)}
            QPushButton::menu-indicator {image: none}
            QToolTip {
                color: rgb(170, 170, 170);
                background-color: rgb(71, 71, 71);
                border: 10px solid rgb(71, 71, 71)}""")

        # Menu
        def match_width():
            """Match menu width to the parent push button width."""
            self.pushbutton_menu.setMinimumWidth(self.size().width())

        self.pushbutton_menu = QtWidgets.QMenu(self)
        self.pushbutton_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushbutton_menu.aboutToShow.connect(match_width)
        self.pushbutton_menu.setStyleSheet("""
            QMenu {
                color: rgb(154, 154, 154);
                background-color: rgb(45, 55, 68);
                border: none; font: 14px 'Discreet'}
            QMenu::item:selected {
                color: rgb(217, 217, 217);
                background-color: rgb(58, 69, 81)}""")

        self.populate_menu(menu_options)
        self.setMenu(self.pushbutton_menu)

    def create_menu(self, option, menu_action):
        """Create menu."""
        self.setText(option)

        if menu_action:
            menu_action()

    def populate_menu(self, options):
        """Empty the menu then reassemble the options."""
        self.pushbutton_menu.clear()

        for option in options:
            self.pushbutton_menu.addAction(
                option, partial(self.create_menu, option, self.menu_action))


class FlameTextEdit(QtWidgets.QTextEdit):
    """Custom Qt Flame Text Edit Widget v2.1

    text: text to be displayed [str]
    read_only: (optional) make text in window read only [bool] - default is False

    Usage:
        text_edit = FlameTextEdit('some_text_here', True_or_False)
    """

    def __init__(self, text, read_only=False):
        super().__init__()

        self.setMinimumHeight(20)
        self.setMinimumWidth(150)
        self.setMaximumHeight(60)
        self.setText(text)
        self.setReadOnly(read_only)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        if read_only:
            self.setStyleSheet("""
                QTextEdit {color: rgb(154, 154, 154);
                           background-color:
                           rgb(28, 28, 28);
                           selection-color: #262626;
                           selection-background-color: #b8b1a7;
                           border: 1px solid rgb(55, 55, 55);
                           padding-left: 5px;
                           font: 14px 'Discreet'}
                ScrollBar {color: #111111;
                           background: rgb(49, 49, 49)}
                ScrollBar::handle {color: #111111;
                                   background : 111111}
                ScrollBar::add-line:vertical {border: none;
                                              background: none;
                                              width: 0px;
                                              height: 0px}
                ScrollBar::sub-line:vertical {border: none;
                                              background: none;
                                              width: 0px;
                                              height: 0px}
                ScrollBar {color: #111111;
                           background: rgb(49, 49, 49)}
                ScrollBar::handle {color: #111111;
                                   background : 111111}
                ScrollBar::add-line:horizontal {border: none;
                                                background: none;
                                                width: 0px;
                                                height: 0px}
                ScrollBar::sub-line:horizontal {border: none;
                                                background: none;
                                                width: 0px;
                                                height: 0px}""")
        else:
            self.setStyleSheet("""
                QTextEdit {color: rgb(154, 154, 154);
                                  background-color: #37414b;
                                  selection-color: #262626;
                                  selection-background-color: #b8b1a7;
                                  border: none;
                                  padding-left: 5px;
                                  font: 14px 'Discreet'}
                QTextEdit:focus {background-color: #495663}'
                QScrollBar {color: #111111;
                            background: rgb(49, 49, 49)}
                QScrollBar::handle {color: #111111;
                                    background : 111111;}
                QScrollBar::add-line:vertical {border: none;
                                               background: none;
                                               width: 0px;
                                               height: 0px}
                QScrollBar::sub-line:vertical {border: none;
                                               background: none;
                                               width: 0px;
                                               height: 0px}
                QScrollBar {color: #111111;
                            background: rgb(49, 49, 49)}
                QScrollBar::handle {color: #111111;
                                    background : 111111;}
                QScrollBar::add-line:horizontal {border: none;
                                                 background: none;
                                                 width: 0px;
                                                 height: 0px}'
                QScrollBar::sub-line:horizontal {border: none;
                                                 background: none;
                                                 width: 0px;
                                                 height: 0px}""")


class CleanupName:
    """Takes PyClips and sanitizes the name.

    Will remove all symbols and change whitespace to underscores.
    """

    def __init__(self, selection):
        """Initialize object."""
        self.selection = selection
        self.names = [clip.name.get_value() for clip in self.selection]
        self.names_clean = [self.cleanup_text(name) for name in self.names]

        self.description = ('Clean up clip names by removing all symbols and replacing '
                            'whitespace with underscores.')
        self.views = ['Clean Name', 'Original Name']
        self.view_selection = self.views[0]

        self.message(VERSION_TITLE)
        self.message(f'Script called from {__file__}')

        self.main_window()

    @staticmethod
    def message(string):
        """Print message to shell window and append global MESSAGE_PREFIX."""
        print(' '.join([MESSAGE_PREFIX, string]))

    @staticmethod
    def refresh():
        """Refresh the flame UI.

        Necessary after changing attributes to have the changes show up on the
        Desktop.  Otherwise, the script runs, but the change will not be shown on the
        thumbnail until you tap on the UI.
        """
        flame.execute_shortcut('Refresh Thumbnails')

    @staticmethod
    def cleanup_text(text):
        """Returns string that is appropriate for filename usage."""
        import re

        # Delete first and last character if a symbol or space.
        chopped = re.sub(r'^[\W_]+|[\W_]+$', '', text)
        # Convert symbols & whitespace to underscores.
        sanitized = re.sub(r'\W+', '_', chopped)
        # Remove duplicate underscores.
        tidy = re.sub(r'(_)\1+', '_', sanitized)

        return tidy

    def update_view(self):
        """Clear the list view and replace with the appropriate list."""
        self.list_scroll.clear()

        if self.view_btn.text() == 'Clean Name':
            self.list_scroll.addItems(self.names_clean)
        if self.view_btn.text() == 'Original Name':
            self.list_scroll.addItems(self.names)

    def update_names(self):
        """Change names of the PyClips to the clean names, skip if unnecesary.

        Relies on 3 lists:
            self.selection = PyClip objects
            self.names = name of the PyClip objects
            self.names_clean = cleaned up names of the above
        """
        for num, clip in enumerate(self.selection):
            if self.names[num] == self.names_clean[num]:
                self.message(f'Skipping {self.names[num]}. No changes necessary.')
                continue

            clip.name.set_value(self.names_clean[num])
            self.message(f'Renamed {self.names[num]} to {self.names_clean[num]}.')

    def main_window(self):
        """The main GUI window."""

        def okay_button():

            self.window.close()
            self.update_names()
            self.refresh()
            self.message('Done!')

        def cancel_button():

            self.window.close()
            self.message('Cancelled!')

        self.window = QtWidgets.QWidget()

        self.window.setMinimumSize(600, 600)
        self.window.setStyleSheet('background-color: #272727')
        self.window.setWindowTitle(VERSION_TITLE)

        # FlameLineEdit class needs this
        self.window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Center Window
        resolution = QtGui.QGuiApplication.primaryScreen().availableGeometry()

        self.window.move(
                (resolution.width() / 2) - (self.window.frameSize().width() / 2),
                (resolution.height() / 2) - (self.window.frameSize().height() / 2)
        )

        # Labels
        self.description_label = FlameLabel('Description', 'normal')
        self.view_label = FlameLabel('View', 'normal')

        # List Widget
        self.list_scroll = FlameListWidget(self.window)
        self.list_scroll.addItems(self.names_clean)

        # Buttons
        self.view_btn = FlamePushButtonMenu(self.view_selection, self.views,
                menu_action=self.update_view)
        self.view_btn.setMaximumWidth(100)

        self.ok_btn = FlameButton('Ok', okay_button, button_color='blue')
        self.ok_btn.setShortcut('Return')

        self.cancel_btn = FlameButton('Cancel', cancel_button)

        # Text
        self.description_text = FlameTextEdit(self.description, True)

        # Layout
        self.grid = QtWidgets.QGridLayout()
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)

        self.grid.addWidget(self.description_label, 0, 0, alignment=QtCore.Qt.AlignTop)
        self.grid.addWidget(self.description_text, 0, 1)
        self.grid.addWidget(self.view_label, 1, 0)
        self.grid.addWidget(self.view_btn, 1, 1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addSpacing(50)
        self.hbox.addWidget(self.list_scroll)
        self.hbox.addSpacing(50)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.cancel_btn)
        self.hbox2.addWidget(self.ok_btn)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(20, 20, 20, 20)
        self.vbox.addLayout(self.grid)
        self.vbox.addSpacing(20)
        self.vbox.addLayout(self.hbox)
        self.vbox.addSpacing(20)
        self.vbox.addLayout(self.hbox2)

        self.window.setLayout(self.vbox)

        self.window.show()
        return self.window


def scope_clip(selection):
    """Test selection."""
    valid_objects = (
            flame.PyClip,
            flame.PySegment,
    )

    return all(isinstance(item, valid_objects) for item in selection)


def get_media_panel_custom_ui_actions():
    """Add right click menu item."""
    return [{'name': 'Edit...',
             'actions': [{'name': 'Cleanup Name',
                          'isVisible': scope_clip,
                          'execute': CleanupName,
                          'minimumVersion': '2025'}]
            }]
