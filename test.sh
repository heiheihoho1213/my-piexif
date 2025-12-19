#!/bin/bash
# Test script for modifying EXIF data in images

# Use python3 explicitly (requires Python 3.6+)
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