# Sitelen Glyphs Web Scraper and Processing Scripts

This directory contains the scripts used to download all the glyphs from [Sona Pona Wiki](https://sona.pona.la/wiki/sitelen_pona/) and process them.

## How to Run the Scripts

The requirements to run these scripts have been excluded from `pyproject.toml` because these scripts are not intended to be run at all (again) for this project to work. They were run only once to download and process the images and are included here only for reference.

Note that while the web scraper uses only python libraries, the svg processor requires `Cairo` to be installed on the machine, e.g., via `brew install cairo` on Mac OS.

## Legal and Ethical Considerations of Web Scraping

The Sona Pona Wiki content is available under CC BY-SA 3.0 license. To minimise impact on the server, the web scraper script was run only once to download and process the images.
