# MY-PIEXIF - EXIF Data Editor

A Python tool for modifying EXIF (Exchangeable Image File Format) metadata in JPEG images. This tool allows you to edit camera parameters, GPS coordinates, and other metadata through a simple command-line interface.

## Features

- ✨ Modify camera parameters (ISO, aperture, exposure time, focal length, etc.)
- 📍 Set GPS coordinates (latitude, longitude, altitude)
- 📝 Edit image metadata (description, artist, copyright, etc.)
- 📅 Modify date/time information
- 🔒 Safe file handling (never overwrites original files)
- 🎯 Python 3.6+ compatible

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd my-piexif
```

2. No installation required! Just run the script directly.

## Quick Start / Testing

To quickly test the tool, you can run the included test script:

```bash
chmod +x test.sh
./test.sh
```

Or use bash/sh directly:

```bash
bash test.sh
# or
sh test.sh
```

The test script will modify `test/data/noexif.jpg` with various EXIF parameters and create a new file with a timestamp suffix.

## Usage

### Basic Syntax

```bash
python3 index.py <input_file> [output_file] [options]
```

### Options

#### Basic Information
- `--make` - Camera make (e.g., Canon, Nikon, Sony)
- `--model` - Camera model
- `--software` - Software version
- `--description` - Image description
- `--artist` - Artist/Photographer name
- `--copyright` - Copyright information

#### Shooting Parameters
- `--iso` - ISO sensitivity (e.g., 100, 200, 400, 800)
- `--fnumber` - Aperture value (e.g., 2.8 or f/2.8)
- `--exposure_time` - Exposure time (e.g., 1/125 or 0.008)
- `--focal_length` - Focal length in mm (e.g., 50)
- `--focal_length_35mm` - 35mm equivalent focal length in mm

#### Shooting Conditions
- `--exposure_program` - Exposure program (0=Undefined, 1=Manual, 2=Auto, 3=Auto Program, 4=Auto Bracket)
- `--exposure_bias` - Exposure bias in EV (e.g., +0.5 or -1.0)
- `--metering_mode` - Metering mode (0=Unknown, 1=Average, 2=Center-weighted, 3=Spot, 4=Multi-spot, 5=Multi-segment)
- `--light_source` - Light source (0=Unknown, 1=Daylight, 2=Fluorescent, 3=Tungsten, 4=Flash)
- `--white_balance` - White balance (0=Auto, 1=Manual)
- `--flash` - Flash mode (0=No Flash, 1=Flash, 5=Flash but no reflection detected, 7=Flash and reflection detected)
- `--scene_capture_type` - Scene capture type (0=Standard, 1=Landscape, 2=Portrait, 3=Night Scene)

#### Date and Time
- `--datetime_original` - Original date/time (format: YYYY:MM:DD HH:MM:SS, e.g., 2024:12:19 10:30:00)

#### GPS Information
- `--latitude` - Latitude (e.g., 39.9042 for Beijing)
- `--longitude` - Longitude (e.g., 116.4074 for Beijing)
- `--altitude` - Altitude in meters (optional)

## Examples

### Modify ISO and Aperture

```bash
python3 index.py photo.jpg --iso 400 --fnumber 2.8
```

### Modify Camera Make and Model

```bash
python3 index.py photo.jpg --make "Canon" --model "EOS 5D Mark IV"
```

### Modify Multiple Parameters

```bash
python3 index.py photo.jpg \
  --iso 800 \
  --fnumber 1.4 \
  --focal_length 85 \
  --exposure_time "1/250"
```

### Set GPS Coordinates

```bash
python3 index.py photo.jpg \
  --latitude 25.0330 \
  --longitude 121.5654
```

### Modify Date and Time

```bash
python3 index.py photo.jpg --datetime_original "2024:12:19 10:30:00"
```

### Complete Example

```bash
python3 index.py test/data/noexif.jpg \
  --make vivo \
  --model "iQOO Z9x" \
  --software "pexif 1.0" \
  --description "The beautiful scenery" \
  --artist "John Doe" \
  --copyright "© 2024 John Doe" \
  --iso 400 \
  --fnumber f/2.8 \
  --exposure_time "1/125" \
  --focal_length 60 \
  --focal_length_35mm 75 \
  --exposure_program 2 \
  --latitude 25.0330 \
  --longitude 121.5654
```

## File Handling

- **Default behavior**: If no output file is specified, a new file is created in the same directory as the input file with a timestamp suffix (e.g., `photo_modified_20241219_143204.jpg`)
- **Original files are never overwritten** - all modifications are saved to new files
- **Specify output**: Use the second positional argument to specify a custom output filename

```bash
# Auto-generate filename with timestamp
python3 index.py photo.jpg --iso 400

# Specify custom output filename
python3 index.py photo.jpg output.jpg --iso 400
```

## GPS Coordinates

The tool uses **WGS84 coordinate system** (standard for EXIF GPS data). All GPS coordinates are stored in WGS84 format according to EXIF specifications.

## Project Structure

```
pexif-master/
├── index.py          # Main script for modifying EXIF data
├── pexif.py          # Core library for EXIF manipulation
├── setup.py          # Package setup script
├── LICENSE           # MIT License
├── MANIFEST.in       # Package manifest
├── test.sh           # Test script
└── test/             # Test data directory
    └── data/         # Sample images for testing
```

## License

MIT License

Copyright (c) 2025-2026 heiheihoho

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Notes

- This tool modifies EXIF data in JPEG files only
- Original files are never overwritten (safety first!)
- Requires Python 3.6+ due to f-string usage
- All GPS coordinates are stored in WGS84 format (EXIF standard)

## Troubleshooting

### SyntaxError with f-strings

If you encounter `SyntaxError: invalid syntax` related to f-strings, make sure you're using Python 3.6 or higher:

```bash
python3 --version  # Should show 3.6 or higher
```

### File Not Found

Ensure the input image path is correct and the file exists:

```bash
ls -l photo.jpg  # Check if file exists
```

### Permission Errors

Make sure you have write permissions in the directory where you want to save the output file.

