
# from fastapi import FastAPI, File, UploadFile, Form, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import xml.etree.ElementTree as ET
# from deep_translator import GoogleTranslator
# import os
# import tempfile
# import uvicorn
# import shutil

# # Create required directories
# os.makedirs('static', exist_ok=True)
# os.makedirs('static/downloads', exist_ok=True)
# os.makedirs('templates', exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# # Serve favicon.ico from static directory
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     file_path = os.path.join("static", "favicon.ico")
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     return HTMLResponse(content="", status_code=204)

# # Translation function
# def translate_xml_labels(input_path, output_path, source_lang='en', target_lang='ar'):
#     try:
#         tree = ET.parse(input_path)
#         root = tree.getroot()
#         translator = GoogleTranslator(source=source_lang, target=target_lang)
        
#         for element in root.findall('.//queryDefinitionString'):
#             if 'label' in element.attrib:
#                 original = element.get('label')
#                 translated = translator.translate(original)
#                 element.set('label', translated)
        
#         tree.write(output_path, encoding='utf-8', xml_declaration=True)
#         return True
#     except Exception as e:
#         print(f"Translation error: {str(e)}")
#         return False

# @app.get("/", response_class=HTMLResponse)
# async def home_page(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/translate", response_class=HTMLResponse)
# async def handle_translation(
#     request: Request,
#     file: UploadFile = File(...),
#     source_lang: str = Form('en'),
#     target_lang: str = Form('ar')
# ):
#     # Save uploaded file to a temp file
#     file_ext = os.path.splitext(file.filename)[1]
#     with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
#         content = await file.read()
#         tmp.write(content)
#         input_path = tmp.name

#     # Prepare output file path in static/downloads
#     safe_base = os.path.splitext(os.path.basename(file.filename))[0]
#     output_filename = f"{safe_base}_{source_lang}_to_{target_lang}.xml"
#     output_path = os.path.join("static", "downloads", output_filename)
    
#     # Process translation
#     success = translate_xml_labels(input_path, output_path, source_lang, target_lang)
    
#     # Cleanup input file
#     try:
#         os.unlink(input_path)
#     except Exception:
#         pass
    
#     if not success:
#         return templates.TemplateResponse("index.html", {
#             "request": request,
#             "error": "Translation failed. Please check the XML format."
#         })
    
#     return templates.TemplateResponse("result.html", {
#         "request": request,
#         "filename": output_filename
#     })

# @app.get("/download/{filename}")
# async def download_translated_file(filename: str):
#     file_path = os.path.join("static", "downloads", filename)
#     if os.path.exists(file_path):
#         return FileResponse(
#             path=file_path,
#             filename=filename,
#             media_type='application/xml'
#         )
#     return HTMLResponse(content="File not found", status_code=404)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 
# from fastapi import FastAPI, File, UploadFile, Form, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import xml.etree.ElementTree as ET
# from deep_translator import GoogleTranslator
# import os
# import tempfile
# import uvicorn

# # Supported languages for dropdowns
# LANGUAGES = [
#     ("en", "English"),
#     ("ar", "Arabic"),
#     ("fr", "French"),
#     ("es", "Spanish"),
#     ("de", "German"),
#     ("hi", "Hindi"),
#     ("zh-CN", "Chinese (Simplified)"),
#     ("ja", "Japanese"),
#     ("ru", "Russian"),
#     ("it", "Italian"),
#     # Add more as needed
# ]

# # Create required directories
# os.makedirs('static', exist_ok=True)
# os.makedirs('static/downloads', exist_ok=True)
# os.makedirs('templates', exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     file_path = os.path.join("static", "favicon.ico")
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     return HTMLResponse(content="", status_code=204)

# def translate_xml_labels(input_path, output_path, source_lang='en', target_lang='ar'):
#     try:
#         tree = ET.parse(input_path)
#         root = tree.getroot()
#         translator = GoogleTranslator(source=source_lang, target=target_lang)
#         for element in root.findall('.//queryDefinitionString'):
#             if 'label' in element.attrib:
#                 original = element.get('label')
#                 translated = translator.translate(original)
#                 element.set('label', translated)
#         tree.write(output_path, encoding='utf-8', xml_declaration=True)
#         return True
#     except Exception as e:
#         print(f"Translation error: {str(e)}")
#         return False

# @app.get("/", response_class=HTMLResponse)
# async def home_page(request: Request):
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "languages": LANGUAGES
#     })

# @app.post("/translate", response_class=HTMLResponse)
# async def handle_translation(
#     request: Request,
#     file: UploadFile = File(...),
#     source_lang: str = Form('en'),
#     target_lang: str = Form('ar'),
#     custom_filename: str = Form('')
# ):
#     # Save uploaded file to a temp file
#     file_ext = os.path.splitext(file.filename)[1]
#     with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
#         content = await file.read()
#         tmp.write(content)
#         input_path = tmp.name

#     # Prepare output file path in static/downloads
#     safe_base = custom_filename.strip() or os.path.splitext(os.path.basename(file.filename))[0]
#     safe_base = "".join(x for x in safe_base if x.isalnum() or x in ('_', '-'))
#     output_filename = f"{safe_base}_{source_lang}_to_{target_lang}.xml"
#     output_path = os.path.join("static", "downloads", output_filename)
    
#     # Process translation
#     success = translate_xml_labels(input_path, output_path, source_lang, target_lang)
    
#     # Cleanup input file
#     try:
#         os.unlink(input_path)
#     except Exception:
#         pass
    
#     if not success:
#         return templates.TemplateResponse("index.html", {
#             "request": request,
#             "languages": LANGUAGES,
#             "error": "Translation failed. Please check the XML format."
#         })
    
#     return templates.TemplateResponse("result.html", {
#         "request": request,
#         "filename": output_filename
#     })

# @app.get("/download/{filename}")
# async def download_translated_file(filename: str):
#     file_path = os.path.join("static", "downloads", filename)
#     if os.path.exists(file_path):
#         return FileResponse(
#             path=file_path,
#             filename=filename,
#             media_type='application/xml'
#         )
#     return HTMLResponse(content="File not found", status_code=404)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# from fastapi import FastAPI, File, UploadFile, Form, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import xml.etree.ElementTree as ET
# from deep_translator import GoogleTranslator
# import os
# import tempfile
# import uvicorn

# # Supported languages for dropdowns
# LANGUAGES = [
#     ("en", "English"),
#     ("ar", "Arabic"),
#     ("fr", "French"),
#     ("es", "Spanish"),
#     ("de", "German"),
#     ("hi", "Hindi"),
#     ("zh-CN", "Chinese (Simplified)"),
#     ("ja", "Japanese"),
#     ("ru", "Russian"),
#     ("it", "Italian"),
#     # Add more as needed
# ]

# # Create required directories
# os.makedirs('static', exist_ok=True)
# os.makedirs('static/downloads', exist_ok=True)
# os.makedirs('templates', exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     file_path = os.path.join("static", "favicon.ico")
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     return HTMLResponse(content="", status_code=204)

# # Universal XML translation: translate all text nodes in the XML
# def translate_element(element, translator):
#     if element.text and element.text.strip():
#         try:
#             element.text = translator.translate(element.text.strip())
#         except Exception as e:
#             print(f"Error translating '{element.text}': {e}")
#     for child in element:
#         translate_element(child, translator)

# def translate_xml_labels(input_path, output_path, source_lang='en', target_lang='ar'):
#     try:
#         tree = ET.parse(input_path)
#         root = tree.getroot()
#         translator = GoogleTranslator(source=source_lang, target=target_lang)
#         translate_element(root, translator)
#         tree.write(output_path, encoding='utf-8', xml_declaration=True)
#         return True
#     except Exception as e:
#         print(f"Translation error: {str(e)}")
#         return False

# @app.get("/", response_class=HTMLResponse)
# async def home_page(request: Request):
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "languages": LANGUAGES
#     })

# @app.post("/translate", response_class=HTMLResponse)
# async def handle_translation(
#     request: Request,
#     file: UploadFile = File(...),
#     source_lang: str = Form('en'),
#     target_lang: str = Form('ar'),
#     custom_filename: str = Form('')
# ):
#     # Save uploaded file to a temp file
#     file_ext = os.path.splitext(file.filename)[1]
#     with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
#         content = await file.read()
#         tmp.write(content)
#         input_path = tmp.name

#     # Prepare output file path in static/downloads
#     safe_base = custom_filename.strip() or os.path.splitext(os.path.basename(file.filename))[0]
#     safe_base = "".join(x for x in safe_base if x.isalnum() or x in ('_', '-'))
#     output_filename = f"{safe_base}_{source_lang}_to_{target_lang}.xml"
#     output_path = os.path.join("static", "downloads", output_filename)
    
#     # Process translation
#     success = translate_xml_labels(input_path, output_path, source_lang, target_lang)
    
#     # Cleanup input file
#     try:
#         os.unlink(input_path)
#     except Exception:
#         pass
    
#     if not success:
#         return templates.TemplateResponse("index.html", {
#             "request": request,
#             "languages": LANGUAGES,
#             "error": "Translation failed. Please check the XML format."
#         })
    
#     return templates.TemplateResponse("result.html", {
#         "request": request,
#         "filename": output_filename
#     })

# @app.get("/download/{filename}")
# async def download_translated_file(filename: str):
#     file_path = os.path.join("static", "downloads", filename)
#     if os.path.exists(file_path):
#         return FileResponse(
#             path=file_path,
#             filename=filename,
#             media_type='application/xml'
#         )
#     return HTMLResponse(content="File not found", status_code=404)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# from fastapi import FastAPI, File, UploadFile, Form, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import xml.etree.ElementTree as ET
# from deep_translator import GoogleTranslator
# import os
# import tempfile
# import uvicorn
# import time  # For rate limiting

# # Supported languages for dropdowns
# LANGUAGES = [
#     ("en", "English"),
#     ("ar", "Arabic"),
#     ("fr", "French"),
#     ("es", "Spanish"),
#     ("de", "German"),
#     ("hi", "Hindi"),
#     ("zh-CN", "Chinese (Simplified)"),
#     ("ja", "Japanese"),
#     ("ru", "Russian"),
#     ("it", "Italian"),
#     # Add more as needed
# ]

# # Create required directories
# os.makedirs('static', exist_ok=True)
# os.makedirs('static/downloads', exist_ok=True)
# os.makedirs('templates', exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     file_path = os.path.join("static", "favicon.ico")
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     return HTMLResponse(content="", status_code=204)

# def translate_xml_element(element, translator):
#     """Recursively translate all text nodes in the XML element."""
#     if element.text and element.text.strip():
#         try:
#             element.text = translator.translate(element.text.strip())
#             time.sleep(0.5)  # Delay to avoid rate limiting
#         except Exception as e:
#             print(f"Error translating text '{element.text}': {e}")
#     for child in element:
#         translate_xml_element(child, translator)

# def translate_xml_file(input_path, output_path, source_lang='en', target_lang='ar'):
#     """Translate entire XML file text content from source_lang to target_lang."""
#     try:
#         tree = ET.parse(input_path)
#         root = tree.getroot()
#         translator = GoogleTranslator(source=source_lang, target=target_lang)
#         translate_xml_element(root, translator)
#         tree.write(output_path, encoding='utf-8', xml_declaration=True)
#         return True
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return False

# @app.get("/", response_class=HTMLResponse)
# async def home_page(request: Request):
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "languages": LANGUAGES
#     })

# @app.post("/translate", response_class=HTMLResponse)
# async def handle_translation(
#     request: Request,
#     file: UploadFile = File(...),
#     source_lang: str = Form('en'),
#     target_lang: str = Form('ar'),
#     custom_filename: str = Form('')
# ):
#     # Save uploaded file temporarily
#     file_ext = os.path.splitext(file.filename)[1]
#     with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
#         content = await file.read()
#         tmp.write(content)
#         input_path = tmp.name

#     # Prepare output filename and path
#     safe_base = custom_filename.strip() or os.path.splitext(os.path.basename(file.filename))[0]
#     safe_base = "".join(c for c in safe_base if c.isalnum() or c in ('_', '-'))
#     output_filename = f"{safe_base}_{source_lang}_to_{target_lang}.xml"
#     output_path = os.path.join("static", "downloads", output_filename)

#     # Translate XML
#     success = translate_xml_file(input_path, output_path, source_lang, target_lang)

#     # Remove temp input file
#     try:
#         os.unlink(input_path)
#     except Exception:
#         pass

#     if not success:
#         return templates.TemplateResponse("index.html", {
#             "request": request,
#             "languages": LANGUAGES,
#             "error": "Translation failed. Please check the XML format and try again."
#         })

#     return templates.TemplateResponse("result.html", {
#         "request": request,
#         "filename": output_filename
#     })

# @app.get("/download/{filename}")
# async def download_translated_file(filename: str):
#     file_path = os.path.join("static", "downloads", filename)
#     if os.path.exists(file_path):
#         return FileResponse(
#             path=file_path,
#             filename=filename,
#             media_type='application/xml'
#         )
#     return HTMLResponse(content="File not found", status_code=404)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
import os
import tempfile
import uvicorn
import time  # For rate limiting

# Supported languages for dropdowns
LANGUAGES = [
    ("en", "English"),
    ("ar", "Arabic"),
    ("fr", "French"),
    ("es", "Spanish"),
    ("de", "German"),
    ("hi", "Hindi"),
    ("zh-CN", "Chinese (Simplified)"),
    ("ja", "Japanese"),
    ("ru", "Russian"),
    ("it", "Italian"),
    # Add more as needed
]

# Create required directories
os.makedirs('static', exist_ok=True)
os.makedirs('static/downloads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    file_path = os.path.join("static", "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(content="", status_code=204)

def translate_xml_element(element, translator):
    """Recursively translate all text nodes and attribute values in the XML element."""
    # Translate element text
    if element.text and element.text.strip():
        try:
            element.text = translator.translate(element.text.strip())
            time.sleep(0.5)  # Delay to avoid rate limiting
        except Exception as e:
            print(f"Error translating text '{element.text}': {e}")
    # Translate element attributes
    for attr in element.attrib:
        if element.attrib[attr].strip():
            try:
                element.attrib[attr] = translator.translate(element.attrib[attr].strip())
                time.sleep(0.5)
            except Exception as e:
                print(f"Error translating attribute '{attr}': {e}")
    # Translate child elements recursively
    for child in element:
        translate_xml_element(child, translator)

def translate_xml_file(input_path, output_path, source_lang='en', target_lang='ar'):
    """Translate entire XML file text content and attributes from source_lang to target_lang."""
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translate_xml_element(root, translator)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        return True
    except Exception as e:
        print(f"Translation error: {e}")
        return False

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "languages": LANGUAGES
    })

@app.post("/translate", response_class=HTMLResponse)
async def handle_translation(
    request: Request,
    file: UploadFile = File(...),
    source_lang: str = Form('en'),
    target_lang: str = Form('ar'),
    custom_filename: str = Form('')
):
    # Save uploaded file temporarily
    file_ext = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        content = await file.read()
        tmp.write(content)
        input_path = tmp.name

    # Prepare output filename and path
    safe_base = custom_filename.strip() or os.path.splitext(os.path.basename(file.filename))[0]
    safe_base = "".join(c for c in safe_base if c.isalnum() or c in ('_', '-'))
    output_filename = f"{safe_base}_{source_lang}_to_{target_lang}.xml"
    output_path = os.path.join("static", "downloads", output_filename)

    # Translate XML
    success = translate_xml_file(input_path, output_path, source_lang, target_lang)

    # Remove temp input file
    try:
        os.unlink(input_path)
    except Exception:
        pass

    if not success:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "languages": LANGUAGES,
            "error": "Translation failed. Please check the XML format and try again."
        })

    return templates.TemplateResponse("result.html", {
        "request": request,
        "filename": output_filename
    })

@app.get("/download/{filename}")
async def download_translated_file(filename: str):
    file_path = os.path.join("static", "downloads", filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/xml'
        )
    return HTMLResponse(content="File not found", status_code=404)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

