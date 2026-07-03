// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import {
    SubjectColumn,
    MaxMarkColumn,
    NumericalMarkColumn
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for purely numerical row
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @returns {JSX.Element} - the rendered table row 
 */
export function NumericalRow({rowId, subjects}) {
    subjects = subjects || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [enteredMark, setEnteredMark] = useState(0);
    const [enteredMaxMark, setEnteredMaxMark] = useState(100);

    useEffect(() => {
        handleDataUpdate(rowId, enteredSubject, enteredMark, enteredMaxMark);
    }, [rowId, enteredSubject, enteredMark, enteredMaxMark]);
    
    const inputFormat = { 
        maxRange: enteredMaxMark,
    }
    return (
        <div className="table-row">
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']}/>
            <NumericalMarkColumn enteredMark={enteredMark} setEnteredMark={setEnteredMark} inputFormat={inputFormat} style={columnStyles['mark']} />
            <MaxMarkColumn enteredMaxMark={enteredMaxMark} enteredMark={enteredMark} setEnteredMark={setEnteredMark} setEnteredMaxMark={setEnteredMaxMark} style={columnStyles["maxMark"]} />
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
            width: width,
        },
        "mark": {
            width: width,
        }, 
        "maxMark": {
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
 * @param {number} enteredMark - mark entered by a user
 * @param {number} enteredMaxMark - maximum mark entered by a user
 */
function handleDataUpdate(rowId, enteredSubject, enteredMark, enteredMaxMark) {
    const ins = RowDataHandler.getInstance();
    ins.insertData(rowId, enteredSubject, {
        'mark': enteredMark, 
        'max_mark': enteredMaxMark
    });
} 

export default NumericalRow;
