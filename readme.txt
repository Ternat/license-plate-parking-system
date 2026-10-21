============================================================
Car License Plate Recognition Smart Parking System
Student: Li Wenhao
University: University of Aberdeen
============================================================


================================================================
SECTION 1: CONTENTS OF THE SUBMISSION ARCHIVE
================================================================

The submission archive contains the following directories and files:

readme.txt                  - This file. Instructions and project overview.
README.md                   - Project documentation (Markdown format).
first_start.bat             - One-click setup and startup script (Windows).
test_images/                - Sample vehicle images for demonstration and testing.

backend/                    - Backend service (FastAPI, Python)
  requirements.txt          - Python dependency list
  app/
    main.py                 - FastAPI application entry point; sets up CORS, routers, and exception handlers
    core/
      config.py             - Centralised configuration (database URL, model paths, device setting, pricing rules: 5.0/hour after 2 free hours)
      database.py           - SQLAlchemy database session and engine setup
      security.py           - Password hashing and JWT token utilities
    models/
      user.py               - Database model for administrator accounts
      parking.py            - Database model for parking records (entry/exit timestamps, fees, status)
    schemas/                - Pydantic request/response schemas for API validation
    api/
      v1/
        endpoints/
          auth.py           - Admin login and JWT authentication endpoint
          parking.py        - Vehicle entry and exit management endpoints
          recognition.py    - Standalone plate recognition endpoint (for testing)
          records.py        - Historical parking record query and management endpoints
    algorithm/
      pipeline.py           - Orchestrates the full ALPR pipeline: Enhancement -> Detection -> Correction -> OCR
      enhancement/
        enhancer.py         - Image preprocessing: denoising and contrast enhancement (CLAHE)
      detection/
        detector.py         - YOLOv8-based license plate localisation
      correction/
        perspective.py      - Perspective transformation to correct geometrically tilted plates
      recognition/
        ocr_engine.py       - OCR character extraction using fast-plate-ocr
    services/
      parking_service.py    - Business logic for entry/exit operations and duration/fee calculation
      record_service.py     - Business logic for querying and filtering parking records
    weights/
      best.pt               - Trained YOLOv8 model weights for license plate detection

frontend/                   - Frontend web application (Vue 3 + Vite)
  package.json              - Node.js dependency list
  vite.config.js            - Vite build configuration; API proxy to backend port 8000
  index.html                - HTML entry point
  src/
    main.js                 - Vue application initialisation and plugin registration
    router/
      index.js              - Client-side routing with authentication guards
    api/
      auth.js               - Axios wrapper for authentication API calls
      parking.js            - Axios wrapper for parking entry/exit API calls
      records.js            - Axios wrapper for records API calls
    views/
      Login.vue             - Administrator login interface
      Layout.vue            - Main dashboard layout with sidebar navigation
      Recognition/
        Index.vue           - Standalone plate recognition test tool
      Parking/
        Entry.vue           - Vehicle entry registration (image upload / camera simulation)
        Exit.vue            - Vehicle exit registration and fee display
        PriceManagement.vue - Hourly rate configuration interface
      Records/
        List.vue            - Searchable data table of historical parking records
    components/
      ImageUpload.vue       - Reusable image upload component

Yolo/                       - YOLOv8 model training configuration and results
  args.yaml                 - Training hyperparameters (see Section 9 for details)
  results.csv               - Per-epoch training metrics log
  results.png               - Training curves (loss, mAP, precision, recall)
  confusion_matrix.png      - Detection confusion matrix
  weights/
    best.pt                 - Best checkpoint (highest mAP during training)
    last.pt                 - Final epoch checkpoint


================================================================
SECTION 2: SOFTWARE DEPENDENCIES
================================================================

---- Backend (Python) ----
Python version:       3.10 or 3.11  (3.12+ NOT supported due to package compatibility)

Key Python packages (full list in backend/requirements.txt):
  fastapi               - Web framework for building the REST API
  uvicorn               - ASGI server for running FastAPI
  sqlalchemy            - ORM for SQLite database interaction
  pydantic-settings     - Configuration management
  python-jose[cryptography] - JWT token creation and validation
  passlib[bcrypt]       - Password hashing
  python-multipart      - Multipart file upload support
  ultralytics           - YOLOv8 model inference (license plate detection)
  fast-plate-ocr        - Optimised OCR engine for multi-region license plate recognition
  opencv-python         - Image processing (enhancement, perspective correction)
  Pillow                - Image I/O support
  numpy                 - Numerical operations

---- Frontend (Node.js) ----
Node.js version:      16.x ~ 18.x  (19+ may cause compatibility issues)
npm version:          8.x or above

Key Node.js packages (full list in frontend/package.json):
  vue (3.x)             - Progressive JavaScript UI framework
  vue-router (4.x)      - Client-side routing
  vite                  - Frontend build tool and development server
  axios                 - HTTP client for backend API requests
  element-plus          - UI component library (forms, tables, dialogs)

---- Browser ----
  Google Chrome (latest) or Mozilla Firefox (latest)
  JavaScript must be enabled.


================================================================
SECTION 3: HARDWARE REQUIREMENTS
================================================================

Minimum recommended hardware:

  CPU:        Dual-core 2.0 GHz or above (Intel Core i5 / AMD Ryzen 5 recommended)
  RAM:        4 GB minimum; 8 GB recommended
  Disk:       At least 3 GB free space
              (approx. 1.5 GB for Python packages, 300 MB for Node modules,
               200 MB for model weights, remainder for database and logs)
  Display:    1280 x 720 resolution or above

GPU is NOT required by default. The system runs on CPU out of the box. GPU acceleration can be enabled by setting DEVICE=cuda in backend/app/core/config.py if a compatible GPU is available.

Network:     Local loopback only. No internet connection required after installation.
             Internet is required during the initial dependency installation step.

Ports:       Port 8000 (backend) and Port 3001 (frontend) must be available and
             not occupied by other processes.


================================================================
SECTION 4: COMPILATION INSTRUCTIONS
================================================================

Python (Backend):
  Python is an interpreted language and does NOT require compilation.
  No build step is needed before running the backend server.

Frontend (Vue 3 + Vite):
  For DEVELOPMENT use, no compilation is required. The Vite development server
  compiles and serves assets on the fly (see Section 5).

  For PRODUCTION deployment (optional), run the following to compile static assets:
    cd frontend
    npm run build
  The compiled output will be placed in frontend/dist/.
  This step is NOT required for local demonstration.


================================================================
SECTION 5: RUNNING INSTRUCTIONS
================================================================

---- Option 1: One-Click Startup (Recommended for Windows) ----

1. Ensure Python 3.10/3.11 and Node.js 16-18 are installed and added to PATH.
2. Double-click the file: first_start.bat
   The script will automatically:
     a) Install all Python backend dependencies (pip install -r requirements.txt)
     b) Install all frontend Node.js dependencies (npm install)
     c) Start the FastAPI backend server on port 8000
     d) Start the Vue 3 frontend development server on port 3001

3. Open a browser and navigate to:
     Frontend (Main Interface):  http://localhost:3001
     Backend API:                http://localhost:8000
     API Documentation (Swagger): http://localhost:8000/docs

4. Log in with the default administrator credentials:
     Username: admin
     Password: 123456

---- Option 2: Manual Startup ----

Step 1 - Start the Backend:
  Open a terminal (Command Prompt or PowerShell) and run:

    cd C:\<path-to-project>\backend
    pip install -r requirements.txt
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  The backend server will start. Keep this terminal window open.

Step 2 - Start the Frontend:
  Open a SECOND terminal and run:

    cd C:\<path-to-project>\frontend
    npm install
    npm run dev

  The frontend server will start on port 3001. Keep this terminal window open.

Step 3 - Access the System:
  Open a browser and navigate to: http://localhost:3001

---- Stopping the System ----
  Press Ctrl+C in each terminal window to stop the respective server.


================================================================
SECTION 6: FIRST-TIME SETUP NOTES
================================================================

- The SQLite database file (parking.db) is created automatically in the backend
  directory on first run. No manual database setup is required.
- If port 8000 or 3001 is already in use, terminate the conflicting process before
  starting the system.
- On slower machines, please allow 20-30 seconds for the backend to initialise,
  as the YOLOv8 and OCR models are loaded into memory on startup.


================================================================
SECTION 7: SYSTEM USAGE (BRIEF)
================================================================

1. Open http://localhost:3001 in a browser.
2. Log in with administrator credentials.
3. Navigate to "Vehicle Entry": upload a vehicle image to register entry.
   The system will automatically detect and recognise the license plate.
4. Navigate to "Vehicle Exit": upload an exit image. The system will match
   the plate, calculate parking duration, and display the fee.
5. Navigate to "Records": view, search, and export historical parking data.
6. Navigate to "Price Management": adjust the hourly parking rate as needed.
7. Navigate to "Recognition Test": upload any image to test the ALPR pipeline
   without creating a parking record.


================================================================
SECTION 8: ALPR PIPELINE SUMMARY
================================================================

Image Input
  -> Image Enhancement (CLAHE contrast, denoising)
  -> YOLOv8 Detection (locate license plate region)
  -> Perspective Correction (rectify tilted plates)
  -> OCR (fast-plate-ocr character extraction)
  -> Result stored in SQLite database
  -> Displayed on frontend


================================================================
SECTION 9: YOLO MODEL TRAINING INFORMATION
================================================================

Training was performed offline; the trained weights are included in the archive.
Re-training is NOT required to run the system.

Training configuration (from Yolo/args.yaml):
  Task:            Object detection
  Base model:      yolov8s.pt (YOLOv8 small variant, pre-trained on COCO)
  Dataset:         License plate images (multi-region)
  Epochs:          50
  Image size:      640 x 640 pixels
  Optimiser:       SGD (default Ultralytics settings)

Final model performance (from Yolo/results.csv, final epoch):
  mAP@0.5:         approximately 0.90
  Precision:        high (see Yolo/results.png for full curves)
  Recall:           high (see Yolo/results.png for full curves)

The trained weights file used by the system:
  backend/weights/best.pt   (copied from Yolo/weights/best.pt)


================================================================
SECTION 10: TROUBLESHOOTING
================================================================

Problem: "Port already in use" error on startup.
Solution: Check for and terminate any process using port 8000 or 3001.
  Windows: netstat -ano | findstr :8000
           taskkill /PID <PID> /F

Problem: "Module not found" or import errors on backend startup.
Solution: Ensure you are using Python 3.10 or 3.11. Run:
           pip install -r requirements.txt
  inside the backend/ directory with the correct Python interpreter active.

Problem: Frontend shows "Network Error" or cannot connect to backend.
Solution: Ensure the backend server is running on port 8000 before accessing
  the frontend. Check the backend terminal for error messages.

Problem: Recognition returns no result or incorrect result.
Solution: Ensure the uploaded image contains a clearly visible license plate.
  Test with the provided images in the test_images/ directory.


================================================================
END OF README
================================================================
