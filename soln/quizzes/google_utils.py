"""
Google API utilities for Drive and Slides operations.

This module provides common functions for:
- Authentication (OAuth 2.0 with token caching)
- Google Drive operations (upload, folders, sharing)
- Google Slides operations (create, copy, update)

Usage from scripts:
    from google_utils import load_credentials, upload_image, create_presentation
    
Usage from notebooks (running from sklearn/md/):
    import sys
    sys.path.insert(0, '..')
    from google_utils import load_credentials, upload_image, create_presentation

Workflow: Upload Images and Add to Slides
------------------------------------------
To upload multiple images and add them to a Google Slides presentation:

1. Load credentials and get services:
   ```python
   from google_utils import (
       load_credentials, get_services, upload_image, 
       add_image_slide, create_presentation, get_slide_count
   )
   
   creds = load_credentials()
   drive_service, slides_service = get_services(creds)
   ```

2. Create a new presentation (optional):
   ```python
   presentation_title = "My Image Slides"
   presentation_id = create_presentation(slides_service, presentation_title, drive_service)
   ```

3. Or use an existing presentation:
   ```python
   presentation_id = 'YOUR_PRESENTATION_ID'
   current_slide_count = get_slide_count(slides_service, presentation_id)
   ```

4. Upload images and add slides:
   ```python
   image_files = ['fig1.png', 'fig2.png', ...]
   for i, image_path in enumerate(image_files):
       # Upload to Drive (makes file publicly accessible)
       file_id, url = upload_image(drive_service, image_path, folder_id=None)
       
       # Add slide with image
       # For new presentation: insertion_index = i + 1 (skip title slide at 0)
       # For existing: insertion_index = current_slide_count + i
       insertion_index = i + 1  # or current_slide_count + i
       slide_id = add_image_slide(
           slides_service, 
           presentation_id, 
           url, 
           insertion_index=insertion_index
       )
   ```

See sklearn/scripts/upload_test_plots_to_slides.py for a complete example.
"""

import os
import pickle
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# ============================================================================
# Constants
# ============================================================================

# OAuth scopes
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.readonly',  # Read existing files
    'https://www.googleapis.com/auth/drive.file',      # Create/modify app files
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/documents'         # Google Docs access
]

# EMU units for slide layout (914400 EMU per inch)
EMU_PER_INCH = 914400
SLIDE_WIDTH = int(10 * EMU_PER_INCH)
SLIDE_HEIGHT = int(5.625 * EMU_PER_INCH)

# Default image placement on slides
IMAGE_X = int(0.5 * EMU_PER_INCH)
IMAGE_Y = int(0.5 * EMU_PER_INCH)
IMAGE_WIDTH = int(9.0 * EMU_PER_INCH)
IMAGE_HEIGHT = int(4.5 * EMU_PER_INCH)

# Title placement for slides
TITLE_X = int(0.5 * EMU_PER_INCH)
TITLE_Y = int(0.1 * EMU_PER_INCH)
TITLE_WIDTH = int(9.0 * EMU_PER_INCH)
TITLE_HEIGHT = int(0.4 * EMU_PER_INCH)

# Weekly reports folder ID
WEEKLY_REPORTS_FOLDER_ID = '1p6x3H6l2QANvYzkcUq7P4WXWJKY4p69-'


# ============================================================================
# Authentication
# ============================================================================

def get_sklearn_dir():
    """Get the sklearn directory path (works from scripts or notebooks)."""
    # Try to find sklearn dir relative to this file
    this_file = Path(__file__).resolve()
    if this_file.parent.name == 'sklearn':
        return this_file.parent
    # Fallback: assume we're in sklearn/
    return Path.cwd()


def load_credentials(token_path=None, credentials_path=None):
    """
    Load Google API credentials with token caching.
    
    Parameters:
    -----------
    token_path : str or Path, optional
        Path to token.pickle file. Defaults to sklearn/token.pickle
    credentials_path : str or Path, optional
        Path to credentials.json file. Defaults to sklearn/credentials.json
    
    Returns:
    --------
    google.oauth2.credentials.Credentials or None
    """
    sklearn_dir = get_sklearn_dir()
    
    if token_path is None:
        token_path = sklearn_dir / 'token.pickle'
    else:
        token_path = Path(token_path)
        
    if credentials_path is None:
        credentials_path = sklearn_dir / 'credentials.json'
    else:
        credentials_path = Path(credentials_path)
    
    creds = None
    
    # Load existing token
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            if not credentials_path.exists():
                print(f"ERROR: {credentials_path} not found.")
                print("Download credentials.json from Google Cloud Console:")
                print("  1. Go to https://console.cloud.google.com/apis/credentials")
                print("  2. Create OAuth 2.0 Client ID (Desktop app)")
                print(f"  3. Download JSON and save as {credentials_path}")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_services(creds=None):
    """
    Get Google Drive and Slides service objects.
    
    Parameters:
    -----------
    creds : Credentials, optional
        Google credentials. If None, loads from default location.
    
    Returns:
    --------
    tuple : (drive_service, slides_service)
    """
    if creds is None:
        creds = load_credentials()
        if not creds:
            return None, None
    
    drive_service = build('drive', 'v3', credentials=creds)
    slides_service = build('slides', 'v1', credentials=creds)
    
    return drive_service, slides_service

def get_docs_service(creds=None):
    """
    Get Google Docs service object.
    
    Parameters:
    -----------
    creds : Credentials, optional
        Google credentials. If None, loads from default location.
    
    Returns:
    --------
    Resource : Google Docs API service object or None
    """
    if creds is None:
        creds = load_credentials()
        if not creds:
            return None
    
    return build('docs', 'v1', credentials=creds)


def get_forms_service(creds=None):
    """
    Get Google Forms service object.
    
    Parameters:
    -----------
    creds : Credentials, optional
        Google credentials. If None, loads from default location.
    
    Returns:
    --------
    Resource : Google Forms API service object or None
    """
    if creds is None:
        creds = load_credentials()
        if not creds:
            return None
    
    return build('forms', 'v1', credentials=creds)


# ============================================================================
# Google Drive Operations
# ============================================================================

def upload_image(drive_service, image_path, folder_id=None, make_public=True):
    """
    Upload an image to Google Drive.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    image_path : str or Path
        Path to the image file
    folder_id : str, optional
        Drive folder ID to upload to
    make_public : bool, default True
        If True, make the file publicly accessible
    
    Returns:
    --------
    tuple : (file_id, shareable_url) or (None, None) on failure
    """
    image_path = Path(image_path)
    file_name = image_path.name
    
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Determine MIME type
    suffix = image_path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(suffix, 'application/octet-stream')
    
    try:
        media = MediaFileUpload(str(image_path), mimetype=mime_type, resumable=True)
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        
        if make_public:
            drive_service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()
        
        shareable_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        return file_id, shareable_url
        
    except HttpError as error:
        print(f"ERROR uploading {image_path}: {error}")
        return None, None


def upload_file_to_drive(drive_service, file_path, folder_id=None, mime_type=None, 
                         convert=False, make_public=False):
    """
    Upload any file to Google Drive.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    file_path : str or Path
        Path to the file to upload
    folder_id : str, optional
        Drive folder ID to upload to
    mime_type : str, optional
        MIME type of the file. If None, will be determined from file extension
    convert : bool, default False
        If True and file is convertible (HTML, DOCX, etc.), convert to Google Workspace format
    make_public : bool, default False
        If True, make the file publicly accessible
    
    Returns:
    --------
    tuple : (file_id, shareable_url) or (None, None) on failure
    """
    file_path = Path(file_path)
    file_name = file_path.name
    
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Determine MIME type if not provided
    if mime_type is None:
        suffix = file_path.suffix.lower()
        mime_types = {
            '.html': 'text/html',
            '.htm': 'text/html',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(suffix, 'application/octet-stream')
    
    try:
        media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
        
        # Upload file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, mimeType'
        ).execute()
        
        file_id = file.get('id')
        uploaded_mime_type = file.get('mimeType', mime_type)
        
        # For convertible files, copy with Google Docs MIME type to trigger conversion
        if convert and mime_type in ['text/html', 
                                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                     'application/msword']:
            try:
                # Copy the uploaded file with Google Docs MIME type
                copied_file = drive_service.files().copy(
                    fileId=file_id,
                    body={
                        'name': file_metadata['name'],
                        'mimeType': 'application/vnd.google-apps.document'
                    },
                    fields='id'
                ).execute()
                
                # Delete the original uploaded file
                drive_service.files().delete(fileId=file_id).execute()
                
                # Use the converted document
                file_id = copied_file.get('id')
                shareable_url = f"https://docs.google.com/document/d/{file_id}/edit"
            except HttpError as e:
                # If copy fails, use original file
                print(f"Warning: Could not convert file, using original: {e}")
                shareable_url = f"https://drive.google.com/file/d/{file_id}/view"
        else:
            shareable_url = f"https://drive.google.com/file/d/{file_id}/view"
        
        if make_public:
            drive_service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()
        
        return file_id, shareable_url
        
    except HttpError as error:
        print(f"ERROR uploading {file_path}: {error}")
        return None, None


def ensure_drive_folder(drive_service, folder_name, parent_id=None, make_public=True):
    """
    Find or create a Drive folder.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    folder_name : str
        Name of the folder
    parent_id : str, optional
        Parent folder ID
    make_public : bool, default True
        If True, make folder publicly accessible
    
    Returns:
    --------
    str : Folder ID or None on failure
    """
    try:
        query = (
            f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' "
            "and trashed=false"
        )
        if parent_id:
            query = f"{query} and '{parent_id}' in parents"
        
        results = drive_service.files().list(
            q=query, spaces='drive', fields='files(id, name)'
        ).execute()
        items = results.get('files', [])
        
        if items:
            folder_id = items[0]['id']
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            folder = drive_service.files().create(
                body=file_metadata, fields='id'
            ).execute()
            folder_id = folder.get('id')
        
        if make_public:
            try:
                drive_service.permissions().create(
                    fileId=folder_id,
                    body={'type': 'anyone', 'role': 'reader'},
                    fields='id'
                ).execute()
            except HttpError:
                pass  # May already be shared
        
        return folder_id
        
    except HttpError as error:
        print(f"ERROR with folder {folder_name}: {error}")
        return None


def move_file_to_folder(drive_service, file_id, folder_id):
    """
    Move a file to a specific folder.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    file_id : str
        ID of the file to move
    folder_id : str
        ID of the destination folder
    """
    file_meta = drive_service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ','.join(file_meta.get('parents', []))
    drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()


# ============================================================================
# Google Slides Operations
# ============================================================================

def create_presentation(slides_service, title, drive_service=None, folder_id=None):
    """
    Create a new Google Slides presentation.
    
    Parameters:
    -----------
    slides_service : Resource
        Google Slides API service object
    title : str
        Presentation title
    drive_service : Resource, optional
        Google Drive API service (required if folder_id is provided)
    folder_id : str, optional
        Move presentation to this folder after creation
    
    Returns:
    --------
    str : Presentation ID
    """
    presentation = slides_service.presentations().create(
        body={'title': title}
    ).execute()
    presentation_id = presentation.get('presentationId')
    
    if folder_id and drive_service:
        move_file_to_folder(drive_service, presentation_id, folder_id)
    
    return presentation_id


def copy_presentation(drive_service, template_id, new_title, folder_id=None, copy_permissions=True):
    """
    Copy an existing presentation.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    template_id : str
        ID of the template presentation to copy
    new_title : str
        Title for the new presentation
    folder_id : str, optional
        Move copy to this folder
    copy_permissions : bool, default True
        Copy sharing permissions from template
    
    Returns:
    --------
    str : New presentation ID or None on failure
    """
    try:
        # Copy the presentation
        copied_file = drive_service.files().copy(
            fileId=template_id,
            body={'name': new_title},
            fields='id'
        ).execute()
        new_id = copied_file.get('id')
        
        # Move to folder if specified
        if folder_id:
            move_file_to_folder(drive_service, new_id, folder_id)
        
        # Copy permissions
        if copy_permissions:
            try:
                permissions = drive_service.permissions().list(
                    fileId=template_id,
                    fields='permissions(type, role, emailAddress)'
                ).execute().get('permissions', [])
                
                for perm in permissions:
                    if perm.get('type') == 'user' and perm.get('emailAddress'):
                        try:
                            drive_service.permissions().create(
                                fileId=new_id,
                                body={
                                    'type': 'user',
                                    'role': perm.get('role', 'reader'),
                                    'emailAddress': perm.get('emailAddress')
                                },
                                sendNotificationEmail=False
                            ).execute()
                        except HttpError:
                            pass
            except HttpError:
                pass
        
        return new_id
        
    except HttpError as error:
        print(f"ERROR copying presentation: {error}")
        return None


def get_slide_count(slides_service, presentation_id):
    """Get the number of slides in a presentation."""
    presentation = slides_service.presentations().get(
        presentationId=presentation_id
    ).execute()
    return len(presentation.get('slides', []))


def update_title_slide(slides_service, presentation_id, title=None, subtitle=None):
    """
    Update the title slide text.
    
    Parameters:
    -----------
    slides_service : Resource
        Google Slides API service object
    presentation_id : str
        Presentation ID
    title : str, optional
        New title text
    subtitle : str, optional
        New subtitle text
    """
    presentation = slides_service.presentations().get(
        presentationId=presentation_id
    ).execute()
    
    slides = presentation.get('slides', [])
    if not slides:
        return
    
    title_slide = slides[0]
    requests = []
    
    for element in title_slide.get('pageElements', []):
        shape = element.get('shape', {})
        placeholder = shape.get('placeholder', {})
        placeholder_type = placeholder.get('type', '')
        object_id = element.get('objectId')
        
        # Check if element has text content (to avoid deleteText on empty elements)
        text_content = shape.get('text', {})
        has_text = False
        for text_elem in text_content.get('textElements', []):
            if text_elem.get('textRun', {}).get('content', '').strip():
                has_text = True
                break
        
        if placeholder_type in ['CENTERED_TITLE', 'TITLE'] and title:
            # Delete existing text first (only if there's text)
            if has_text:
                requests.append({
                    'deleteText': {
                        'objectId': object_id,
                        'textRange': {'type': 'ALL'}
                    }
                })
            requests.append({
                'insertText': {
                    'objectId': object_id,
                    'text': title,
                    'insertionIndex': 0
                }
            })
        elif placeholder_type == 'SUBTITLE' and subtitle:
            if has_text:
                requests.append({
                    'deleteText': {
                        'objectId': object_id,
                        'textRange': {'type': 'ALL'}
                    }
                })
            requests.append({
                'insertText': {
                    'objectId': object_id,
                    'text': subtitle,
                    'insertionIndex': 0
                }
            })
    
    if requests:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()


def add_image_slide(slides_service, presentation_id, image_url, insertion_index=None,
                   slide_id=None, image_x=None, image_y=None, image_width=None, image_height=None):
    """
    Add a slide with an image.
    
    Parameters:
    -----------
    slides_service : Resource
        Google Slides API service object
    presentation_id : str
        Presentation ID
    image_url : str
        URL of the image (must be publicly accessible)
    insertion_index : int, optional
        Where to insert the slide (default: end)
    slide_id : str, optional
        Custom slide ID (auto-generated if not provided)
    image_x, image_y : int, optional
        Image position in EMU (defaults to module constants)
    image_width, image_height : int, optional
        Image size in EMU (defaults to module constants)
    
    Returns:
    --------
    str : The slide ID
    """
    if slide_id is None:
        import uuid
        slide_id = f"slide_{uuid.uuid4().hex[:8]}"
    
    image_id = f"image_{slide_id}"
    
    # Use defaults if not specified
    if image_x is None:
        image_x = IMAGE_X
    if image_y is None:
        image_y = IMAGE_Y
    if image_width is None:
        image_width = IMAGE_WIDTH
    if image_height is None:
        image_height = IMAGE_HEIGHT
    
    requests = []
    
    # Create slide
    create_slide_request = {
        'createSlide': {
            'objectId': slide_id
        }
    }
    if insertion_index is not None:
        create_slide_request['createSlide']['insertionIndex'] = insertion_index
    requests.append(create_slide_request)
    
    # Add image
    requests.append({
        'createImage': {
            'objectId': image_id,
            'url': image_url,
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': image_width, 'unit': 'EMU'},
                    'height': {'magnitude': image_height, 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': image_x,
                    'translateY': image_y,
                    'unit': 'EMU'
                }
            }
        }
    })
    
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()
    
    return slide_id


def add_section_slide(slides_service, presentation_id, title, insertion_index=None):
    """
    Add a section header slide.
    
    Parameters:
    -----------
    slides_service : Resource
        Google Slides API service object
    presentation_id : str
        Presentation ID
    title : str
        Section title text
    insertion_index : int, optional
        Where to insert the slide
    
    Returns:
    --------
    str : The slide ID
    """
    import uuid
    slide_id = f"section_{uuid.uuid4().hex[:8]}"
    
    requests = [{
        'createSlide': {
            'objectId': slide_id,
            'slideLayoutReference': {
                'predefinedLayout': 'SECTION_HEADER'
            }
        }
    }]
    if insertion_index is not None:
        requests[0]['createSlide']['insertionIndex'] = insertion_index
    
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()
    
    # Get the slide to find the title placeholder
    presentation = slides_service.presentations().get(
        presentationId=presentation_id
    ).execute()
    
    for slide in presentation.get('slides', []):
        if slide.get('objectId') == slide_id:
            for element in slide.get('pageElements', []):
                shape = element.get('shape', {})
                placeholder = shape.get('placeholder', {})
                if placeholder.get('type') in ['TITLE', 'CENTERED_TITLE']:
                    slides_service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': [{
                            'insertText': {
                                'objectId': element.get('objectId'),
                                'text': title,
                                'insertionIndex': 0
                            }
                        }]}
                    ).execute()
                    break
    
    return slide_id


def add_text_slide(slides_service, presentation_id, text, insertion_index=None,
                   font_size=22, font_family='Calibri'):
    """
    Add a slide with formatted text.
    
    Parameters:
    -----------
    slides_service : Resource
        Google Slides API service object
    presentation_id : str
        Presentation ID
    text : str
        Text content for the slide
    insertion_index : int, optional
        Where to insert the slide (default: end)
    font_size : int, default 22
        Font size in points
    font_family : str, default 'Calibri'
        Font family name
    
    Returns:
    --------
    str : The slide ID
    """
    import uuid
    slide_id = f"text_{uuid.uuid4().hex[:8]}"
    text_box_id = f"textbox_{slide_id}"
    
    # Text box dimensions (centered, with margins)
    text_x = int(0.5 * EMU_PER_INCH)
    text_y = int(0.5 * EMU_PER_INCH)
    text_width = int(9.0 * EMU_PER_INCH)
    text_height = int(4.5 * EMU_PER_INCH)
    
    requests = []
    
    # Create slide
    create_slide_request = {
        'createSlide': {
            'objectId': slide_id
        }
    }
    if insertion_index is not None:
        create_slide_request['createSlide']['insertionIndex'] = insertion_index
    requests.append(create_slide_request)
    
    # Create text box
    requests.append({
        'createShape': {
            'objectId': text_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': text_width, 'unit': 'EMU'},
                    'height': {'magnitude': text_height, 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': text_x,
                    'translateY': text_y,
                    'unit': 'EMU'
                }
            }
        }
    })
    
    # Insert text with formatting
    requests.append({
        'insertText': {
            'objectId': text_box_id,
            'text': text,
            'insertionIndex': 0
        }
    })
    
    # Apply formatting to all text
    requests.append({
        'updateTextStyle': {
            'objectId': text_box_id,
            'style': {
                'fontSize': {
                    'magnitude': font_size,
                    'unit': 'PT'
                },
                'fontFamily': font_family
            },
            'textRange': {
                'type': 'ALL'
            },
            'fields': 'fontSize,fontFamily'
        }
    })
    
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()
    
    return slide_id


# ============================================================================
# High-level Convenience Functions
# ============================================================================

def upload_images_and_create_slides(image_paths, presentation_title, 
                                    folder_id=WEEKLY_REPORTS_FOLDER_ID):
    """
    Upload images and create a presentation with one slide per image.
    
    Parameters:
    -----------
    image_paths : list of str/Path
        Paths to image files
    presentation_title : str
        Title for the presentation
    folder_id : str, optional
        Drive folder to store presentation and images
    
    Returns:
    --------
    str : Presentation URL or None on failure
    """
    creds = load_credentials()
    if not creds:
        return None
    
    drive_service, slides_service = get_services(creds)
    
    # Create presentation
    presentation_id = create_presentation(
        slides_service, presentation_title, drive_service, folder_id
    )
    
    # Upload images and add slides
    for i, image_path in enumerate(image_paths):
        file_id, url = upload_image(drive_service, image_path)
        if file_id and url:
            add_image_slide(slides_service, presentation_id, url, insertion_index=i+1)
    
    return f"https://docs.google.com/presentation/d/{presentation_id}/edit"


# ============================================================================
# Markdown to Google Docs Operations
# ============================================================================

def markdown_to_html(md_path):
    """
    Convert markdown file to HTML using pandoc.
    
    Parameters:
    -----------
    md_path : str or Path
        Path to markdown file
    
    Returns:
    --------
    str : HTML content
    
    Raises:
    -------
    RuntimeError: If pandoc is not available or conversion fails
    """
    import subprocess
    
    md_path = Path(md_path)
    
    # Check if pandoc is available
    try:
        subprocess.run(['pandoc', '--version'], 
                      capture_output=True, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("pandoc is not installed or not in PATH. Install pandoc to use this function.")
    
    # Convert markdown to HTML using pandoc
    try:
        result = subprocess.run(
            ['pandoc', str(md_path), '-f', 'markdown', '-t', 'html', '--standalone'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"pandoc conversion failed: {e.stderr}")


def markdown_to_docx(md_path):
    """
    Convert markdown file to DOCX using pandoc.
    
    Parameters:
    -----------
    md_path : str or Path
        Path to markdown file
    
    Returns:
    --------
    Path : Path to temporary DOCX file
    
    Raises:
    -------
    RuntimeError: If pandoc is not available or conversion fails
    """
    import subprocess
    import tempfile
    
    md_path = Path(md_path)
    
    # Check if pandoc is available
    try:
        subprocess.run(['pandoc', '--version'], 
                      capture_output=True, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("pandoc is not installed or not in PATH. Install pandoc to use this function.")
    
    # Create temporary DOCX file
    docx_path = Path(tempfile.mktemp(suffix='.docx'))
    
    # Convert markdown to DOCX using pandoc
    try:
        subprocess.run(
            ['pandoc', str(md_path), '-f', 'markdown', '-t', 'docx', '-o', str(docx_path)],
            capture_output=True,
            check=True
        )
        return docx_path
    except subprocess.CalledProcessError as e:
        # Clean up on error
        try:
            docx_path.unlink()
        except Exception:
            pass
        raise RuntimeError(f"pandoc conversion failed: {e.stderr.decode('utf-8', errors='ignore')}")


def markdown_to_google_docs(md_path, title, folder_id, drive_service, make_public=False):
    """
    Convert markdown to DOCX, upload to Drive, convert to Google Docs.
    
    Parameters:
    -----------
    md_path : str or Path
        Path to markdown file
    title : str
        Title for the Google Doc
    folder_id : str
        Drive folder ID to upload to
    drive_service : Resource
        Google Drive API service object
    make_public : bool, default False
        If True, make the document publicly accessible
    
    Returns:
    --------
    str : Google Docs URL or None on failure
    """
    md_path = Path(md_path)
    
    # Convert markdown to DOCX using pandoc
    docx_path = markdown_to_docx(md_path)
    
    try:
        # Upload DOCX with convert=True to create Google Doc
        file_id, url = upload_file_to_drive(
            drive_service,
            docx_path,
            folder_id=folder_id,
            mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            convert=True,  # This converts DOCX to Google Docs
            make_public=make_public
        )
        
        if file_id:
            # Rename the document to the desired title
            try:
                drive_service.files().update(
                    fileId=file_id,
                    body={'name': title},
                    fields='id'
                ).execute()
            except HttpError:
                pass  # Rename failed, but document was created
        
        return url
        
    finally:
        # Clean up temp DOCX file
        try:
            docx_path.unlink()
        except Exception:
            pass


# ============================================================================
# Google Forms Operations
# ============================================================================

def create_quiz_form(forms_service, title, description=None, shuffle_option_order=True):
    """
    Create a new Google Form and enable quiz mode.
    
    Parameters:
    -----------
    forms_service : Resource
        Google Forms API service object
    title : str
        Form title
    description : str, optional
        Form description (set via batchUpdate after creation)
    shuffle_option_order : bool, default True
        Whether to shuffle option order for multiple choice questions
        (Note: This may need to be set per-question or manually in UI)
    
    Returns:
    --------
    str : Form ID or None on failure
    """
    try:
        # Only title can be set during creation
        form = {
            "info": {
                "title": title
            }
        }
        
        # Create the form
        result = forms_service.forms().create(body=form).execute()
        form_id = result['formId']
        
        # Build batch update requests
        requests = []
        
        # Enable quiz mode
        requests.append({
            "updateSettings": {
                "settings": {
                    "quizSettings": {
                        "isQuiz": True
                    }
                },
                "updateMask": "quizSettings.isQuiz"
            }
        })
        
        # Add description if provided
        if description:
            requests.append({
                "updateFormInfo": {
                    "info": {
                        "description": description
                    },
                    "updateMask": "description"
                }
            })
        
        # Apply all updates
        if requests:
            forms_service.forms().batchUpdate(
                formId=form_id,
                body={"requests": requests}
            ).execute()
        
        return form_id
        
    except HttpError as error:
        print(f"ERROR creating quiz form: {error}")
        return None


def add_quiz_question(forms_service, form_id, question_text, options, 
                     correct_answer_index, points=1, required=True,
                     correct_feedback=None, incorrect_feedback=None,
                     shuffle_option_order=True, location_index=None):
    """
    Add a multiple choice quiz question to a Google Form.
    
    Parameters:
    -----------
    forms_service : Resource
        Google Forms API service object
    form_id : str
        Form ID
    question_text : str
        Question text (may include markdown-like formatting)
    options : list of str
        List of answer options (4 options expected)
    correct_answer_index : int
        Index of the correct answer (0-based)
    points : int, default 1
        Point value for this question
    required : bool, default True
        Whether the question is required
    correct_feedback : str, optional
        Feedback text shown when answer is correct
    incorrect_feedback : str, optional
        Feedback text shown when answer is incorrect
    shuffle_option_order : bool, default True
        Whether to shuffle the order of options
    location_index : int, optional
        Index where to insert the question (None = append)
    
    Returns:
    --------
    str : Question/item ID or None on failure
    """
    try:
        if correct_answer_index < 0 or correct_answer_index >= len(options):
            print(f"ERROR: correct_answer_index {correct_answer_index} out of range for {len(options)} options")
            return None
        
        # Build choice question
        choice_question = {
            "type": "RADIO",
            "options": [{"value": opt} for opt in options]
        }
        
        # Note: shuffleOptionOrder is not supported in the Forms API v1
        # Option shuffling must be enabled manually in the Google Forms UI
        
        # Build grading object
        grading = {
            "pointValue": points,
            "correctAnswers": {
                "answers": [{"value": options[correct_answer_index]}]
            }
        }
        
        # Add feedback
        if correct_feedback:
            grading["whenRight"] = {"text": correct_feedback}
        if incorrect_feedback:
            grading["whenWrong"] = {"text": incorrect_feedback}
        
        # Build question
        question = {
            "required": required,
            "choiceQuestion": choice_question,
            "grading": grading
        }
        
        # Build create item request
        item = {
            "title": question_text,
            "questionItem": {
                "question": question
            }
        }
        
        request = {
            "createItem": {
                "item": item
            }
        }
        
        if location_index is not None:
            request["createItem"]["location"] = {"index": location_index}
        
        # Execute batch update
        result = forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": [request]}
        ).execute()
        
        # Extract item ID from response
        if result.get("replies") and len(result["replies"]) > 0:
            return result["replies"][0].get("createItem", {}).get("item", {}).get("itemId")
        
        return None
        
    except HttpError as error:
        print(f"ERROR adding quiz question: {error}")
        return None


def add_quiz_questions_batch(forms_service, form_id, questions_data, 
                            shuffle_option_order=True, batch_size=50, starting_index=0):
    """
    Add multiple quiz questions to a form in batches.
    
    Parameters:
    -----------
    forms_service : Resource
        Google Forms API service object
    form_id : str
        Form ID
    questions_data : list of dict
        List of question dictionaries, each with:
        - question_text: str
        - options: list of str
        - correct_answer_index: int
        - points: int (optional, default 1)
        - correct_feedback: str (optional)
        - incorrect_feedback: str (optional)
    shuffle_option_order : bool, default True
        Whether to shuffle option order
    batch_size : int, default 50
        Number of questions to add per batch
    starting_index : int, default 0
        Starting index for item location (use 1 if intro text is at index 0)
    
    Returns:
    --------
    list of str : List of item IDs for created questions
    """
    requests = []
    item_count = starting_index
    item_ids = []
    
    for q_data in questions_data:
        question_text = q_data['question_text']
        options = q_data['options']
        correct_answer_index = q_data['correct_answer_index']
        points = q_data.get('points', 1)
        correct_feedback = q_data.get('correct_feedback')
        incorrect_feedback = q_data.get('incorrect_feedback')
        
        if correct_answer_index < 0 or correct_answer_index >= len(options):
            print(f"ERROR: Skipping question with invalid correct_answer_index")
            continue
        
        # Build choice question
        choice_question = {
            "type": "RADIO",
            "options": [{"value": opt} for opt in options]
        }
        
        # Note: shuffleOptionOrder is not supported in the Forms API v1
        # Option shuffling must be enabled manually in the Google Forms UI
        # or may be available in future API versions
        
        # Build grading
        grading = {
            "pointValue": points,
            "correctAnswers": {
                "answers": [{"value": options[correct_answer_index]}]
            }
        }
        
        if correct_feedback:
            grading["whenRight"] = {"text": correct_feedback}
        if incorrect_feedback:
            grading["whenWrong"] = {"text": incorrect_feedback}
        
        # Build question
        question = {
            "required": True,
            "choiceQuestion": choice_question,
            "grading": grading
        }
        
        # Build create item request
        requests.append({
            "createItem": {
                "item": {
                    "title": question_text,
                    "questionItem": {
                        "question": question
                    }
                },
                "location": {"index": item_count}
            }
        })
        
        item_count += 1
    
    # Execute in batches
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i+batch_size]
        try:
            result = forms_service.forms().batchUpdate(
                formId=form_id,
                body={"requests": batch}
            ).execute()
            
            # Debug: print result structure
            if i == 0:  # Only print for first batch
                import json
                print(f"  DEBUG: Batch update result keys: {list(result.keys())}")
                if "replies" in result:
                    print(f"  DEBUG: Number of replies: {len(result['replies'])}")
                    if result["replies"]:
                        print(f"  DEBUG: First reply keys: {list(result['replies'][0].keys())}")
            
            # Extract item IDs from replies
            # Structure: reply["createItem"]["itemId"] (not nested under "item")
            for reply in result.get("replies", []):
                if "createItem" in reply:
                    item_id = reply["createItem"].get("itemId")
                    if item_id:
                        item_ids.append(item_id)
            
        except HttpError as error:
            print(f"ERROR in batch {i//batch_size + 1}: {error}")
            print(f"  Error details: {error.error_details if hasattr(error, 'error_details') else 'No details'}")
            print(f"  Error content: {error.content if hasattr(error, 'content') else 'No content'}")
            # Print first request for debugging
            if batch:
                import json
                print(f"  First request in batch: {json.dumps(batch[0], indent=2)}")
        except Exception as e:
            print(f"ERROR in batch {i//batch_size + 1}: Unexpected error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    return item_ids


def get_form_urls(form_id):
    """
    Get edit and responder URLs for a form.
    
    Parameters:
    -----------
    form_id : str
        Form ID
    
    Returns:
    --------
    tuple : (edit_url, responder_url)
    """
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    responder_url = f"https://docs.google.com/forms/d/e/{form_id}/viewform"
    return edit_url, responder_url


def add_intro_text_item(forms_service, form_id, title, description, location_index=0):
    """
    Add an introduction text item to a Google Form.
    
    Parameters:
    -----------
    forms_service : Resource
        Google Forms API service object
    form_id : str
        Form ID
    title : str
        Title for the introduction section
    description : str
        Description/intro text (supports basic formatting)
    location_index : int, default 0
        Index where to insert the item
    
    Returns:
    --------
    str : Item ID or None on failure
    """
    try:
        request = {
            "createItem": {
                "item": {
                    "title": title,
                    "description": description,
                    "textItem": {}
                },
                "location": {"index": location_index}
            }
        }
        
        result = forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": [request]}
        ).execute()
        
        # Extract item ID from response
        if result.get("replies") and len(result["replies"]) > 0:
            return result["replies"][0].get("createItem", {}).get("item", {}).get("itemId")
        
        return None
        
    except HttpError as error:
        print(f"ERROR adding intro text: {error}")
        print(f"  Error details: {error.error_details if hasattr(error, 'error_details') else 'No details'}")
        print(f"  Error content: {error.content if hasattr(error, 'content') else 'No content'}")
        import json
        print(f"  Request: {json.dumps(request, indent=2)}")
        return None
    except Exception as e:
        print(f"ERROR adding intro text: Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def move_form_to_folder(drive_service, form_id, folder_id):
    """
    Move a Google Form to a specific Drive folder.
    
    Note: Forms are Drive files, so we can use the same move_file_to_folder function,
    but this is a convenience wrapper with a clearer name.
    
    Parameters:
    -----------
    drive_service : Resource
        Google Drive API service object
    form_id : str
        Form ID (which is also a Drive file ID)
    folder_id : str
        ID of the destination folder
    """
    move_file_to_folder(drive_service, form_id, folder_id)

