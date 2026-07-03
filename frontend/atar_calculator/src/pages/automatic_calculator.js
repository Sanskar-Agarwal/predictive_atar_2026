// Package Imports
import Template from '../components/template.js';
import TranscriptExtractor from '../components/transcript_extractor.js';

// CSS Imports
import '../styles/automatic_calculator.css';

/**
 * Automatic calculator page: a heading plus the reusable transcript extractor.
 */
function AutomaticCalculator() {
    return (
        <>
            <Template />
            <div className="auto-page-header">
                <h1 className="auto-title">Upload a transcript</h1>
                <p className="auto-subtitle">
                    Upload a PDF and we'll pull out the subjects and marks. Review the table and
                    edit anything that looks off before continuing.
                </p>
            </div>
            <TranscriptExtractor />
        </>
    );
}

export default AutomaticCalculator;
