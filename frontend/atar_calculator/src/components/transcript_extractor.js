// Library Imports
import React, { useState } from 'react';
import RequestHandler from './data_handlers/request_handler.js';
import { AUTOMATIC_EXTRACTION_ENABLED } from '../constants/constants.js';

// CSS Imports
import '../styles/automatic_calculator.css';

// The scales the extractor uses; shown as an editable dropdown per row.
const SCALE_OPTIONS = [
    'numerical_percent',
    'numerical_out_of_50',
    'band_A_E',
    'other',
];

/**
 * Reusable transcript-extraction panel: upload a PDF, the backend extracts the
 * subjects/marks, and the user can review and edit them. Used by both the
 * automatic calculator page and mirror mode.
 */
function TranscriptExtractor() {
    const [status, setStatus] = useState('idle');   // idle | loading | done | error
    const [error, setError] = useState(null);
    const [filename, setFilename] = useState(null);
    const [showApiUnavailable, setShowApiUnavailable] = useState(false);

    // Editable extraction result
    const [region, setRegion] = useState('');
    const [gradeFormat, setGradeFormat] = useState('');
    const [notes, setNotes] = useState('');
    const [usage, setUsage] = useState(null);
    const [subjects, setSubjects] = useState([]);   // [{subject, mark, scale, source_label}]

    const handleFile = async (file) => {
        setFilename(file.name);

        // Automatic extraction needs a configured ANTHROPIC_API_KEY on the
        // backend; until one is added, skip the call entirely instead of
        // hitting an endpoint that's guaranteed to fail.
        if (!AUTOMATIC_EXTRACTION_ENABLED) {
            setShowApiUnavailable(true);
            return;
        }

        setStatus('loading');
        setError(null);
        try {
            const data = await RequestHandler.getInstance().uploadTranscript(file);
            setRegion(data.region || '');
            setGradeFormat(data.grade_format || '');
            setNotes(data.notes || '');
            setUsage(data.usage || null);
            setSubjects((data.subjects || []).map((s) => ({ ...s })));
            setStatus('done');
        } catch (err) {
            setError(err.message || String(err));
            setStatus('error');
        }
    };

    const handleChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            handleFile(file);
        }
        event.target.value = ''; // allow re-selecting the same file
    };

    const triggerPick = () => document.getElementById('fileUpload').click();

    // Row editing
    const updateRow = (i, field, value) =>
        setSubjects((prev) => prev.map((r, idx) => (idx === i ? { ...r, [field]: value } : r)));
    const removeRow = (i) =>
        setSubjects((prev) => prev.filter((_, idx) => idx !== i));
    const addRow = () =>
        setSubjects((prev) => [...prev, { subject: '', mark: '', scale: 'other', source_label: '' }]);

    return (
        <div className="auto-container">
            {showApiUnavailable && (
                <div className="api-unavailable-overlay" onClick={() => setShowApiUnavailable(false)}>
                    <div className="api-unavailable-modal" onClick={(e) => e.stopPropagation()}>
                        <h3>Automatic extraction unavailable</h3>
                        <p>No API is currently available for automatic transcript extraction. Please use the Manual or Mirror Mode calculator instead.</p>
                        <button className="api-unavailable-close" onClick={() => setShowApiUnavailable(false)}>Close</button>
                    </div>
                </div>
            )}
            <input
                type="file"
                accept=".pdf"
                onChange={handleChange}
                style={{ display: 'none' }}
                id="fileUpload"
            />
            <div className="auto-dropzone" onClick={triggerPick}>
                <span className="auto-dropzone-plus">+</span>
                <span>{filename ? `Replace “${filename}”` : 'Click to select a transcript PDF'}</span>
            </div>

            {status === 'loading' && (
                <p className="auto-status">
                    Extracting marks from <b>{filename}</b> … this takes a few seconds.
                </p>
            )}
            {status === 'error' && (
                <p className="auto-status auto-error">Could not extract {filename}: {error}</p>
            )}

            {status === 'done' && (
                <div className="auto-results">
                    <div className="auto-meta-row">
                        <label>
                            Region
                            <input
                                className="auto-meta-input"
                                value={region}
                                onChange={(e) => setRegion(e.target.value)}
                            />
                        </label>
                        <label>
                            Format
                            <input
                                className="auto-meta-input"
                                value={gradeFormat}
                                onChange={(e) => setGradeFormat(e.target.value)}
                            />
                        </label>
                    </div>

                    {notes && <p className="auto-note">{notes}</p>}
                    {subjects.length === 0 && (
                        <p className="auto-error">
                            No usable final marks were found in this transcript — you can add rows manually below.
                        </p>
                    )}

                    <div className="auto-table-wrap">
                        <table className="auto-table">
                            <thead>
                                <tr>
                                    <th className="col-subject">Subject</th>
                                    <th className="col-mark">Mark / Code</th>
                                    <th className="col-scale">Scale</th>
                                    <th className="col-source">Source</th>
                                    <th className="col-delete" aria-label="delete" />
                                </tr>
                            </thead>
                            <tbody>
                                {subjects.map((s, i) => (
                                    <tr key={i}>
                                        <td>
                                            <input
                                                value={s.subject}
                                                onChange={(e) => updateRow(i, 'subject', e.target.value)}
                                            />
                                        </td>
                                        <td>
                                            <input
                                                className="mark-input"
                                                value={s.mark}
                                                onChange={(e) => updateRow(i, 'mark', e.target.value)}
                                            />
                                        </td>
                                        <td>
                                            <select
                                                value={s.scale}
                                                onChange={(e) => updateRow(i, 'scale', e.target.value)}
                                            >
                                                {SCALE_OPTIONS.map((o) => (
                                                    <option key={o} value={o}>{o}</option>
                                                ))}
                                            </select>
                                        </td>
                                        <td>
                                            <input
                                                className="source-input"
                                                value={s.source_label}
                                                onChange={(e) => updateRow(i, 'source_label', e.target.value)}
                                            />
                                        </td>
                                        <td className="cell-delete">
                                            <button
                                                className="row-delete"
                                                onClick={() => removeRow(i)}
                                                title="Delete this subject"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td className="add-row-cell" colSpan={5}>
                                        <button
                                            className="add-button-circle"
                                            onClick={addRow}
                                            title="Add a subject"
                                        >
                                            +
                                        </button>
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>

                    {usage && (
                        <p className="auto-usage">
                            {usage.model} · {usage.pages} pages · {usage.input_tokens} in / {usage.output_tokens} out tokens
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default TranscriptExtractor;
