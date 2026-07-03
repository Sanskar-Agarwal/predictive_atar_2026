// Package Imports
import PdfUploader from "../components/pdf_uploader";
import Template from "../components/template";

// CSS Imports
import '../styles/mirror_mode.css';
import ManualCalculator from "./manual_calculator";

function MirrorMode() {
    return (
        <>
            <Template />
            <div className='mirror-mode-container'>
                <LeftContainer />
                <RightContainer />
            </div>
        </>
    );
}

function LeftContainer() {
    return ( 
        <div className='mirror-mode-left-container'>
            <ManualCalculator hasTemplate={false}/>
        </div>
    );
}

/**
 * Right side of mirror mode: just displays the uploaded transcript PDF (with
 * zoom/paging) for the user to reference while filling in the form on the
 * left — no automated extraction runs here, unlike the Automatic page.
 */
function RightContainer() {
    return (
        <div className='mirror-mode-right-container'>
            <PdfUploader />
        </div>
    );
}

export default MirrorMode;