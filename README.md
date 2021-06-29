# Image Processing

![python]
![pyqt]
![opencv]
![numpy]
![windows]
[![license]][license-url]

This is a python raster graphics editor.<br>
General-purpose of the project is to manipulate and edit images.<br>
Additionally, you can [download](#download) a desktop application for Windows.

![demo-hist]
![demo-profile]
![demo-norm]

---

## Table of content

- [Features](#features)
- [Installation](#installation)
- [Build Process](#build-process)
- [Download](#download)
- [Documentation](#documentation)
- [License](#license)

---

## Features

* Open/Save images in common extensions
* Type changing
* Rename/Duplicate
* Zoom in/out
* Histogram
    - Graphical
    - Table representation
* Profile Line
* Object Features
* Histogram Operations
    - Normalization
    - Equalization
* Point Operations
    - Negation
    - Posterize
    - Image Calculator
* Local Operations
    - Smooth
    - Sharpen
    - Convolve
    - Gray Morphology
    - Edge Detection
* Segmentation  
    - Threshold
    - Watershed
* SVM Classification among rice, beans, lentils
* Images stitching (panorama)
* Windows platform-oriented
* Shortcuts

---

## Installation

Clone the project from GitHub, then you'll need [Git](https://git-scm.com/) 
installed on your computer:

```
# Clone this repository
$ git clone https://github.com/vmariiechko/python-image-processing
```

---

## Build Process

To run this application, you'll need [Python 3.6+](https://www.python.org/) installed on your computer.<br>
In your [working environment][venv-url] from the command line:

```
# Go into the repository
$ cd python-image-processing

# Install dependencies
$ pip3 install -r requirements.txt
```

Once you've installed all the dependencies, use the custom 'pythonpath.bat' 
file to run the application from the terminal:

```
# Navigate to src folder
$ cd src

# Run app
$ pythonpath.bat .. main.py
```

That's it! After all the actions, the app's main window must show up.

---

## Download

Get the executable desktop version for Windows from [here][download-url].

There are available images in the 'Test Images' folder inside the root app folder.

---

## Documentation

For technical documentation, see [readthedocs.io][readthedocs-url]

For user documentation in Polish, see [pdf file][pdf-docs-url].

---

## License

>You can check out the full license [here][license-url].

This project is licensed under the terms of the **MIT** license.

---

> Gmail [vmariiechko@gmail.com](mailto:vmariiechko@gmail.com) &nbsp;&middot;&nbsp;
> GitHub [@vmariiechko](https://github.com/vmariiechko) &nbsp;&middot;&nbsp;
> LinkedIn [@mariiechko](https://www.linkedin.com/in/mariiechko/)

<!-- Markdown links and images -->
[python]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[pyqt]: https://img.shields.io/badge/pyqt5-%2341CD52.svg?&style=for-the-badge&logo=qt&logoColor=white
[opencv]: https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white
[numpy]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white
[windows]: https://img.shields.io/badge/windows-0078D6?logo=windows&logoColor=white&style=for-the-badge
[license]: https://img.shields.io/badge/license-MIT-%2341CD52.svg?&style=for-the-badge

[license-url]: https://github.com/vmariiechko/python-image-processing/blob/main/LICENSE.txt
[venv-url]: https://docs.python.org/3/tutorial/venv.html
[readthedocs-url]: https://python-image-processing.readthedocs.io/en/latest/
[pdf-docs-url]: https://github.com/vmariiechko/python-image-processing/blob/main/docs/docs-pl.pdf
[download-url]: https://github.com/vmariiechko/python-image-processing/releases/tag/v1.0.0

[demo-hist]: https://imgur.com/P6r42jD.png
[demo-profile]: https://imgur.com/wWMA5Q9.png
[demo-norm]: https://imgur.com/ak3KJxw.png

