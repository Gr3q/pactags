#!venv/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from db import dbsession


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


class DbEditor(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pactags")
        builder = Gtk.Builder()
        builder.add_from_file("db_editor/layout.glade")
        window = builder.get_object("main")

    def on_button_clicked(self, widget):
        dbsession.commit()


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("db_editor/layout.glade")
    builder.connect_signals(Handler())

    window = builder.get_object("main")
    window.show_all()
    Gtk.main()

