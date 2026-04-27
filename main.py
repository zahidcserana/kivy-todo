import os
import traceback
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform
from database import init_db, get_all_todos, add_todo, toggle_todo, delete_todo, clear_done

if platform != "android":
    Window.size = (400, 700)


class TodoRow(RecycleDataViewBehavior, BoxLayout):
    todo_id = NumericProperty(0)
    title = StringProperty("")
    done = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        self.todo_id = data["todo_id"]
        self.title = data["title"]
        self.done = data["done"]
        return super().refresh_view_attrs(rv, index, data)

    def on_toggle(self):
        toggle_todo(self.todo_id)
        App.get_running_app().root.get_screen("list").refresh()

    def on_delete(self):
        delete_todo(self.todo_id)
        App.get_running_app().root.get_screen("list").refresh()


class TodoListView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def load_todos(self):
        todos = get_all_todos()
        self.data = [
            {"todo_id": t.id, "title": t.title, "done": t.done}
            for t in todos
        ]


class TodoListScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.refresh(), 0)

    def refresh(self):
        self.ids.todo_list.load_todos()

    def open_add_dialog(self):
        content = BoxLayout(orientation="vertical", spacing=12, padding=16)
        text_input = TextInput(
            hint_text="What needs to be done?",
            multiline=False,
            size_hint_y=None,
            height=48,
            font_size=16,
        )
        btn_row = BoxLayout(size_hint_y=None, height=44, spacing=8)
        cancel_btn = Button(text="Cancel", background_color=(0.5, 0.5, 0.5, 1))
        add_btn = Button(text="Add", background_color=(0.2, 0.6, 1, 1))

        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(add_btn)
        content.add_widget(text_input)
        content.add_widget(btn_row)

        popup = Popup(
            title="New Todo",
            content=content,
            size_hint=(0.9, None),
            height=180,
            auto_dismiss=False,
        )

        def do_add(_):
            title = text_input.text.strip()
            if title:
                add_todo(title)
                self.refresh()
            popup.dismiss()

        cancel_btn.bind(on_release=lambda _: popup.dismiss())
        add_btn.bind(on_release=do_add)
        text_input.bind(on_text_validate=do_add)
        popup.open()
        text_input.focus = True

    def confirm_clear_done(self):
        content = BoxLayout(orientation="vertical", spacing=12, padding=16)
        content.add_widget(Label(text="Remove all completed todos?"))
        btn_row = BoxLayout(size_hint_y=None, height=44, spacing=8)
        cancel_btn = Button(text="Cancel", background_color=(0.5, 0.5, 0.5, 1))
        ok_btn = Button(text="Clear", background_color=(1, 0.3, 0.3, 1))
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(ok_btn)
        content.add_widget(btn_row)

        popup = Popup(
            title="Clear Completed",
            content=content,
            size_hint=(0.85, None),
            height=160,
            auto_dismiss=True,
        )

        def do_clear(_):
            clear_done()
            self.refresh()
            popup.dismiss()

        cancel_btn.bind(on_release=lambda _: popup.dismiss())
        ok_btn.bind(on_release=do_clear)
        popup.open()


class TodoApp(App):
    def build(self):
        try:
            init_db(self.user_data_dir)
            kv_file = os.path.join(os.path.dirname(__file__), "ui.kv")
            Builder.load_file(kv_file)
            sm = ScreenManager()
            sm.add_widget(TodoListScreen(name="list"))
            return sm
        except Exception:
            # Write crash log to user_data_dir so it can be retrieved
            log_path = os.path.join(self.user_data_dir, "crash.log")
            with open(log_path, "w") as f:
                f.write(traceback.format_exc())
            raise


if __name__ == "__main__":
    TodoApp().run()
