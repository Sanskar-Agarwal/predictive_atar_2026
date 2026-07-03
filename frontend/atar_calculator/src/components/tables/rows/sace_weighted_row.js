// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import {
    SubjectColumn,
    AssessmentColumn,
    WeightingColumn,
    CategoricalMarkColumn
} from "../columns/table_columns.js";

import {
    updateSubjectWeighting,
} from "../columns/table_column_updaters.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for South Australia with weighting 
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @param {Array} options - an array of available categorical mark options
 * @returns {JSX.Element} - the rendered table row 
 */
function SACEWeightedRow({rowId, subjects, options}) {
    // Variables Assignments 
    subjects = subjects || []; 
    options = options || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [selectedMark, setSelectedMark] = useState(options[0] || "E");
    const [enteredWeighting, setEnteredWeighting] = useState(0);
    const [enteredAssessment, setEnteredAssessment] = useState('');

    useEffect(
        // Update level options when the entered subject changes
        () =>  {
            const subjectWeighting = {};
            updateSubjectWeighting(enteredSubject, subjectWeighting, setEnteredWeighting);
        }, [enteredSubject]  
    );

    useEffect(
        () => {
            handleDataUpdate(rowId, enteredSubject, enteredAssessment ,selectedMark, enteredWeighting);
        }, [rowId, enteredSubject, enteredAssessment, selectedMark, enteredWeighting]
    )

    return (
        <div className="table-row">
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']}/>
            <AssessmentColumn setEnteredAssessment={setEnteredAssessment} style={columnStyles['subjectLevels']} />
            <CategoricalMarkColumn options={options} setSelectedMark={setSelectedMark} style={columnStyles['mark']}/>
            <WeightingColumn enteredWeighting={enteredWeighting} setEnteredWeighting={setEnteredWeighting} style={columnStyles['weighting']} />
        </div>
    );
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100/4}%`;
    const styles = {
        "subjects": {
            width: width,
        },
        "subjectLevels": {
            width: width,
        }, 
        "mark": {
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
 * @param {number} enteredMark - mark enterd by a user
 * @param {number} enteredWeighting - weighting entered by a user
 */
function handleDataUpdate(rowId, enteredSubject, enteredAssessment, enteredMark, enteredWeighting) {
    const ins = RowDataHandler.getInstance();
    ins.insertData(rowId, enteredSubject, { [enteredAssessment]:
        {
            "mark": enteredMark,
            "weighting": enteredWeighting
        }
    }
    );
}

export default SACEWeightedRow;