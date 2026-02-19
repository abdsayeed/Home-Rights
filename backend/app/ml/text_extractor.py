"""
Text Extraction Utilities
Extract text from PDF and image files with retry logic and error handling
"""
import pytesseract
from PIL import Image
import PyPDF2
import io
import os
from app.utils.retry_strategies import RetryStrategies
from app.utils.logging_config import get_logger

logger = get_logger('ml.text_extractor')


class TextExtractor:
    """Extract text from various document formats with production-grade error handling"""
    
    @staticmethod
    @RetryStrategies.OCR
    def extract_from_image(image_path):
        """
        Extract text from image using Tesseract OCR with validation and retry logic
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text string
        """
        if not image_path:
            logger.error("Image path is empty")
            return ""
        
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return ""
        
        image = None
        
        try:
            logger.info(f"Starting OCR for image: {image_path}")
            
            # Open image
            image = Image.open(image_path)
            
            # Validate image
            if image.size[0] == 0 or image.size[1] == 0:
                logger.error("Image has zero dimensions")
                return ""
            
            # Preprocess image for better OCR
            image = TextExtractor._preprocess_image(image)
            
            # Perform OCR
            text = pytesseract.image_to_string(image, lang='eng')
            
            logger.info(
                f"OCR completed successfully",
                extra={
                    'image_path': image_path,
                    'text_length': len(text)
                }
            )
            
            return text.strip()
            
        except IOError as e:
            logger.error(f"Error opening image file: {e}", exc_info=True)
            return ""
        except pytesseract.TesseractNotFoundError:
            logger.error("Tesseract OCR not installed or not in PATH")
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}", exc_info=True)
            raise  # Re-raise for retry mechanism
        finally:
            # Close image if opened
            if image:
                try:
                    image.close()
                except Exception:
                    pass
    
    @staticmethod
    @RetryStrategies.OCR
    def extract_from_pdf(pdf_path):
        """
        Extract text from PDF file with proper resource management and retry logic
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text string
        """
        if not pdf_path:
            logger.error("PDF path is empty")
            return ""
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return ""
        
        text = ""
        file_handle = None
        
        try:
            logger.info(f"Starting PDF text extraction: {pdf_path}")
            
            file_handle = open(pdf_path, 'rb')
            reader = PyPDF2.PdfReader(file_handle)
            
            # Check if PDF has pages
            if not reader.pages:
                logger.warning("PDF has no pages")
                return ""
            
            page_count = len(reader.pages)
            logger.info(f"PDF has {page_count} pages")
            
            # Extract text from all pages
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(
                        f"Error extracting text from page {page_num + 1}: {e}"
                    )
                    continue
            
            # If PDF is scanned (no text extracted), try OCR
            if len(text.strip()) < 100:
                logger.info("PDF appears to be scanned, attempting OCR...")
                # Close file handle before OCR
                if file_handle:
                    file_handle.close()
                    file_handle = None
                text = TextExtractor._ocr_pdf(pdf_path)
            
            logger.info(
                "PDF extraction completed",
                extra={
                    'pdf_path': pdf_path,
                    'text_length': len(text),
                    'page_count': page_count
                }
            )
            
            return text.strip()
            
        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"PDF read error (corrupted or encrypted): {e}", exc_info=True)
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
            raise  # Re-raise for retry mechanism
        finally:
            # Ensure file handle is always closed
            if file_handle:
                try:
                    file_handle.close()
                except Exception as e:
                    logger.error(f"Error closing file handle: {e}")
    
    @staticmethod
    def _preprocess_image(image):
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        try:
            import cv2
            import numpy as np
            
            # Convert PIL to numpy array
            img = np.array(image)
            
            # Convert to grayscale if color
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Apply thresholding to get binary image
            thresh = cv2.threshold(
                gray, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(thresh)
            
            # Convert back to PIL Image
            return Image.fromarray(denoised)
        except ImportError:
            # If OpenCV not available, return original
            print("OpenCV not available, skipping image preprocessing")
            return image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image
    
    @staticmethod
    def _ocr_pdf(pdf_path):
        """
        Perform OCR on scanned PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text string
        """
        try:
            import pdf2image
            
            # Convert PDF pages to images
            images = pdf2image.convert_from_path(pdf_path)
            
            text = ""
            for i, image in enumerate(images):
                print(f"OCR processing page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image, lang='eng')
                text += page_text + "\n"
            
            return text.strip()
        except ImportError:
            print("pdf2image not available, cannot OCR scanned PDF")
            return ""
        except Exception as e:
            print(f"Error performing OCR on PDF: {e}")
            return ""
    
    @staticmethod
    def extract_from_bytes(file_bytes, file_type):
        """
        Extract text from file bytes
        
        Args:
            file_bytes: File content as bytes
            file_type: File extension (pdf, jpg, png, etc.)
            
        Returns:
            Extracted text string
        """
        try:
            if file_type.lower() in ['jpg', 'jpeg', 'png']:
                # Convert bytes to image
                image = Image.open(io.BytesIO(file_bytes))
                image = TextExtractor._preprocess_image(image)
                return pytesseract.image_to_string(image, lang='eng').strip()
            
            elif file_type.lower() == 'pdf':
                # Extract from PDF bytes
                reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
            
            else:
                return ""
        except Exception as e:
            print(f"Error extracting text from bytes: {e}")
            return ""
