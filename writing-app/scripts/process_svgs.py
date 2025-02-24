import os
import xml.etree.ElementTree as ET

# Register SVG and other namespaces
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")


def process_svg(input_path, output_path):
    # Parse SVG
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Function to process an element and its children
    def process_element(elem):
        # Handle any element that might have style or direct color attributes
        style = elem.get("style", "")
        if style:
            # Replace colors in style attribute
            replacements = [
                ("fill:#000000", "fill:#ffffff"),
                ("fill:#000", "fill:#fff"),
                ("stroke:#000000", "stroke:#ffffff"),
                ("stroke:#000", "stroke:#fff"),
                ("stroke:none", "stroke:#ffffff"),
                ("fill-opacity:1", "fill-opacity:1;stroke:#ffffff"),
            ]
            for old, new in replacements:
                style = style.replace(old, new)
            elem.set("style", style)

        # Handle direct color attributes
        if elem.get("fill") == "#000000" or elem.get("fill") == "#000":
            elem.set("fill", "#ffffff")
        if elem.get("stroke") == "#000000" or elem.get("stroke") == "#000":
            elem.set("stroke", "#ffffff")
        if elem.get("stroke") == "none":
            elem.set("stroke", "#ffffff")

        # Process all child elements
        for child in elem:
            process_element(child)

    # Process the entire tree
    process_element(root)

    # Write modified SVG
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def main():
    input_dir = "sitelen_pona_svgs"
    output_dir = "sitelen_pona_svgs_dark"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all SVGs
    for filename in os.listdir(input_dir):
        if filename.endswith(".svg"):
            # Add _dark suffix before .svg extension
            base_name = filename[:-4]  # remove .svg
            dark_filename = f"{base_name}_dark.svg"

            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, dark_filename)
            process_svg(input_path, output_path)
            print(f"Processed: {filename} -> {dark_filename}")


if __name__ == "__main__":
    main()
