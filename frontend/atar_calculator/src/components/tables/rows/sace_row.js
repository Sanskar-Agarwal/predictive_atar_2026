// Library Imports
import React, { useEffect, useState } from 'react';

// Package Imports
import {
   SubjectColumn,
   CategoricalMarkColumn, 
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for South Australia 
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @param {Array} options - an array of available categorical mark options
 * @returns {JSX.Element} - the rendered table row 
 */
function SACERow({rowId, subjects, options}) {
    subjects = subjects || []; 
    options = options || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [selectedMark, setSelectedMark] = useState(options[0] || 'E');
    
    useEffect(
        () => { handleDataUpdate(rowId, enteredSubject, selectedMark)}, 
        [rowId, enteredSubject, selectedMark]
    )

    return ( 
        <div className="table-row">
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']}/>
            <CategoricalMarkColumn options={options} setSelectedMark={setSelectedMark} style={columnStyles['mark']} />
        </div>
    );
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100/2}%`;
    const styles = {
        "subjects": {
            width: width,
        },
        "mark": {
            width: width,
            borderRight: "2px solid black"
        }, 
    }
    return styles; 
}

/**
 * update function for updating the row information to RowDataHandler when a change occurred to each of the column
 * @param {number} rowId - id of the current row 
 * @param {string} enteredSubject - subject entered by a user
 * @param {number} enteredMark - mark enterd by a user
 */
function handleDataUpdate(rowId, enteredSubject, enteredMark) {
    const ins = RowDataHandler.getInstance();
    ins.insertData(rowId, enteredSubject, {
        "mark": enteredMark,
    })
}

export default SACERow;