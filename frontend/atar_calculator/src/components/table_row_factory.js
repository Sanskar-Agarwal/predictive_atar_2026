// Library Imports
import React from 'react';

// Package Imports
import { CATEGORICAL_MARK_OPTIONS } from "../constants/constants";
import CategoricalRow from "./tables/rows/categorical_row";
import MultipleCategoricalGradeRow from "./tables/rows/multiple_categorical_grade_row";
import NumericalRow from "./tables/rows/numerical_row";
import NumericalWeightedRow from "./tables/rows/numerical_weighted_row";
import SACERow from "./tables/rows/sace_row";
import SACEWeightedRow from "./tables/rows/sace_weighted_row";
import TasYearMixedRow from "./tables/rows/tas_year_mixed_row";
import IBRow from './tables/rows/ib_row';
import ACTCombinedWeightCategoryAndNumericalRow from "./tables/rows/act_combined_weight_category_and_numerical_row";
import NumericalAndCategoricalRow from "./tables/rows/numerical_and_categorical_row";

class TableRowFactory {
    /**
     * Factory class used for making the Table Row Object
     * @param {number} rowId the id of the row used for storing row data 
     * @param {Array} subjects array of subjects to be displayed for the dropdown list
     */
    constructor(
        rowId, subjects 
    ) { 
        const categoricalMarkOptions = CATEGORICAL_MARK_OPTIONS;
        this.factories = {
            'Numerical': <NumericalRow rowId={rowId} subjects={subjects} />,
            'ABCDE': <CategoricalRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['ABCDE']}/>,
            'OHSBL': <CategoricalRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['OHSBL']}/>,
            'Numerical Weighted': <NumericalWeightedRow rowId={rowId} subjects={subjects} />,
            'Multiple Categorical Grade': <MultipleCategoricalGradeRow rowId={rowId} subjects={subjects} />,
            'A+ to E-': <SACERow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['A+ to E-']} />,
            'A+ to E- With Weighted': <SACEWeightedRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['A+ to E-']} />,
            'TAS Year': <TasYearMixedRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['TAS Year']} />,
            'IB': <IBRow rowId={rowId} subjects={subjects} /> ,
            'ACT Combined Weighted Category & Numerical': <ACTCombinedWeightCategoryAndNumericalRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['ACT Combined Weighted Category & Numerical']} />,
            'Numerical & Categorical': <NumericalAndCategoricalRow rowId={rowId} subjects={subjects} options={categoricalMarkOptions['ABCDE']} />,
        }
    }
    
    /**
     * method for making variety of table row given the grede type
     * @param {string} gradeType the selected grade type to determine what table row to make 
     * @returns {JSX.Element} table row elements correspond to the grade type
     */
    makeTableRow(gradeType) {
        if (!this.factories.hasOwnProperty(gradeType)) {
            return <div />;
        }
        return React.cloneElement(this.factories[gradeType]);
    }
}

export default TableRowFactory;