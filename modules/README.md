
# Exercise: OCR system for object tracking integrated with PLC Siemens

## - Implement an Optical Character Recognition (OCR) system with a Raspberry pi

### 1. How-To

This tutorial aims to explain how to solve some issues you might encounter while installing OpenCV (among other python modules). Instructions for downloading and installing OS images can be found in this [link](https://www.raspberrypi.com/documentation/computers/getting-started.html). This section includes some simple guides to setting up the software on your Raspberry Pi. We recommend that beginners start by downloading and installing NOOBS.
From my experience, I would suggest to install ubuntu mate for raspberry pi 2/3 while for 3 B+ models I would recommend to install Raspbian since the latest model has a 1.4GHz 64-bit quad-core processor instead of a 32 bit processor, as the previous models . If you are going to use snap7 library do not use the 3B+ model since it has only been tested for models with ARMv6 and ARMv7 architecture microprocessors.
During the implementation of a simple OCR system that was meant to send a digit through an OPC server while interacting with a PLC unit , I faced however, some challenges when installing some python modules that were required for the job. Those issues were solved by installing the following libraries:

- libblas-dev
- liblapack-dev
- libxml2
- libxslt1-dev
- zlib1g-dev

To install it just open the command line and run the following:
>`$ sudo apt-get install <library_name>`

Do not forget to update the repository:
> `$ sudo apt-get update`

### 2. A careful look to BLAS and LAPACK libraries

LAPACK stands for Linear Algebra PACKage and is a library of Fortran 77 subroutines for solving the most commonly occurring problems in numerical algebra. It has been designed to be efficient on a wide range of modern high-performance computers. The efficiency of LAPACK software depends on efficient implementations of the BLAS being provided by computer vendors (or others) for their machines. Common applications making use of these libraries are programs like NumPy, SAGE, R, among others. Numpy is one of the most important python modules and is one of OpenCV dependencies. For some unknown reason, both BLAS and LAPACK packages are not automatically installed with the OS, hence it is mandatory that you manually install it.

### 3. XML2 Library

The libxml2 library is the XML (eXtensive Markup Language) C parser and toolkit developed for the Gnome project. It is a world wide web consortium standard for the exchange of structured data in text form. XML itself is a metalanguage to design markup languages, i.e. text language where semantic and structure are added to the content using extra "markup" information enclosed between angle brackets. HTML is the most well-known markup language. Though the library is written in C a variety of language bindings make it available in other environments.

### 4. XLST Library
This package is based on libxml2 and is the XSLT C library (also developed for the GNOME project. XSLT is the acronym for eXtensible Stylesheet Language Transformations and is a declarative language that allows you to translate your XML into arbitrary text output using a stylesheet. libxslt provides the functions to perform the transformation for XML.


### 5. ZLib Library

zlib is a library implementing the deflate compression method found in gzip and PKZIP. This package includes the development support files.

### 6. OpenCV Installation

To install opencv:
> `$ sudo apt-get update` \
 `$ sudo apt-get install libopencv-dev python-opencv`\
 `$ sudo apt-get install libv4l-dev v4l-utils`


You might need to install the Video4Linux library (V4L) in order to be able to connect to a wide range of cameras.

### 7. Available OCR Libraries: TextExtract, PyTesseract, PyOCR

Any of the afore mentioned packages can be used to recognize digits with Python from images in PDF files. We find three python packages that are just wrappers for Tesseract. This means we must install the tesseract-ocr library. 
> `$ sudo apt-get install tesseract-ocr`

For the OCR project, the pytesseract package was used. It has a good library for recognition, but nothing special. Moreover, it was observed that the recognition was very sensitive to image rotation along other visible features in the image that made impossible to “read” the digit. Thus, image processing methods were applied in order to properly recognize the characters (the digit had to be horizontally aligned to be “readable”). That is why I would recommend in the future to use Pyocr. This package has a lot of functions such as to switch data we want to recognize and have orientation detection.


