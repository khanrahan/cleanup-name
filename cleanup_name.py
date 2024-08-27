"""
Script Name: Cleanup Name
Written By: Kieran Hanrahan

Script Version: 1.0.0
Flame Version: 2021.1

URL: http://github.com/khanrahan/cleanup-name

Creation Date: 06.23.23
Update Date: 10.04.23

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

from PySide2 import QtCore, QtWidgets

TITLE = 'Cleanup Name'
VERSION_INFO = (1, 0, 0, 'dev')
VERSION = '.'.join([str(num) for num in VERSION_INFO])
VERSION_TITLE = '{} v{}'.format(TITLE, VERSION)

MESSAGE_PREFIX = "[PYTHON HOOK]"


class FlameButton(QtWidgets.QPushButton):
    """
    Custom Qt Flame Button Widget
    To use:
    button = FlameButton('Button Name', do_when_pressed, window)
    """

    def __init__(self, button_name, do_when_pressed, parent_window, *args, **kwargs):
        super(FlameButton, self).__init__(*args, **kwargs)

        self.setText(button_name)
        self.setParent(parent_window)
        self.setMinimumSize(QtCore.QSize(110, 28))
        self.setMaximumSize(QtCore.QSize(110, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(do_when_pressed)
        self.setStyleSheet("""
            QPushButton {color: #9a9a9a;
                         background-color: #424142;
                         border-top: 1px inset #555555;
                         border-bottom: 1px inset black;
                         font: 14px 'Discreet'}
            QPushButton:pressed {color: #d9d9d9;
                                 background-color: #4f4f4f;
                                 border-top: 1px inset #666666;
                                 font: italic}
            QPushButton:disabled {color: #747474;
                                  background-color: #353535;
                                  border-top: 1px solid #444444;
                                  border-bottom: 1px solid #242424}
            QToolTip {color: black;
                      background-color: #ffffde;
                      border: black solid 1px}""")


class FlameLabel(QtWidgets.QLabel):
    """
    Custom Qt Flame Label Widget
    For different label looks set label_type as: 'normal', 'background', or 'outline'
    To use:
    label = FlameLabel('Label Name', 'normal', window)
    """

    def __init__(self, label_name, label_type, parent_window, *args, **kwargs):
        super(FlameLabel, self).__init__(*args, **kwargs)

        self.setText(label_name)
        self.setParent(parent_window)
        self.setMinimumSize(110, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        border-bottom: 1px inset #282828;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")
        elif label_type == 'background':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        background-color: #393939;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")
        elif label_type == 'outline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        background-color: #212121;
                        border: 1px solid #404040;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")


class FlameListWidget(QtWidgets.QListWidget):
    """
    Custom Qt Flame List Widget
    To use:
    list_widget = FlameListWidget(window)
    """

    def __init__(self, parent_window, *args, **kwargs):
        super(FlameListWidget, self).__init__(*args, **kwargs)

        self.setMinimumSize(500, 250)
        self.setParent(parent_window)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # only want 1 selection possible.  no multi selection.
        #self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setSpacing(3)
        self.setAlternatingRowColors(True)
        self.setUniformItemSizes(True)
        self.setStyleSheet("""
            QListWidget {color: #9a9a9a;
                         background-color: #2a2a2a;
                         alternate-background-color: #2d2d2d;
                         outline: none;
                         font: 14px 'Discreet'}
            QListWidget::item:selected {color: #d9d9d9;
                                        background-color: #474747}""")


class FlamePushButtonMenu(QtWidgets.QPushButton):
    """
    Custom Qt Flame Menu Push Button Widget v2.0

    button_name: text displayed on button [str]
    menu_options: list of options show when button is pressed [list]
    menu_width: (optional) width of widget. default is 150. [int]
    max_menu_width: (optional) set maximum width of widget. default is 2000. [int]
    menu_action: (optional) execute when button is changed. [function]

    Usage:

        push_button_menu_options = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        menu_push_button = FlamePushButtonMenu('push_button_name', push_button_menu_options)

        or

        push_button_menu_options = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        menu_push_button = FlamePushButtonMenu(push_button_menu_options[0], push_button_menu_options)
    """

    def __init__(self, button_name, menu_options, menu_width=150, max_menu_width=2000, menu_action=None):
        super(FlamePushButtonMenu, self).__init__()
        from functools import partial

        self.setText(button_name)
        self.setMinimumHeight(28)
        self.setMinimumWidth(menu_width)
        self.setMaximumWidth(max_menu_width)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""
            QPushButton {color: rgb(154, 154, 154);
                         background-color: rgb(45, 55, 68);
                         border: none;
                         font: 14px 'Discreet';
                         padding-left: 6px;
                         text-align: left}
            QPushButton:disabled {color: rgb(116, 116, 116);
                                  background-color: rgb(45, 55, 68);
                                  border: none}
            QPushButton:hover {border: 1px solid rgb(90, 90, 90)}
            QPushButton::menu-indicator {image: none}
            QToolTip {color: rgb(170, 170, 170);
                      background-color: rgb(71, 71, 71);
                      border: 10px solid rgb(71, 71, 71)}""")

        def create_menu(option, menu_action):
            self.setText(option)
            if menu_action:
                menu_action()

        pushbutton_menu = QtWidgets.QMenu(self)
        pushbutton_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        pushbutton_menu.setStyleSheet("""
            QMenu {color: rgb(154, 154, 154);
                   background-color: rgb(45, 55, 68);
                   border: none;
                   font: 14px 'Discreet'}
            QMenu::item:selected {color: rgb(217, 217, 217);
                   background-color: rgb(58, 69, 81)}""")

        for option in menu_options:
            pushbutton_menu.addAction(option, partial(create_menu, option, menu_action))

        self.setMenu(pushbutton_menu)


class FlameTextEdit(QtWidgets.QTextEdit):
    """
    Custom Qt Flame Text Edit Widget v2.1

    text: text to be displayed [str]
    read_only: (optional) make text in window read only [bool] - default is False

    To use:

        text_edit = FlameTextEdit('some_text_here', True_or_False)
    """

    def __init__(self, text, read_only=False):
        super(FlameTextEdit, self).__init__()

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
    """Takes PyClips and sanitizes the name to remove all symbols and change whitespace
    to underscores."""

    def __init__(self, selection):
        self.selection = selection
        self.names = [clip.name.get_value() for clip in self.selection]
        self.names_clean = [self.cleanup_text(name) for name in self.names]

        self.description = ('Clean up clip names by removing all symbols and replacing '
                            'whitespace with underscores.')
        self.views = ['Clean Name', 'Original Name']
        self.view_selection = self.views[0]

        self.message(VERSION_TITLE)
        self.message('Script called from {}'.format(__file__))

        self.main_window()


    @staticmethod
    def message(string):
        """Print message to shell window and append global MESSAGE_PREFIX."""

        print(' '.join([MESSAGE_PREFIX, string]))


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

    @staticmethod
    def refresh():
        """Necessary after changing attributes to have the changes show up on the
        Desktop.  Otherwise, the script runs, but the change will not be shown on the
        thumbnail until you tap on the UI."""

        import flame
        flame.execute_shortcut("Refresh Thumbnails")

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
                self.message('Skipping {}. No changes necessary.'.format(self.names[num]))
                continue

            clip.name.set_value(self.names_clean[num])
            self.message('Renamed {} to {}'.format(self.names[num],
                                                   self.names_clean[num]))


    def main_window(self):

        def okay_button():

            self.window.close()
            self.update_names()
            self.refresh()
            self.message("Done!")

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
        resolution = QtWidgets.QDesktopWidget().screenGeometry()

        self.window.move((resolution.width() / 2) - (self.window.frameSize().width() / 2),
                         (resolution.height() / 2) - (self.window.frameSize().height() / 2))

        # Labels
        self.description_label = FlameLabel('Description', 'normal', self.window)
        self.view_label = FlameLabel('View', 'normal', self.window)

        # List Widget
        self.list_scroll = FlameListWidget(self.window)
        self.list_scroll.addItems(self.names_clean)

        # Buttons
        self.view_btn = FlamePushButtonMenu(self.view_selection, self.views,
                menu_action=self.update_view)
        self.view_btn.setMaximumWidth(100)
        #the below should work, but doesnt
        #self.view_btn.released.connect(self.update_view)

        self.ok_btn = FlameButton('Ok', okay_button, self.window)
        self.ok_btn.setStyleSheet('background: #732020')
        self.ok_btn.setShortcut('Return')

        self.cancel_btn = FlameButton('Cancel', cancel_button, self.window)

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
        self.vbox.setMargin(20)
        self.vbox.addLayout(self.grid)
        self.vbox.insertSpacing(1, 20)
        self.vbox.addLayout(self.hbox)
        self.vbox.insertSpacing(3, 20)
        self.vbox.addLayout(self.hbox2)

        self.window.setLayout(self.vbox)

        self.window.show()
        return self.window


def scope_clip(selection):

    import flame
    return any(isinstance(item, flame.PyClip) for item in selection)


def get_media_panel_custom_ui_actions():

    return [{'name': 'Edit...',
             'actions': [{'name': 'Cleanup Name',
                          'isVisible': scope_clip,
                          'execute': CleanupName,
                          'minimumVersion': '2022'}]
            }]
