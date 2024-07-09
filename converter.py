import flet as ft
import os
import json
import yaml
import xml.etree.ElementTree as ET

def read_file(file_path, input_format):
    with open(file_path, 'r') as file:
        if input_format == '.json':
            return json.load(file)
        elif input_format in ['.yml', '.yaml']:
            return yaml.safe_load(file)
        elif input_format == '.xml':
            tree = ET.parse(file)
            return tree.getroot()
    return None

def write_file(data, file_path, output_format):
    with open(file_path, 'wb') as file:  # otwarcie w trybie binarnym
        if output_format == '.json':
            file.write(json.dumps(data, indent=4).encode('utf-8'))
        elif output_format in ['.yml', '.yaml']:
            yaml.dump(data, file, allow_unicode=True)
        elif output_format == '.xml':
            # Konwersja słownika na XML
            def dict_to_xml(tag, d):
                elem = ET.Element(tag)
                for key, val in d.items():
                    child = ET.SubElement(elem, key)
                    child.text = str(val)
                return elem

            root = dict_to_xml('root', data)  # Główny element XML
            tree = ET.ElementTree(root)
            tree.write(file, encoding='utf-8', xml_declaration=True)

def convert_file(input_path, output_path, input_format, output_format):
    data = read_file(input_path, input_format)
    write_file(data, output_path, output_format)

def main(page: ft.Page):
    input_file_path = ft.Ref[ft.TextField]()
    output_dir_path = ft.Ref[ft.TextField]()
    output_format = ft.Ref[ft.Dropdown]()

    file_picker = ft.FilePicker(on_result=lambda e: on_file_picked(e, input_file_path))
    dir_picker = ft.FilePicker(on_result=lambda e: on_directory_picked(e, output_dir_path))

    page.overlay.extend([file_picker, dir_picker])

    def select_input_file(e):
        file_picker.pick_files()

    def select_output_directory(e):
        dir_picker.get_directory_path()

    def on_file_picked(e, input_ref):
        if e.files:
            input_ref.current.value = e.files[0].path
            input_ref.current.update()

    def on_directory_picked(e, output_ref):
        if e.path:
            output_ref.current.value = e.path
            output_ref.current.update()

    def show_snack_bar(message):
        snack = ft.SnackBar(ft.Text(message))
        page.overlay.append(snack)
        page.update()

    def on_convert(e):
        input_path = input_file_path.current.value
        output_dir = output_dir_path.current.value
        output_ext = output_format.current.value

        if not input_path or not output_dir or not output_ext:
            show_snack_bar("Please select all required fields")
            return

        input_ext = os.path.splitext(input_path)[1].lower()
        output_file_path = os.path.join(output_dir, f"converted{output_ext}")

        try:
            convert_file(input_path, output_file_path, input_ext, output_ext)
            show_snack_bar("File converted successfully")
        except Exception as ex:
            show_snack_bar(f"Error converting file: {ex}")

    page.title = "File Converter"
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("Select Input File:"),
                ft.TextField(ref=input_file_path, read_only=True),
                ft.IconButton(ft.icons.FOLDER_OPEN, on_click=select_input_file)
            ]),
            ft.Row([
                ft.Text("Select Output Directory:"),
                ft.TextField(ref=output_dir_path, read_only=True),
                ft.IconButton(ft.icons.FOLDER_OPEN, on_click=select_output_directory)
            ]),
            ft.Row([
                ft.Text("Select Output Format:"),
                ft.Dropdown(ref=output_format, options=[
                    ft.dropdown.Option(".xml"),
                    ft.dropdown.Option(".json"),
                    ft.dropdown.Option(".yml"),
                    ft.dropdown.Option(".yaml")
                ])
            ]),
            ft.ElevatedButton("Convert", on_click=on_convert)
        ])
    )

ft.app(target=main)
