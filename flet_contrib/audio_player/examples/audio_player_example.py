import flet as ft

from flet_contrib.audio_player import AudioPlayer


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        AudioPlayer(
            page=page,
            src="https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true",
            width=page.width / 2,
        )
    )


ft.app(main)
