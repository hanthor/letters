// window.rs — Letters main window: native GTK4 text editor.
// SPDX-License-Identifier: GPL-3.0-or-later

use gtk4 as gtk;
use gtk::prelude::*;
use libadwaita::prelude::AdwApplicationWindowExt;

pub struct LettersWindow {
    window: libadwaita::ApplicationWindow,
    editor: gtk::TextView,
}

impl LettersWindow {
    pub fn new(app: &libadwaita::Application) -> Self {
        let win = libadwaita::ApplicationWindow::new(Some("org.tunaos.letters"), Default::default());
        win.set_title(Some("Letters"));
        win.set_default_size(800, 600);

        let header = libadwaita::HeaderBar::new();
        let open_btn = gtk::Button::with_label("Open");
        header.pack_start(&open_btn);
        let save_btn = gtk::Button::with_label("Save");
        header.pack_start(&save_btn);

        let toolbar = gtk::Box::new(gtk::Orientation::Horizontal, 4);
        toolbar.set_halign(gtk::Align::Center);
        toolbar.add_css_class("toolbar");
        toolbar.append(&gtk::ToggleButton::with_label("B"));
        toolbar.append(&gtk::ToggleButton::with_label("I"));
        toolbar.append(&gtk::ToggleButton::with_label("U"));

        let editor = gtk::TextView::new();
        editor.set_monospace(true);
        editor.set_wrap_mode(gtk::WrapMode::Word);
        let scroll = gtk::ScrolledWindow::new();
        scroll.set_child(Some(&editor));
        scroll.set_vexpand(true);

        let main_box = gtk::Box::new(gtk::Orientation::Vertical, 0);
        main_box.append(&toolbar);
        main_box.append(&scroll);

        let status = gtk::Label::new(Some("0 words"));
        status.set_halign(gtk::Align::End);
        main_box.append(&status);

        let container = gtk::Box::new(gtk::Orientation::Vertical, 0);
        container.append(&header);
        container.append(&main_box);
        win.set_content(Some(&container));

        Self { window: win, editor }
    }

    pub fn present(&self) {
        self.window.present();
    }
}
