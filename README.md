# FIXUS-APP

## Overview
FIXUS-APP is a Flask-based web application designed for the analysis of X-ray images, particularly focusing on foot and ankle views. Utilizing advanced machine learning models, the app provides insightful heatmaps on X-ray images, highlighting key areas of interest and aiding in medical diagnostics.

## Features
- **Multiple X-ray Views**: Supports different views (AP, lateral, oblique) for both foot and ankle X-rays.
- **Heatmap Generation**: Uses GradCAM technology to generate heatmaps, offering visual insights into the areas of interest in the X-ray images.
- **User-Friendly Interface**: Simple and intuitive UI for easy uploading and analyzing of X-ray images.

## Installation

To set up the FIXUS-APP on your local machine, follow these steps:

1. **Clone the Repository**
   ```
   git clone https://github.com/AMustafa4983/FIXUS-APP.git
   cd FIXUS-APP
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```
   python app.py
   ```

## Usage

1. **Start the Application**
   - Run `python app.py` and navigate to `http://localhost:5000` in your web browser.

2. **Upload X-ray Images**
   - Select the type of X-ray (foot or ankle) and upload the images in the respective views (AP, lateral, oblique).

3. **View Results**
   - After processing, the application will display the original X-ray images along with their corresponding heatmaps.

## Contributing

Contributions to FIXUS-APP are welcome! If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
