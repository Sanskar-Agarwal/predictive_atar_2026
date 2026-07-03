// Library Imports
import React, { useEffect, useState } from 'react';

// Package ImportS
import {
    SubjectColumn,
    NumericalMarkColumn,
    CategoricalMarkColumn
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for ACT
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} options - an array of available categorical mark options
 * @returns {JSX.Element} - the rendered table row 
 */
function ACTCombinedWeightCategoryAndNumericalRow({rowId, subjects, options}) {
    subjects = subjects || []; 
    options = options || {};
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState('');
    const [selectedType, setSelectedType] = useState(options[0] ||  '');
    const [aCount, setACount] = useState(0);
    const [bCount, setBCount] = useState(0);
    const [cCount, setCCount] = useState(0);
    const [dCount, setDCount] = useState(0);
    const [eCount, setECount] = useState(0);
    
    useEffect(() => {
        handleDataUpdate(
            rowId, enteredSubject, selectedType,
            aCount, bCount, cCount, dCount, eCount
        );
    }, [
        rowId, enteredSubject, selectedType,
        aCount, bCount, cCount, dCount, eCount
    ]);

    const inputFormat = { 
        maxRange: 10,
        step: 1,
    }
    return ( 
        <div className='table-row'> 
            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']} />
            <CategoricalMarkColumn options={options} setSelectedMark={setSelectedType} style={columnStyles['mark']}/>
            <NumericalMarkColumn enteredMark={aCount} inputFormat={inputFormat} setEnteredMark={setACount} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={bCount} inputFormat={inputFormat} setEnteredMark={setBCount} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={cCount} inputFormat={inputFormat} setEnteredMark={setCCount} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={dCount} inputFormat={inputFormat} setEnteredMark={setDCount} style={columnStyles["mark"]} />
            <NumericalMarkColumn enteredMark={eCount} inputFormat={inputFormat} setEnteredMark={setECount} style={columnStyles['mark_end']} />
        </div>
    )
}

/**
 * setup functions for initialising the styles for each column, primarly used for setting up equal width and right border
 * @returns {Object} styles object used to customise table column
 */
function setupColumnStyles() {
    const width = `${100/7}%`;
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
 * @param {number} rowId - the id of the current row
 * @param {string} enteredSubject - the subject entered by the user
 * @param {string} selectedType - type of assessment 'MAJOR' or 'MINOR' selected by the user 
 * @param {number} outstandingMark - the number of time the student has achieved outstanding mark
 * @param {number} highMark - the number of time the student has achieved high mark
 * @param {number} soundMark - the number of time the student has achieved sound mark
 * @param {number} basicMark - the number of time the student has achieved basic mark
 * @param {number} limitedMark - the number of time the student has achieved limited mark
 */
function handleDataUpdate(rowId, enteredSubject, selectedType, outstandingMark, highMark, soundMark, basicMark, limitedMark) {
    const ins = RowDataHandler.getInstance(); 
    ins.insertData(rowId, enteredSubject, {
        "type": selectedType,
        "marks": {
            "A": outstandingMark,
            "B": highMark,
            "C": soundMark, 
            "D": basicMark, 
            "E": limitedMark
        }
    });
}

export default ACTCombinedWeightCategoryAndNumericalRow;
