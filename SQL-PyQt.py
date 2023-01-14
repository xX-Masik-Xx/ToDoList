import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QApplication, QPushButton, QListWidget, QVBoxLayout, QLineEdit, QMenu, QMainWindow, QAction, QComboBox, QTextEdit, QHBoxLayout, QLabel, QLayout, QCheckBox, QSpacerItem, QListView
from PyQt5.QtCore import Qt, QPoint
import math

class ApplicationMainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.categories_combo_box = QComboBox()
        self.categories_list = QListWidget()
        self.tasks_list = QListWidget()
        self.chechboxes_list = []
        self.categories_colours = ["429a8e", "4d99d3", "d95676", "6789e0", "dabd5f"]
        self.categories_colours_id = []
        self.create_db()
        self.load_categories()
        self.load_tasks()
        self.initUI()
        self.add_task_window = None
        self.task_name = None
        self.task_description = None
        self.add_task_window = None
        self.categories_window = None

    def initUI(self):
        #Начало
        self.main_widget = QWidget(self)
        self.main_widget.setFocus()
        self.main_widget.setStyleSheet(
            """
            background-color : #2d2e32;
            """
        )
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout(self.main_widget)

        #Действия
        self.addTaskAction = QAction("Добавить", self)
        self.addTaskAction.triggered.connect(self.show_add_task_window)
        self.editTaskAction = QAction("Редактировать", self)
        self.deleteTaskAction = QAction("Удалить", self)
        self.deleteTaskAction.triggered.connect(self.remove_task)

        #Список задач
        layout.setContentsMargins(0, 0, 0, 52)
        layout.addWidget(self.tasks_list)
        

        #Кнопка "Добавить задачу"
        button = QPushButton("+", self.main_widget)
        button.setFixedSize(100, 100)
        button.setFont(QFont('Rubik Mono One', 45, 57, False))
        button.setStyleSheet("""
        QPushButton{
            color: #32bc81;
            background-color : #2d2e32;
            border-radius : 50; 
            border : 7.5px solid #1f1f1f;
            } 
                              """)
        button.clicked.connect(self.show_add_task_window)
        p = self.tasks_list.geometry().bottomRight() - button.geometry().bottomRight() - QPoint(math.floor(self.tasks_list.geometry().width() / 2) - 50, 45)
        button.move(p)

        categoriesButton = QPushButton("🔠", self.main_widget)
        categoriesButton.resize(50, 50)
        categoriesButton.setFont(QFont('Segoe UI Emoji', 20, 57, False))
        categoriesButton.move(10, 397)
        categoriesButton.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        categoriesButton.clicked.connect(self.show_categories_window)
        
        #Конец
        self.setGeometry(700, 400, 675, 450)
        self.setWindowTitle('ToDoList')
        self.show()

    def contextMenuEvent(self, event):
        #Создание
        self.context_menu = QMenu(self)
        self.context_menu.addAction(self.addTaskAction)
        self.context_menu.addAction(self.editTaskAction)
        self.context_menu.addAction(self.deleteTaskAction)
        
        #Стиль
        self.context_menu.setStyleSheet(
            """
            QMenu{
                background-color: #595b60;
                border: 1px solid black;
            }
            """
        )
        action = self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def show_add_task_window(self):
        if self.add_task_window is None:
            self.add_task_window = AddTaskWindow(self)

        else:
            self.add_task_window.close()  # Close window.
            self.add_task_window = None # Discard reference.
            self.add_task_window = AddTaskWindow(self)

    def show_categories_window(self):
        if self.categories_window is None:
            self.categories_window = CategoriesWindow(self)

        else:
            self.categories_window.close()  # Close window.
            self.categories_window = None # Discard reference.
            self.categories_window = CategoriesWindow(self)

    def create_db(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("contacts.sqlite")

        con.open()
        
        create_table_query = QSqlQuery()
        create_table_query.exec(
            """
            CREATE table if not Exists categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
            );
            """
        )

        # insert_categories_query = QSqlQuery()
        # insert_categories_query.prepare(
        #     """
        #     INSERT INTO categories 
        #     (
        #         name
        #     ) 
        #     VALUES (?)
        #     """
        # )
        # inserted_categories_data_query = ['AAA', 'BBB', 'CCC']
        # for inserted_categories_data_query in inserted_categories_data_query:
        #     insert_categories_query.addBindValue(inserted_categories_data_query)
        #     insert_categories_query.exec()
        
        create_table_query.exec(
            """
            CREATE TABLE IF NOT Exists tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT null,
            description VARCHAR(255) NOT null,
            active BOOL NOT NULL DEFAULT true,
            category_id int,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );
            """
        )

        # insert_tasks_query = QSqlQuery()
        # insert_tasks_query.prepare(
        #     """
        #     INSERT INTO tasks (name, description, active, category_id) 
        #     VALUES (?, ?, ?, ?)
        #     """
        # )
        # inserted_tasks_data_query = [('ToDo1', 'You must do this!', True, 1), ('ToDo2', 'You definetely must do this!', True, 3), ('ToDo3', 'I\'m sure you will definetely must do this!', True, 1), ('ToDo4', 'I beg you to do this!!!', True, 2)]
        # for inserted_task_data_query in inserted_tasks_data_query:
        #     for i in range(4):
        #         insert_tasks_query.addBindValue(inserted_task_data_query[i])
        #     insert_tasks_query.exec()

        create_table_query.finish()

    def load_categories(self):
        self.categories_combo_box = QComboBox()
        self.categories_list = QListWidget()
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM categories;
            """
        )
        self.categories = []
        self.categories_colours_id = []
        count = query.record().count()
        while query.next():
            self.categories.append([query.value(i) for i in range(count)])
            self.categories_colours_id.append(query.value(0))
        self.categories_combo_box.clear()
        self.categories_list.clear()
        for category in self.categories:
            self.categories_combo_box.addItem(category[1])
            self.categories_list.addItem(QListWidgetItem(category[1]))
        query.finish()

    def load_tasks(self):
        self.tasks_list.clear()
        self.tasks_list.setWrapping(True)
        self.tasks_list.setSpacing(5)
        self.tasks_list.setItemAlignment(Qt.AlignCenter)
        self.tasks_list.setStyleSheet(
            """
            background-color: #1f1f1f;
            border: none;
            """
        )
        self.chechboxes_list.clear()

        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM tasks LEFT JOIN categories ON category_id=categories.id;
            """
        )
        self.tasks = []
        while query.next():
            self.tasks.append([query.value(i) for i in range(5)])
        for tasks in self.tasks:
            itemN = QListWidgetItem()
            widget = QWidget()
            widget.setStyleSheet(
                f"""
                background-color: #{self.categories_colours[self.categories_colours_id.index(tasks[4])]};;
                border-radius: 5;
                """
            )
            taskName = QLabel(tasks[1])
            taskName.setFont(QFont('Graphik LCG', 20, 57, False))
            taskName.setStyleSheet("color: #1f1f1f" if not tasks[3] else """
                color: #1f1f1f;
                text-decoration: line-through;
            """)
            taskDescription = QLabel(tasks[2])
            taskDescription.setFont(QFont('Graphik LCG', 15, 57, True))
            taskDescription.font().setItalic(True)
            if taskDescription.fontMetrics().boundingRect(taskDescription.text()).width() > 305:
                for i in range(len(taskDescription.text())):
                    if taskDescription.fontMetrics().boundingRect(taskDescription.text()[:-(i+ 1)]).width() <= 289:
                        taskDescription.setText(taskDescription.text()[:-(i+ 1)] + "...")
                        break
            taskDescription.setStyleSheet("color: #9ba0a6")
            self.chechboxes_list.append(QCheckBox())
            self.chechboxes_list[-1].setChecked(tasks[3])
            self.chechboxes_list[-1].toggled.connect(self.swich_active)
            widgetLayout = QHBoxLayout()
            widgetLayout.addWidget(self.chechboxes_list[-1])
            
            widgetLayout.addWidget(taskName)
            space_width = 316 - taskDescription.fontMetrics().boundingRect(taskName.text()).width()
            widgetLayout.addSpacerItem(QSpacerItem(space_width, 0))
            widgetLayout.addWidget(taskDescription)
            widgetLayout.addStretch()

            widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
            widget.setLayout(widgetLayout)
            itemN.setSizeHint(widget.sizeHint())

            # Add widget to QListWidget funList
            self.tasks_list.addItem(itemN)
            self.tasks_list.setItemWidget(itemN, widget)
        query.finish()
    
    def add_category(self):
        name = self.category_name.text()
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO categories 
              (
                  name
              ) 
              VALUES (?);
            """
        )
        
        query.addBindValue(name)
        query.exec()
        self.load_categories()
        query.finish()
        self.categories_window.close()
        self.categories_window = None

    def add_task(self):
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        category_id = self.categories[self.categories_combo_box.currentIndex()][0]
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO tasks (name, description, active, category_id) VALUES (?, ?, ?, ?);
            """
        )
        
        query.addBindValue(name)
        query.addBindValue(description)
        query.addBindValue(False)
        query.addBindValue(category_id)
        query.exec()
        self.load_tasks()
        query.finish()
        self.add_task_window.close()
        self.add_task_window = None

    def remove_task(self):
        if(self.tasks_list.currentRow() >= 0):
            query = QSqlQuery()
            query.prepare(
                """
                DELETE FROM tasks WHERE id = ?;
                """
            )
            query.addBindValue(self.tasks[self.tasks_list.currentRow()][0])
            query.exec()
            self.load_tasks()

    def swich_active(self):
        sender = self.sender()
        active = sender.isChecked()
        id = self.tasks[self.chechboxes_list.index(sender)][0]
        query = QSqlQuery()
        query.prepare(
            """
            UPDATE tasks SET active=? WHERE id=?;
            """
        )
        query.addBindValue(active)
        query.addBindValue(id)
        query.exec()
        self.load_tasks()

class AddTaskWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Добавить задачу")
        layout = QVBoxLayout(self)

        #Поля для ввода задачи
        self.parent_window.task_name = QLineEdit()
        self.parent_window.task_description = QTextEdit()
        layout.addWidget(self.parent_window.task_name)
        layout.addWidget(self.parent_window.task_description)
        categories_and_button_widget = QWidget()
        categories_and_button = QHBoxLayout()
        categories_and_button.addWidget(self.parent_window.categories_combo_box)
        edit_categories_button = QPushButton("...")
        edit_categories_button.clicked.connect(self.parent_window.show_categories_window)
        categories_and_button.addWidget(edit_categories_button)
        categories_and_button_widget.setLayout(categories_and_button)
        layout.addWidget(categories_and_button_widget)

        #Кнопка "Добавить задачу"
        add_task_button = QPushButton('Добавить задачу')
        add_task_button.resize(add_task_button.sizeHint())
        add_task_button.clicked.connect(self.parent_window.add_task)
        layout.addWidget(add_task_button)

class CategoriesWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Категории")
        layout = QVBoxLayout(self)

        layout.addWidget(self.parent_window.categories_list)

        self.parent_window.category_name = QLineEdit()
        layout.addWidget(self.parent_window.category_name)

        #Кнопка "Добавить категорию"
        add_category_button = QPushButton('Добавить категорию')
        add_category_button.resize(add_category_button.sizeHint())
        add_category_button.clicked.connect(self.parent_window.add_category)
        layout.addWidget(add_category_button)

class  Window(QWidget):
    def __init__(self, parent_window = None):
        super().__init__
        self.window_title = None
        self.this_window = None
        self.parent_window = parent_window
        self.children_windows = {}
        self.show_these_window()

    def init_UI(self):
        pass

    def show_this_window(self, size_x, size_y, window_title = 'Application window'):
        self.window_title = window_title
        self.setGeometry(size_x, size_y)
        self.setWindowTitle(self.window_title)
        self.show()

    def close_this_window(self):
        self.close()
        self.parent_window.open_window_as_child()

    def open_window_as_child(self, child_window_class, window_name, size_x, size_y):
        created_child_window = child_window_class(window_name, size_x, size_y)
        if(not self.children_windows.has_key(child_window_class)):
            self.children_windows[child_window_class] = created_child_window
        else:
            self.children_windows[child_window_class].close_this_window()

        created_child_window.show_this_window()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = ApplicationMainWindows()

    sys.exit(app.exec_())