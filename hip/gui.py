from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
import random


class ContentWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Loading label
        self.loading_label = Label(
            text="Loading...", size_hint_y=None, height=50)

        # Content area for text or image
        self.content_area = BoxLayout(
            orientation='vertical', size_hint=(1, None), height=200)

        # Question
        self.question_label = Label(
            text="Does it appear to be human centric?", size_hint_y=None, height=40)

        # Options for the user to select
        self.options_layout = BoxLayout(
            size_hint_y=None, height=40, orientation='horizontal')
        self.options = ["Very Human-like",
                        "Somewhat Human-like", "Not Human-like", "Unsure"]
        self.user_response = None
        self.buttons = []
        for option in self.options:
            btn = Button(text=option, on_press=self.on_option_select)
            self.options_layout.add_widget(btn)
            self.buttons.append(btn)

        # Submit button
        self.submit_btn = Button(
            text="Submit", size_hint_y=None, height=50, on_press=self.submit_response)

        # Initial loading screen
        self.show_loading_screen()

    def show_loading_screen(self):
        self.clear_widgets()
        self.add_widget(self.loading_label)
        Clock.schedule_once(self.fetch_data, 1)

    def fetch_data(self, dt):
        self.generate_random_input()

    def generate_random_input(self, *args):
        # Simulate a 5-second delay for data fetching
        Clock.schedule_once(self.process_fetched_data, 5)

    def process_fetched_data(self, dt):
        # Simulate receiving new data
        types = ['text', 'image']
        chosen_type = random.choice(types)
        data = {}
        if chosen_type == 'text':
            data = {'text': f"Random text {random.randint(
                1, 100)}", 'type': 'text', 'id': random.randint(1, 10000)}
        else:
            data = {'image': 'https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/c24904d4-f0f0-4a26-9470-fec227dde15c/image-90.png',
                    'type': 'image', 'id': random.randint(1, 10000), 'text': f"Image caption {random.randint(1, 100)}"}
        self.update_content(data)

    def update_content(self, data):
        self.clear_widgets()
        self.content_area.clear_widgets()  # Clear existing content

        if data['type'] == 'text':
            self.content_area.add_widget(
                Label(text=data['text'], size_hint_y=None, height=100))
        elif data['type'] == 'image':
            img = AsyncImage(source=data['image'], allow_stretch=True,
                             keep_ratio=True, size_hint_y=None, height=400)
            self.content_area.add_widget(img)
            if 'text' in data:
                self.content_area.add_widget(
                    Label(text=data['text'], size_hint_y=None, height=50))

        self.add_widget(self.content_area)
        self.add_widget(self.question_label)
        self.add_widget(self.options_layout)
        self.add_widget(self.submit_btn)
        self.reset_options()

    def reset_options(self):
        for btn in self.buttons:
            btn.background_color = (1, 1, 1, 1)
        self.user_response = None

    def on_option_select(self, instance):
        self.user_response = instance.text
        # Highlight the selected button
        for btn in self.buttons:
            btn.background_color = (1, 1, 1, 1)  # Default color
        # Light grey to indicate selection
        instance.background_color = (0.7, 0.7, 0.7, 1)

    def submit_response(self, instance):
        if self.user_response:
            # Log the user's choice to the console
            print(f"User's choice: {self.user_response}")
            # Show loading screen while waiting for the next set of data
            self.show_loading_screen()
            # Simulate fetching new data with a delay
            # Adjust this delay as needed
            Clock.schedule_once(self.fetch_data, 1)


class MyApp(App):
    def build(self):
        self.title = 'Human Centric Content Evaluation'
        return ContentWidget()


if __name__ == '__main__':
    MyApp().run()
