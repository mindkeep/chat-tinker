"""
Main flet entry point to have a dialogue with the user and an LLM
"""

import flet as ft


class MessageEntry(ft.Row):
    """
    Message entry control
    """

    def __init__(self, author: str, message: str, parent: ft.Column) -> None:
        """
        Initialize the message entry control
        """
        super().__init__()
        self.author = author  # Store the author of the message
        self.saved_content = message  # Store the initial message content
        self.me_parent = parent  # Reference to the parent container for removal

        # Create a text field for displaying the message content
        self.text_box = ft.TextField(
            label=self.author,
            value=self.saved_content,
            multiline=True,
            disabled=True,
            expand=True,
        )
        # Button to enable editing of the message
        self.edit_button = ft.ElevatedButton(
            text="Edit", on_click=self.on_edit
        )
        # Button to save the edited message, hidden by default
        self.save_button = ft.ElevatedButton(
            text="Save", on_click=self.on_save, visible=False
        )
        # Button to cancel editing, hidden by default
        self.cancel_button = ft.ElevatedButton(
            text="Cancel", on_click=self.on_cancel, visible=False
        )
        # Button to delete the message
        self.delete_button = ft.ElevatedButton(
            text="Delete", on_click=self.on_delete
        )

        # List of controls for easy management
        self.controls = [
            self.text_box,
            self.edit_button,
            self.save_button,
            self.cancel_button,
            self.delete_button,
        ]

    def on_edit(self, _: ft.ControlEvent) -> None:
        """
        Handle the edit button click event:
        - Hide the edit and delete buttons
        - Show the save and cancel buttons
        - Enable the text box for editing
        - Focus the text box
        """
        self.edit_button.visible = False
        self.save_button.visible = True
        self.cancel_button.visible = True
        self.delete_button.visible = False
        self.text_box.disabled = False
        self.text_box.focus()
        self.update()

    def on_save(self, _: ft.ControlEvent) -> None:
        """
        Handle the save button click event:
        - Save the edited content
        - Show the edit and delete buttons
        - Hide the save and cancel buttons
        - Disable the text box to prevent editing
        """
        self.saved_content = self.text_box.value
        self.edit_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.delete_button.visible = True
        self.text_box.disabled = True
        self.update()

    def on_cancel(self, _: ft.ControlEvent) -> None:
        """
        Handle the cancel button click event:
        - Revert the text box content to the saved content
        - Show the edit and delete buttons
        - Hide the save and cancel buttons
        - Disable the text box to prevent editing
        """
        self.text_box.value = self.saved_content
        self.edit_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.delete_button.visible = True
        self.text_box.disabled = True
        self.update()

    def on_delete(self, _: ft.ControlEvent) -> None:
        """
        Handle the delete button click event:
        - Remove this control from the parent container
        - Update the parent container to reflect the change
        """
        self.me_parent.controls.remove(self)
        self.me_parent.update()


class STMainPage(ft.Column):
    """
    Main page for the StoryTeller application.
    This class represents the main interface of the application, where users can interact
    by sending messages and viewing a history of messages.
    """

    def __init__(self) -> None:
        """
        Initialize the main page by setting up the message history, input box, and send button.
        """
        super().__init__()

        # Message history container where all messages will be displayed
        self.msg_hist = ft.Column()

        # Add a welcome message from the system to the message history
        self.msg_hist.controls.append(
            MessageEntry(
                author="Setting",
                message="Welcome to the Chat-Tinker GUI!",
                parent=self.msg_hist,
            )
        )

        # Add an initial message from the AI to the message history
        self.msg_hist.controls.append(
            MessageEntry(
                author="AI",
                message="Type 'exit' to exit the application.",
                parent=self.msg_hist,
            )
        )

        # Input box for the user to type their message
        self.input_box = ft.TextField(label="You", expand=True, multiline=True)

        # Send button to submit the user's message
        self.send_button = ft.ElevatedButton(text="Send", on_click=self.on_send)

        # Layout for the input box and send button
        input_layout = ft.Row(
            controls=[
                self.input_box,
                self.send_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Add the message history, a divider, and the input layout to the main page controls
        self.controls = [
            self.msg_hist,
            ft.Divider(),
            input_layout
        ]

    def on_send(self, _: ft.ControlEvent) -> None:
        """
        Handle the send button click event:
        - Add the user's message to the message history
        - Clear the input box
        - Add a placeholder AI response to the message history
        - Update the UI and refocus on the input box
        """
        # Add the user's message to the message history
        self.msg_hist.controls.append(
            MessageEntry(
                author="You",
                message=str(self.input_box.value),
                parent=self.msg_hist,
            )
        )

        # Clear the input box after sending the message
        self.input_box.value = ""

        # Add a placeholder AI response to the message history
        response_box = MessageEntry(
            author="AI",
            message="Processing...",
            parent=self.msg_hist,
        )
        self.msg_hist.controls.append(response_box)

        # Update the UI to reflect the changes and refocus on the input box
        self.update()
        self.input_box.focus()


def main(page: ft.Page) -> None:
    """
    Main entry point for the Chat-Tinker GUI
    """

    # Set the page title, theme, and scroll mode
    page.title = "Chat-Tinker"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS
    
    # Add the main page to the page controls
    page.add(STMainPage())


def run(web: bool = False) -> None:
    """
    Run the StoryTeller application
    """

    if web:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main)


if __name__ == "__main__":
    run()
