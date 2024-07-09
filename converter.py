import sys
import os


def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def parse_arguments(args):
    if len(args) != 3:
        raise ValueError("Usage: ")

    input_file = args[1]
    output_file = args[2]

    input_format = get_file_extension(input_file)
    output_format = get_file_extension(output_file)

    supported_formats = ['.xml', '.json', '.yml', '.yaml']

    if input_format not in supported_formats:
        raise ValueError(f"Unsupported input file format: {input_format}")

    if output_format not in supported_formats:
        raise ValueError(f"Unsupported output file format: {output_format}")

    return input_file, output_file, input_format, output_format


def main():
    try:
        input_file, output_file, input_format, output_format = parse_arguments(sys.argv)
        print(f"Input file: {input_file} (format: {input_format})")
        print(f"Output file: {output_file} (format: {output_format})")
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
