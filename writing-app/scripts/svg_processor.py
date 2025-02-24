import io
from pathlib import Path

import cairosvg  # For SVG conversion
import cv2
import numpy as np
from PIL import Image


class SitelenPonaTemplateProcessor:
    def __init__(self, input_dir, output_dir, size=(100, 100)):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.size = size
        self.output_dir.mkdir(exist_ok=True)

    def process_svg(self, svg_path):
        """Convert SVG to PNG and preprocess for template matching"""
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(
            url=str(svg_path),
            output_width=self.size[0],
            output_height=self.size[1],
            background_color="white",
        )

        # Convert to numpy array
        image = Image.open(io.BytesIO(png_data))
        image_array = np.array(image)

        # Convert to grayscale if needed
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Threshold to create binary image
        _, binary = cv2.threshold(image_array, 127, 255, cv2.THRESH_BINARY)

        return binary

    def process_all(self):
        """Process all SVG files in the input directory"""
        for svg_file in self.input_dir.glob("*.svg"):
            try:
                # Process the SVG
                processed = self.process_svg(svg_file)

                # Save as PNG
                output_path = self.output_dir / f"{svg_file.stem}.png"
                cv2.imwrite(str(output_path), processed)

                print(f"Processed: {svg_file.name} -> {output_path.name}")

            except Exception as e:
                print(f"Error processing {svg_file.name}: {e}")


def main():
    # Example usage
    processor = SitelenPonaTemplateProcessor(
        input_dir="sitelen_pona_svgs", output_dir="templates", size=(100, 100)
    )
    processor.process_all()


if __name__ == "__main__":
    main()
