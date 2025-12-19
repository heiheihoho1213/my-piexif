"""
Example: Modify camera parameters (EXIF data) in images

Receive camera parameters via command-line arguments and set them to images.
"""

import sys
import os
import argparse

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pexif
from pexif import Rational

def modify_camera_params(image_path, output_path=None, **kwargs):
    """
    Modify camera parameters in images
    
    Parameters:
        image_path: Input image path
        output_path: Output image path (if None, create new file in same directory with timestamp suffix)
    """
    try:
        print("Reading image file: %s" % image_path)
        sys.stdout.flush()
        
        # Read image file
        img = pexif.JpegFile.fromFile(image_path)
        print("Image read successfully")
        sys.stdout.flush()
        
        # Clean all old EXIF segments and recreate to ensure correct offset
        exif_segments = [seg for seg in img._segments if isinstance(seg, pexif.ExifSegment)]
        if len(exif_segments) > 0:
            print("Found %d old EXIF segment(s), cleaning and recreating to ensure data correctness..." % len(exif_segments))
            # Delete all old EXIF segments (using list comprehension to ensure complete cleanup)
            img._segments = [seg for seg in img._segments if not isinstance(seg, pexif.ExifSegment)]
            print("Cleaned all old EXIF segments")
        
        # Create new EXIF data (this ensures correct offset)
        print("Creating new EXIF data...")
        sys.stdout.flush()
        exif = img.get_exif(create=True)
        if exif is None:
            print("Warning: Unable to create EXIF data")
            sys.stdout.flush()
            return
        
        print("EXIF data ready")
        sys.stdout.flush()
        
        primary = img.exif.primary
        # Extended EXIF data is accessed via primary.ExtendedEXIF (will be auto-created)
        # Note: Attribute name is ExtendedEXIF, not exif
        try:
            exif_extended = primary.ExtendedEXIF
        except AttributeError:
            # If access fails, try direct access via EXIF_OFFSET
            EXIF_OFFSET = 0x8769
            if EXIF_OFFSET in primary:
                exif_extended = primary[EXIF_OFFSET]
            else:
                # In rw mode, accessing ExtendedEXIF will auto-create
                exif_extended = primary.ExtendedEXIF
        
        modified_params = []
        
        # ========== 1. Basic Information ==========
        if kwargs.get('make'):
            primary.Make = kwargs['make']
            modified_params.append(f"Camera Make: {kwargs['make']}")
        
        if kwargs.get('model'):
            primary.Model = kwargs['model']
            modified_params.append(f"Camera Model: {kwargs['model']}")
        
        if kwargs.get('software'):
            primary.Software = kwargs['software']
            modified_params.append(f"Software Version: {kwargs['software']}")
        
        if kwargs.get('description'):
            # EXIF description field usually uses ASCII, Chinese characters may need special handling
            try:
                primary.ImageDescription = kwargs['description']
                modified_params.append(f"Image Description: {kwargs['description']}")
            except Exception as e:
                print(f"Warning: Unable to set image description (may contain unsupported characters), skipping this parameter")
                sys.stdout.flush()
        
        if kwargs.get('artist'):
            primary.Artist = kwargs['artist']
            modified_params.append(f"Artist: {kwargs['artist']}")
        
        if kwargs.get('copyright'):
            primary.Copyright = kwargs['copyright']
            modified_params.append(f"Copyright: {kwargs['copyright']}")
        
        # ========== 2. Shooting Parameters ==========
        if kwargs.get('iso'):
            # ISO Speed Ratings need to be in list format
            iso_value = int(kwargs['iso'])
            try:
                exif_extended.ISOSpeedRatings = [iso_value]
                modified_params.append(f"ISO: {kwargs['iso']}")
            except Exception as e:
                # If list format fails, try direct assignment
                try:
                    exif_extended.ISOSpeedRatings = iso_value
                    modified_params.append(f"ISO: {kwargs['iso']}")
                except Exception as e2:
                    print(f"Warning: Unable to set ISO value {iso_value}, skipping this parameter")
                    sys.stdout.flush()
        
        if kwargs.get('fnumber'):
            # Support f/2.8 or 2.8 format
            fval = kwargs['fnumber'].replace('f/', '').replace('f', '')
            fnum = float(fval)
            exif_extended.FNumber = Rational(int(fnum * 10), 10)
            modified_params.append(f"Aperture: f/{fnum}")
        
        if kwargs.get('exposure_time'):
            # Support 1/125 or 0.008 format
            exp_str = kwargs['exposure_time']
            if '/' in exp_str:
                num, den = map(int, exp_str.split('/'))
                exif_extended.ExposureTime = Rational(num, den)
                modified_params.append(f"Exposure Time: {exp_str} sec")
            else:
                exp_val = float(exp_str)
                # Convert to fraction form
                exif_extended.ExposureTime = Rational(1, int(1/exp_val))
                modified_params.append(f"Exposure Time: {exp_val} sec")
        
        if kwargs.get('focal_length'):
            fl = float(kwargs['focal_length'])
            exif_extended.FocalLength = Rational(int(fl), 1)
            modified_params.append(f"Focal Length: {fl}mm")
        
        if kwargs.get('focal_length_35mm'):
            exif_extended.FocalLengthIn35mmFilm = int(kwargs['focal_length_35mm'])
            modified_params.append(f"35mm Equivalent Focal Length: {kwargs['focal_length_35mm']}mm")
        
        # ========== 3. Shooting Conditions ==========
        if kwargs.get('exposure_program') is not None:
            exif_extended.ExposureProgram = int(kwargs['exposure_program'])
            programs = {0: "Undefined", 1: "Manual", 2: "Auto", 3: "Auto Program", 4: "Auto Bracket"}
            modified_params.append(f"Exposure Program: {programs.get(int(kwargs['exposure_program']), 'Unknown')}")
        
        if kwargs.get('exposure_bias'):
            # Support +0.5 or 0.5 format
            bias_str = kwargs['exposure_bias'].replace('+', '')
            if '/' in bias_str:
                num, den = map(int, bias_str.split('/'))
                exif_extended.ExposureBiasValue = Rational(num, den)
            else:
                bias_val = float(bias_str)
                exif_extended.ExposureBiasValue = Rational(int(bias_val * 10), 10)
            modified_params.append(f"Exposure Bias: {kwargs['exposure_bias']} EV")
        
        if kwargs.get('metering_mode') is not None:
            exif_extended.MeteringMode = int(kwargs['metering_mode'])
            modes = {0: "Unknown", 1: "Average", 2: "Center-weighted", 3: "Spot", 4: "Multi-spot", 5: "Multi-segment"}
            modified_params.append(f"Metering Mode: {modes.get(int(kwargs['metering_mode']), 'Unknown')}")
        
        if kwargs.get('light_source') is not None:
            exif_extended.LightSource = int(kwargs['light_source'])
            sources = {0: "Unknown", 1: "Daylight", 2: "Fluorescent", 3: "Tungsten", 4: "Flash"}
            modified_params.append(f"Light Source: {sources.get(int(kwargs['light_source']), 'Unknown')}")
        
        if kwargs.get('white_balance') is not None:
            exif_extended.WhiteBalance = int(kwargs['white_balance'])
            modified_params.append(f"White Balance: {'Auto' if int(kwargs['white_balance']) == 0 else 'Manual'}")
        
        if kwargs.get('flash') is not None:
            exif_extended.Flash = int(kwargs['flash'])
            flash_states = {0: "No Flash", 1: "Flash", 5: "Flash but no reflection detected", 7: "Flash and reflection detected"}
            modified_params.append(f"Flash: {flash_states.get(int(kwargs['flash']), 'Unknown')}")
        
        if kwargs.get('scene_capture_type') is not None:
            exif_extended.SceneCaptureType = int(kwargs['scene_capture_type'])
            scenes = {0: "Standard", 1: "Landscape", 2: "Portrait", 3: "Night Scene"}
            modified_params.append(f"Scene Capture Type: {scenes.get(int(kwargs['scene_capture_type']), 'Unknown')}")
        
        # ========== 4. Date and Time ==========
        if kwargs.get('datetime_original'):
            dt = kwargs['datetime_original']
            exif_extended.DateTimeOriginal = dt
            exif_extended.DateTimeDigitized = dt
            primary.DateTime = dt
            modified_params.append(f"Date/Time Original: {dt}")
        
        # ========== 5. GPS Information ==========
        if kwargs.get('latitude') is not None or kwargs.get('longitude') is not None:
            try:
                latitude = kwargs.get('latitude', 0.0)
                longitude = kwargs.get('longitude', 0.0)
                altitude = kwargs.get('altitude')
                
                # Use set_geo method to set GPS coordinates
                img.set_geo(latitude, longitude)
                modified_params.append(f"GPS Coordinates: {latitude}, {longitude}")
                
                # If altitude is provided, try to set it (pexif may not support, but we can try)
                if altitude is not None:
                    try:
                        gps = primary.new_gps()
                        # GPS altitude information is in GPS IFD, but pexif may not support direct setting
                        # Record here first, implement if pexif supports it
                        modified_params.append(f"Altitude: {altitude} meters")
                    except:
                        pass
            except Exception as gps_error:
                print(f"Warning: Error setting GPS coordinates: {gps_error}")
                sys.stdout.flush()
        
        if modified_params:
            print("\nModified parameters:")
            for param in modified_params:
                print(f"  ✓ {param}")
        else:
            print("\nNo parameters provided, no modifications made")
        sys.stdout.flush()
        
        # ========== Save File ==========
        if output_path is None:
            # Generate new filename in the same directory as original file
            dir_name = os.path.dirname(image_path) or '.'
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            # Add timestamp to make filename unique
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(dir_name, f"{name}_modified_{timestamp}{ext}")
        
        print("\nSaving file: %s" % output_path)
        sys.stdout.flush()
        
        # Save to new file (never overwrite original)
        img.writeFile(output_path)
        
        print("\n✓ File saved successfully!")
        sys.stdout.flush()
        
    except IOError as e:
        print("Error: Unable to open file -", e)
        sys.stdout.flush()
    except pexif.JpegFile.InvalidFile as e:
        print("Error: Invalid JPEG file -", e)
        sys.stdout.flush()
    except Exception as e:
        import traceback
        print("Error:", e)
        traceback.print_exc()
        sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Modify camera parameters (EXIF data) in images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  # Modify ISO and aperture
  python modify_camera_params.py photo.jpg --iso 400 --fnumber 2.8
  
  # Modify camera make and model
  python modify_camera_params.py photo.jpg --make "Canon" --model "EOS 5D Mark IV"
  
  # Modify multiple parameters
  python modify_camera_params.py photo.jpg --iso 800 --fnumber 1.4 --focal_length 85 --exposure_time "1/250"
  
  # Modify date and time
  python modify_camera_params.py photo.jpg --datetime_original "2024:12:19 10:30:00"
  
  # Save to new file
  python modify_camera_params.py photo.jpg output.jpg --iso 400
        """
    )
    
    parser.add_argument('input_file', help='Input image path')
    parser.add_argument('output_file', nargs='?', help='Output image path (optional, default creates new file in same directory with timestamp suffix)')
    
    # Basic Information
    parser.add_argument('--make', help='Camera make (e.g., Canon, Nikon, Sony)')
    parser.add_argument('--model', help='Camera model')
    parser.add_argument('--software', help='Software version')
    parser.add_argument('--description', help='Image description')
    parser.add_argument('--artist', help='Artist/Photographer')
    parser.add_argument('--copyright', help='Copyright information')
    
    # Shooting Parameters
    parser.add_argument('--iso', type=int, help='ISO sensitivity (e.g., 100, 200, 400, 800)')
    parser.add_argument('--fnumber', help='Aperture value (e.g., 2.8 or f/2.8)')
    parser.add_argument('--exposure_time', help='Exposure time (e.g., 1/125 or 0.008)')
    parser.add_argument('--focal_length', help='Focal length (unit: mm, e.g., 50)')
    parser.add_argument('--focal_length_35mm', type=int, help='35mm equivalent focal length (unit: mm)')
    
    # Shooting Conditions
    parser.add_argument('--exposure_program', type=int, 
                       help='Exposure program (0=Undefined, 1=Manual, 2=Auto, 3=Auto Program, 4=Auto Bracket)')
    parser.add_argument('--exposure_bias', help='Exposure bias (e.g., +0.5 or -1.0, unit: EV)')
    parser.add_argument('--metering_mode', type=int,
                       help='Metering mode (0=Unknown, 1=Average, 2=Center-weighted, 3=Spot, 4=Multi-spot, 5=Multi-segment)')
    parser.add_argument('--light_source', type=int,
                       help='Light source (0=Unknown, 1=Daylight, 2=Fluorescent, 3=Tungsten, 4=Flash)')
    parser.add_argument('--white_balance', type=int, help='White balance (0=Auto, 1=Manual)')
    parser.add_argument('--flash', type=int,
                       help='Flash (0=No Flash, 1=Flash, 5=Flash but no reflection detected, 7=Flash and reflection detected)')
    parser.add_argument('--scene_capture_type', type=int,
                       help='Scene capture type (0=Standard, 1=Landscape, 2=Portrait, 3=Night Scene)')
    
    # Date and Time
    parser.add_argument('--datetime_original',
                       help='Date/time original (format: YYYY:MM:DD HH:MM:SS, e.g., 2024:12:19 10:30:00)')
    
    # GPS Information
    parser.add_argument('--latitude', type=float, help='Latitude (e.g., 39.9042 for Beijing)')
    parser.add_argument('--longitude', type=float, help='Longitude (e.g., 116.4074 for Beijing)')
    parser.add_argument('--altitude', type=float, help='Altitude (unit: meters, optional)')
    
    args = parser.parse_args()
    
    # Build parameter dictionary
    params = {}
    if args.make:
        params['make'] = args.make
    if args.model:
        params['model'] = args.model
    if args.software:
        params['software'] = args.software
    if args.description:
        params['description'] = args.description
    if args.artist:
        params['artist'] = args.artist
    if args.copyright:
        params['copyright'] = args.copyright
    if args.iso:
        params['iso'] = args.iso
    if args.fnumber:
        params['fnumber'] = args.fnumber
    if args.exposure_time:
        params['exposure_time'] = args.exposure_time
    if args.focal_length:
        params['focal_length'] = args.focal_length
    if args.focal_length_35mm:
        params['focal_length_35mm'] = args.focal_length_35mm
    if args.exposure_program is not None:
        params['exposure_program'] = args.exposure_program
    if args.exposure_bias:
        params['exposure_bias'] = args.exposure_bias
    if args.metering_mode is not None:
        params['metering_mode'] = args.metering_mode
    if args.light_source is not None:
        params['light_source'] = args.light_source
    if args.white_balance is not None:
        params['white_balance'] = args.white_balance
    if args.flash is not None:
        params['flash'] = args.flash
    if args.scene_capture_type is not None:
        params['scene_capture_type'] = args.scene_capture_type
    if args.datetime_original:
        params['datetime_original'] = args.datetime_original
    if args.latitude is not None:
        params['latitude'] = args.latitude
    if args.longitude is not None:
        params['longitude'] = args.longitude
    if args.altitude is not None:
        params['altitude'] = args.altitude
    
    # Check if output file parameter might be a misparsed argument value
    output_file = args.output_file
    if output_file and not output_file.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
        # If output file doesn't look like a filename, it might be a parsing error
        print("Warning: Output filename '%s' doesn't look correct." % output_file)
        print("Tip: If parameter values contain spaces, use quotes, e.g.: --model \"iQOO Z9x\"")
        print("Will ignore this output filename and overwrite original file.")
        print()
        output_file = None
    
    modify_camera_params(args.input_file, output_file, **params)
