// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import {
    SubjectColumn,
    YearColumn,
    MixedMarkColumn,
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for Tasmania
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @param {Array} options - an array of available categorical mark options
 * @returns {JSX.Element} - the rendered table row 
 */
function TasYearMixedRow({rowId, subjects, options}) {
    subjects = subjects || []; 
    options = options || [];
    const columnStyles = setupColumnStyles();
    const currentYear = new Date().getFullYear();
    const [enteredYear, setEnteredYear] = useState(currentYear);
    const [enteredSubject, setEnteredSubject] = useState('');
    const [enteredMark, setEnteredMark] = useState('');
    
    useEffect(
        () => { 
            console.log(enteredMark);
            handleDataUpdate(rowId, enteredSubject, enteredYear, enteredMark);
        }, [rowId, enteredSubject, enteredYear, enteredMark]
    )
     
    const inputFormat = { 
        minRange: 0,
        maxRange: 50,
    }
    
    return (
        <div className="table-row">
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']}/>
            <YearColumn enteredYear={enteredYear} setEnteredYear={setEnteredYear} currentYear={currentYear} style={columnStyles['year']} />
            <MixedMarkColumn options={options} setEnteredMark={setEnteredMark} inputFormat={inputFormat} style={columnStyles['score']} />
        </div>
    );
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100/3}%`;
    const styles = {
        "subjects": {
            width: width
        },
        "year": {
            width: width
        },
        "score": {
            width: width,
            borderRight: '2px solid black',
        },
    }
    return styles;
}

/**
 * update function for updating the row information to RowDataHandler when a change occurred to each of the column
 * @param {number} rowId - id of the current row
 * @param {string} enteredSubject - subject entered by a user
 * @param {number} enteredYear - year entered by a user
 * @param {number} enteredMark - mark entered by a user
 */
function handleDataUpdate(rowId, enteredSubject, enteredYear, enteredMark) { 
    const ins = RowDataHandler.getInstance();
    if (enteredMark === '') enteredMark = 0;
    ins.insertData(rowId,  enteredSubject, {
        "year": enteredYear,
        "mark": enteredMark
    })
}

export default TasYearMixedRow;