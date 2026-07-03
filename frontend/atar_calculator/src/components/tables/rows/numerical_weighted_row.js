// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import {
    SubjectColumn,
    AssessmentColumn,
    NumericalMarkColumn,
    MaxMarkColumn,
    WeightingColumn
} from "../columns/table_columns.js";

import { updateSubjectWeighting } from "../columns/table_column_updaters.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for ACT
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available categorical mark options
 * @returns {JSX.Element} - the rendered table row 
 */
function NumericalWeightedRow({rowId, subjects }) {
    // Variables Assignments 
    subjects = subjects || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [enteredMark, setEnteredMark] = useState(0);
    const [enteredMaxMark, setEnteredMaxMark] = useState(100);
    const [enteredWeighting, setEnteredWeighting] = useState(0);
    const [enteredAssessment, setEnteredAssessment] = useState('');
    
    useEffect(
        // Update level options when the entered subject changes
        () => {
            const subjectWeighting = {};
            updateSubjectWeighting(enteredSubject, subjectWeighting, setEnteredWeighting);
        }, [enteredSubject]
    );
    
    useEffect(
        () => {
            handleDataUpdate(rowId, enteredSubject, enteredAssessment, enteredMark, enteredMaxMark, enteredWeighting);
        }, [rowId, enteredSubject, enteredAssessment, enteredMark, enteredMaxMark, enteredWeighting]
    )
    
    const inputFormat = {
        maxRange: enteredMaxMark,
    }

    return (
        <div className="table-row">
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']} />
            <AssessmentColumn setEnteredAssessment={setEnteredAssessment} style={columnStyles['assessment']} />
            <NumericalMarkColumn enteredMark={enteredMark} inputFormat={inputFormat} setEnteredMark={setEnteredMark} style={columnStyles['mark']} />
            <MaxMarkColumn enteredMaxMark={enteredMaxMark} setEnteredMark={setEnteredMark} enteredMark={enteredMark} setEnteredMaxMark={setEnteredMaxMark} style={columnStyles["maxMark"]} />
            <WeightingColumn enteredWeighting={enteredWeighting} setEnteredWeighting={setEnteredWeighting} style={columnStyles['weighting']} />
        </div>
    );
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100 / 5}%`;
    const styles = {
        "subjects": {
            width: width,
        },
        "assessment": {
            width: width,
        },
        "mark": {
            width: width,
            borderColor: 'black',
            color: 'black',
        },
        "maxMark": {
            width: width,
        },
        "weighting": {
            width: width,
            borderRight: '2px solid black',
        }
    }
    return styles;
}

/**
 * update function for updating the row information to RowDataHandler when a change occurred to each of the column
 * @param {number} rowId - id of the current row
 * @param {string} enteredSubject - subject entered by a user
 * @param {string} enteredAssessment - assessment entered by a user
 * @param {number} enteredMark - mark entered by a user
 * @param {number} enteredMaxMark - maximum mark entered by a user
 * @param {number} enteredWeighting - weighting entered by a user
 */

function handleDataUpdate(rowId, enteredSubject, enteredAssessment, enteredMark, enteredMaxMark, enteredWeighting) {
    const ins = RowDataHandler.getInstance();
    ins.insertData(rowId, enteredSubject, { [enteredAssessment]:
        {
            "mark": enteredMark,
            "max_mark": enteredMaxMark,
            "weighting": enteredWeighting
        }
    });
}

export default NumericalWeightedRow;
