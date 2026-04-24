import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button


class GalleryLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        images_dir = os.path.join(os.path.dirname(__file__), "images")
        self.image_files = [os.path.join(images_dir, f)
                            for f in os.listdir(images_dir)
                            if os.path.isfile(os.path.join(images_dir, f))]

        self.index = 0

        self.main_image = AsyncImage(
            source=self.image_files[self.index],
            size_hint=(1, 0.9)
        )

        self.add_widget(self.main_image)

        btn_layout = BoxLayout(size_hint=(1, 0.1))

        self.prev_btn = Button(text="◀Previous")
        self.next_btn = Button(text="Next ▶")

        self.prev_btn.bind(on_press=self.prev_image)
        self.next_btn.bind(on_press=self.next_image)

        btn_layout.add_widget(self.prev_btn)
        btn_layout.add_widget(self.next_btn)

        self.add_widget(btn_layout)

    def next_image(self, instance):
        self.index += 1
        if self.index >= len(self.image_files):
            self.index = 0
        self.main_image.source = self.image_files[self.index]

    def prev_image(self, instance):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.image_files) - 1
        self.main_image.source = self.image_files[self.index]


class GalleryApp(App):
    def build(self):
        gallery_layout = GalleryLayout()
        scroll_view = ScrollView()
        scroll_view.add_widget(gallery_layout)
        return scroll_view


if __name__ == '__main__':
    GalleryApp().run()
