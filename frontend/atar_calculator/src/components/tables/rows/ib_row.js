// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import {
    SubjectColumn,
    NumericalMarkColumn,
    FixedSubjectColumn,
    CategoricalMarkColumn,
} from "../columns/table_columns.js";
import RowDataHandler from '../../data_handlers/row_data_handler.js';
import { CATEGORICAL_MARK_OPTIONS, IB_REQUIRED_SUBJECTS } from '../../../constants/constants.js';

// CSS Imports
import "../../../styles/components/subject_table_row.css";

/**
 * table row that encompasses all required field to get the predicted atar for International Baccalaurate (IB)
 * @param {Object} props - component props
 * @param {number} rowId - id of the current row
 * @param {Array} subjects - an array of available subjects that can be selected
 * @returns {JSX.Element} - the rendered table row 
 */
function IBRow({rowId, subjects}) {
    // IB - Internatioal Baccalaurate
    subjects = subjects || [];
    const columnStyles = setupColumnStyles();
    const [enteredSubject, setEnteredSubject] = useState(rowId < 2 ? IB_REQUIRED_SUBJECTS[rowId] : '');
    const [enteredMark, setEnteredMark] = useState(rowId < 2 ? CATEGORICAL_MARK_OPTIONS['ABCDE'][0] : '7'); 
    const inputFormat = {
        minRange: 1, 
        maxRange: 7,
        step: 1,
    };

    if (rowId < 2) { 
        handleDataUpdate(rowId, enteredSubject, enteredMark); 
    }

    useEffect(
        () => { 
            handleDataUpdate(rowId, enteredSubject, enteredMark); 
        }, [rowId, enteredSubject, enteredMark]
    );

    return (
        <div className="table-row">
            {
                rowId > 1  ?
                    (
                        <>
                            <SubjectColumn subjects={subjects} setEnteredSubject={setEnteredSubject} style={columnStyles['subjects']}/>
                            <NumericalMarkColumn enteredMark={enteredMark} setEnteredMark={setEnteredMark} inputFormat={inputFormat} style={columnStyles['mark']} />
                        </>
                    ) : 
                    (
                        <>
                            <FixedSubjectColumn subject={IB_REQUIRED_SUBJECTS[rowId]} style={columnStyles['subjects']}/>
                            <CategoricalMarkColumn options={CATEGORICAL_MARK_OPTIONS['ABCDE']} setSelectedMark={setEnteredMark} style={columnStyles['mark']}/>
                        </>
                    )
            }
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
            borderRight: '2px solid black'
        }, 
    }
    return styles;
}

/**
 * update function for updating the row information to RowDataHandler when a change occurred to each of the column
 * @param {number} rowId - id of the current row
 * @param {string} enteredSubject - subject entered by a user
 * @param {string} enteredMark - mark entered by a user
 */
function handleDataUpdate(rowId, enteredSubject, enteredMark ) {
    const ins = RowDataHandler.getInstance();
    ins.insertData(rowId, enteredSubject, {
        "mark": enteredMark,
    })
}
 
export default IBRow;
