// Library Imports
import React, { useEffect, useState } from 'react';

// Package Imports
import {
    SubjectColumn,
    NumericalMarkColumn
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for Multiple categorical grade type
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @returns {JSX.Element} - the rendered table row 
 */
function MultipleCategoricalGradeRow({rowId, subjects}) {
    subjects = subjects || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [outstandingMark, setOutstandingMark] = useState(0);
    const [highMark, setHighMark] = useState(0);
    const [soundMark, setSoundMark] = useState(0);
    const [basicMark, setBasicMark] = useState(0);
    const [limitedMark, setLimitedMark] = useState(0);
    
    useEffect(() => {
        handleDataUpdate(
            rowId, enteredSubject, 
            outstandingMark, highMark, soundMark, basicMark, limitedMark
        );
    }, [
        rowId,
        enteredSubject,
        outstandingMark, 
        highMark, 
        soundMark, 
        basicMark,
        limitedMark
    ]);
    
    const inputFormat = {
        step: 1,
        maxRange: 20,
        minRange: 0,
    }
    
    return ( 
        <div className='table-row'> 
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']} />
            <NumericalMarkColumn enteredMark={outstandingMark} inputFormat={inputFormat} setEnteredMark={setOutstandingMark} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={highMark} inputFormat={inputFormat} setEnteredMark={setHighMark} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={soundMark} inputFormat={inputFormat} setEnteredMark={setSoundMark} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={basicMark} inputFormat={inputFormat} setEnteredMark={setBasicMark} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={limitedMark} inputFormat={inputFormat} setEnteredMark={setLimitedMark} style={columnStyles['mark_end']} />
        </div>
    )
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100/6}%`;
    const styles = {
        'subjects': {
            width: width
        },
        'mark': {
            width: width,
        },
        'mark_end': {
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
 * @param {number} outstandingMark - the number of time the student has achieved outstanding mark
 * @param {number} highMark - the number of time the student has achieved high mark
 * @param {number} soundMark - the number of time the student has achieved sound mark
 * @param {number} basicMark - the number of time the student has achieved basic mark
 * @param {number} limitedMark - the number of time the student has achieved limited mark
 */
function handleDataUpdate(rowId, enteredSubject, outstandingMark, highMark, soundMark, basicMark, limitedMark) {
    const ins = RowDataHandler.getInstance(); 
    ins.insertData(rowId, enteredSubject, {
        "marks": {
            "outstanding": outstandingMark,
            "high": highMark,
            "sound": soundMark, 
            "basic": basicMark, 
            "limited": limitedMark
        }
    });
}

export default MultipleCategoricalGradeRow;
