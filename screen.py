#!/usr/bin/python

import argparse
import gc
import json
import logging
import os
import subprocess
import pathlib
import traceback  # noqa
import locale
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango
from importlib import import_module
from jinja2 import Environment
from signal import SIGTERM
from datetime import datetime

logging.getLogger("urllib3").setLevel(logging.WARNING)
gi.require_version("Gtk", "3.0")

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ginger Updater")

        button = Gtk.Button(label="Ask me later")
        button.connect("clicked", self.on_askMeLater_button_clicked)
        
        self.add(button)
        
        button = Gtk.Button(label="Update now")
        button.connect("clicked", self.on_button_clicked)
        self.add(button)
        
    def on_askMeLater_button_clicked(self, widget):
        Gtk.main_quit()

    def on_updateNow_button_clicked(self, widget):
        Gtk.main_quit()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

