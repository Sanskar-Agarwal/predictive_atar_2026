// Library Imports
import React, { useState, useEffect, useCallback } from 'react';
import { Document, Page } from 'react-pdf';
import { useDropzone } from 'react-dropzone';
import { pdfjs } from 'react-pdf';

// CSS Imports
import '../styles/pdf_uploaders.css';

// Configurations
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  '../../node_modules/react-pdf/node_modules/pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();

const MIN_SCALE = 0.4;
const MAX_SCALE = 3;
const DEFAULT_SCALE = 1.2;

/**
 * the container that allows the user to upload pdf and displayed them onto the screen
 * @returns {JSX.Element} rendered pdf uploader and displayed
 */
const PdfUploader = () => {
  const [pdfs, setPdfs] = useState([]);
  const [selectedPdfIndex, setSelectedPdfIndex] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [numPages, setNumPages] = useState(null);
  const [scale, setScale] = useState(DEFAULT_SCALE);

  useEffect(() => {
    if (pdfs.length > 0) {
      UpdatePageNumbers(selectedPdfIndex, pdfs, setNumPages);
    }
  }, [pdfs, selectedPdfIndex]);

  return (
    <div className='pdf-uploader-container'>
      <FileDropBox pdfs={pdfs} setPdfs={setPdfs} setSelectedPdfIndex={setSelectedPdfIndex} setCurrentPage={setCurrentPage} />
      { pdfs.length > 0 && (
        <>
          <NavigationContainer currentPage={currentPage}  setCurrentPage={setCurrentPage}
            numPages={numPages} selectedPdfIndex={selectedPdfIndex} setSelectedPdfIndex={setSelectedPdfIndex}
            pdfs={pdfs} />
          <ZoomContainer scale={scale} setScale={setScale} />
          <PdfDisplayContainer pdfs={pdfs} selectedPdfIndex={selectedPdfIndex}
            currentPage={currentPage} scale={scale} />
        </>
      )}
    </div>
  );
};

/**
 * container with zoom in/out/reset controls for the pdf display
 * @param {Object} props - component props
 * @param {number} scale - the current zoom scale applied to the pdf page
 * @param {function} setScale - function to update the zoom scale
 * @returns {JSX.Element} rendered zoom controls
 */
function ZoomContainer({ scale, setScale }) {
  const zoomOut = () => setScale((prev) => Math.max(MIN_SCALE, Math.round((prev - 0.2) * 10) / 10));
  const zoomIn = () => setScale((prev) => Math.min(MAX_SCALE, Math.round((prev + 0.2) * 10) / 10));
  const resetZoom = () => setScale(DEFAULT_SCALE);

  return (
    <div className='zoom-container'>
      <button onClick={zoomOut} disabled={scale <= MIN_SCALE} title="Zoom out">-</button>
      <h3 onClick={resetZoom} title="Reset zoom">{`${Math.round(scale * 100)}%`}</h3>
      <button onClick={zoomIn} disabled={scale >= MAX_SCALE} title="Zoom in">+</button>
    </div>
  );
}

/**
 * container that allows the user to upload pdfs to be displayed on the screen
 * @param {Object} props - component props
 * @param {Array} pdfs - an array of all uploaded pdfs
 * @param {function} setPdfs - function to update the array of pdfs
 * @param {function} setSelectedPdfIndex - function to switch the currently displayed pdf
 * @param {function} setCurrentPage - function to reset the displayed page
 * @returns
 */
function FileDropBox({pdfs, setPdfs, setSelectedPdfIndex, setCurrentPage}) {
  const [rejectedMessage, setRejectedMessage] = useState('');

  const onDrop = (acceptedFiles) => {
    const hasNonPdf = acceptedFiles.some(file => file.type !== 'application/pdf');
    let newFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    newFiles = newFiles.filter(file => !pdfs.some(pdf => pdf.name === file.name));

    setRejectedMessage(hasNonPdf ? 'Only PDF files are supported — other files were skipped.' : '');
    if (newFiles.length > 0) {
      // Without this, a newly dropped file is added to the "Select PDF" list
      // but the viewer keeps showing whatever was already selected — looking
      // exactly like the upload silently did nothing.
      setSelectedPdfIndex(pdfs.length);
      setCurrentPage(1);
    }
    setPdfs([...pdfs, ...newFiles]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: '.pdf',
    onDrop,
  });

  return (
    <div>
      <div className={`file-upload-box${isDragActive ? ' file-upload-box-active' : ''}`} {...getRootProps()}>
        <span className="file-upload-plus">+</span>
        <input {...getInputProps()} />
        <p>Drag &amp; drop a PDF file here, or click to select one</p>
      </div>
      {rejectedMessage && <p className="file-upload-error">{rejectedMessage}</p>}
    </div>
  );
}

/**
 * container that allows the user to navigate between different pdf files and pages
 * @param {Object} props - component props 
 * @param {number} currentPage - the current page of the selected pdf being rendered
 * @param {number} numPages - the number of pages that the pdf has
 * @param {number} selectedPdfIndex - the index of the selected pdf
 * @param {Array} pdfs - an array of all uploaded pdfs
 * @returns {JSX.Element} rendered container
 */
function NavigationContainer({currentPage, setCurrentPage, numPages, selectedPdfIndex, setSelectedPdfIndex, pdfs}) {
  const nextPage = useCallback(() => {
    if (currentPage < numPages) {
      setCurrentPage(currentPage + 1);
    }
  }, [currentPage, numPages, setCurrentPage]); // Dependencies for nextPage
  
  const prevPage = useCallback(() => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  }, [currentPage, setCurrentPage]); // Dependencies for prevPage
  

  const handlePdfSelect = (index) => {
    setSelectedPdfIndex(index);
    setCurrentPage(1);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      // Don't hijack arrow keys while the user is typing/navigating text in a
      // form field (e.g. reading a long subject name in mirror mode) — only
      // page the pdf when focus isn't inside an editable element.
      const target = event.target;
      const isTypingContext = target && (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.tagName === 'SELECT' ||
        target.isContentEditable
      );
      if (isTypingContext) {
        return;
      }

      switch (event.key) {
        case 'ArrowRight':
          nextPage();
          break;
        case 'ArrowLeft':
          prevPage();
          break;
        default:
          break;
      }
    };
  
    window.addEventListener('keydown', handleKeyDown);
  
    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentPage, numPages, nextPage, prevPage]); // Include nextPage and prevPage in dependencies if they're stable or memoized
  
  return (
    <div className='navigation-container'>
      <div className='pdf-selector-container'>
        <label>Select PDF:</label>
        <select className='pdf-selector' value={selectedPdfIndex} onChange={(e) => handlePdfSelect(e.target.value)}>
            {pdfs.map((pdf, index) => (
              <option key={index} value={index}>{pdf.name}</option>
            ))}
          </select>
      </div>
      <div className='page-navigation-container'>
        <button onClick={prevPage} disabled={currentPage === 1}>Previous</button>
        <h3>{` Page ${currentPage} of ${numPages || '-'} `}</h3>
        <button onClick={nextPage} disabled={currentPage === numPages}>Next</button>
      </div>
    </div>
  );
}

/**
 * containter that shows the current selected pdf onto the screen
 * @param {Object} props - component props
 * @param {Array} pdfs - an array of all uploaded pdfs
 * @param {number} selectedPdfIndex - index of the current selected pdf
 * @param {number} currentPage - the page number to be displayed
 * @param {number} scale - the zoom scale to render the page at
 * @returns {JSX.Element} rendered container
 */
function PdfDisplayContainer({pdfs, selectedPdfIndex, currentPage, scale }){
  return (
    <div className='pdf-display-container'>
      <Document file={pdfs[selectedPdfIndex]}>
        <Page pageNumber={currentPage} scale={scale} renderAnnotationLayer={false} renderTextLayer={false}/>
      </Document>
    </div>
  );
}

/**
 * update functions for changing the page of a selected pdf
 * @param {number} selectedPdfIndex - index of the current selected pdf
 * @param {Array} pdfs - an array of all uploaded pdfs
 * @param {number} setNumPages - used to set the page number for the selected pdf
 */
function UpdatePageNumbers(selectedPdfIndex, pdfs, setNumPages) {
  const selectedPdf = pdfs[selectedPdfIndex];
  const reader = new FileReader();
  reader.onload = (event) => {
    const typedArray = new Uint8Array(event.target.result);
    pdfjs.getDocument(typedArray).promise.then(
      pdf => {
        setNumPages(pdf.numPages);
      }
    );
  };
  reader.readAsArrayBuffer(selectedPdf);  
}

export default PdfUploader;