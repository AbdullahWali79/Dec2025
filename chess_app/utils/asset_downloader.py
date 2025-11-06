"""
Asset Downloader - Downloads default chess piece images from open-license sources.
Fetches pieces from Wikimedia Commons if assets are missing.
"""

import os
import urllib.request
import urllib.error


# Wikimedia Commons URLs for chess pieces (public domain / CC0)
# Using standard chess piece images from Wikimedia Commons
WIKIMEDIA_BASE_URL = "https://upload.wikimedia.org/wikipedia/commons"
WIKIMEDIA_PIECES = {
    # White pieces
    'white_king': f"{WIKIMEDIA_BASE_URL}/4/42/Chess_klt45.svg",
    'white_queen': f"{WIKIMEDIA_BASE_URL}/1/15/Chess_qlt45.svg",
    'white_rook': f"{WIKIMEDIA_BASE_URL}/7/72/Chess_rlt45.svg",
    'white_bishop': f"{WIKIMEDIA_BASE_URL}/b/b1/Chess_blt45.svg",
    'white_knight': f"{WIKIMEDIA_BASE_URL}/7/70/Chess_nlt45.svg",
    'white_pawn': f"{WIKIMEDIA_BASE_URL}/4/45/Chess_plt45.svg",
    # Black pieces
    'black_king': f"{WIKIMEDIA_BASE_URL}/f/f0/Chess_kdt45.svg",
    'black_queen': f"{WIKIMEDIA_BASE_URL}/4/47/Chess_qdt45.svg",
    'black_rook': f"{WIKIMEDIA_BASE_URL}/f/ff/Chess_rdt45.svg",
    'black_bishop': f"{WIKIMEDIA_BASE_URL}/9/98/Chess_bdt45.svg",
    'black_knight': f"{WIKIMEDIA_BASE_URL}/e/ef/Chess_ndt45.svg",
    'black_pawn': f"{WIKIMEDIA_BASE_URL}/c/c7/Chess_pdt45.svg",
}

# Alternative: Lichess piece set (simpler, may need conversion)
# These are SVG format, which PyQt5 can handle


def download_piece_image(piece_name, destination_folder, progress_callback=None):
    """
    Download a chess piece image from Wikimedia Commons.
    
    Args:
        piece_name (str): Piece name (e.g., 'white_king')
        destination_folder (str): Folder to save the image
        progress_callback (callable, optional): Callback for progress updates
        
    Returns:
        bool: True if download successful, False otherwise
    """
    if piece_name not in WIKIMEDIA_PIECES:
        return False
    
    url = WIKIMEDIA_PIECES[piece_name]
    filename = f"{piece_name}.svg"  # Wikimedia provides SVG
    filepath = os.path.join(destination_folder, filename)
    
    # If we need PNG, we'll download SVG and note that conversion may be needed
    # For now, download SVG (PyQt5 can handle SVG)
    
    try:
        if progress_callback:
            progress_callback(f"Downloading {piece_name}...")
        
        # Create directory if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        
        # Download the file
        urllib.request.urlretrieve(url, filepath)
        
        if progress_callback:
            progress_callback(f"Downloaded {piece_name}")
        
        return True
    except urllib.error.URLError as e:
        if progress_callback:
            progress_callback(f"Error downloading {piece_name}: {str(e)}")
        return False
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error downloading {piece_name}: {str(e)}")
        return False


def download_all_pieces(destination_folder, progress_callback=None):
    """
    Download all chess piece images.
    
    Args:
        destination_folder (str): Folder to save images
        progress_callback (callable, optional): Callback for progress updates
        
    Returns:
        dict: Dictionary with piece names as keys and success status as values
    """
    results = {}
    piece_names = [
        'white_king', 'white_queen', 'white_rook', 'white_bishop', 
        'white_knight', 'white_pawn',
        'black_king', 'black_queen', 'black_rook', 'black_bishop',
        'black_knight', 'black_pawn'
    ]
    
    for piece_name in piece_names:
        success = download_piece_image(piece_name, destination_folder, progress_callback)
        results[piece_name] = success
    
    return results


def check_pieces_folder(folder_path):
    """
    Check if a folder contains all required chess piece images.
    
    Args:
        folder_path (str): Path to folder to check
        
    Returns:
        dict: Dictionary with piece names as keys and bool (exists) as values
    """
    required_pieces = [
        'white_king', 'white_queen', 'white_rook', 'white_bishop',
        'white_knight', 'white_pawn',
        'black_king', 'black_queen', 'black_rook', 'black_bishop',
        'black_knight', 'black_pawn'
    ]
    
    results = {}
    
    if not os.path.exists(folder_path):
        return {piece: False for piece in required_pieces}
    
    for piece_name in required_pieces:
        # Check for PNG first (preferred), then SVG
        png_path = os.path.join(folder_path, f"{piece_name}.png")
        svg_path = os.path.join(folder_path, f"{piece_name}.svg")
        results[piece_name] = os.path.exists(png_path) or os.path.exists(svg_path)
    
    return results


def ensure_default_pieces(folder_path, progress_callback=None):
    """
    Ensure default pieces are available, downloading if missing.
    
    Args:
        folder_path (str): Path to pieces folder
        progress_callback (callable, optional): Callback for progress updates
        
    Returns:
        bool: True if all pieces are available, False otherwise
    """
    # Check what pieces are missing
    piece_status = check_pieces_folder(folder_path)
    missing_pieces = [name for name, exists in piece_status.items() if not exists]
    
    if not missing_pieces:
        return True  # All pieces present
    
    if progress_callback:
        progress_callback(f"Downloading {len(missing_pieces)} missing pieces...")
    
    # Download missing pieces
    results = {}
    for piece_name in missing_pieces:
        success = download_piece_image(piece_name, folder_path, progress_callback)
        results[piece_name] = success
    
    # Check if all downloads were successful
    all_success = all(results.values())
    
    if progress_callback:
        if all_success:
            progress_callback("All pieces downloaded successfully!")
        else:
            failed = [name for name, success in results.items() if not success]
            progress_callback(f"Some pieces failed to download: {', '.join(failed)}")
    
    return all_success

