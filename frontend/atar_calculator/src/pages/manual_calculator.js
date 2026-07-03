// Library Imports
import { useState } from 'react';

// Package Imports
import Template from "../components/template";
import SubjectSelectionTable from "../components/subject_selection_table";
import { 
    DescriptionContainer,
    GradeTypeDropDownList,
    RegionAndApplicationIDContainer,
    NoteContainer,
    FormSubmissonContainer
} from '../components/manual_calculator_components.js';
import { DEFAULT_VALUES } from "../constants/constants.js";

import GradeTypeObserver from "../components/observers/grade_type_observer.js";
import RegionObserver from "../components/observers/region_observer.js";


// CSS Imports
import '../styles/manual_calculator.css';

/**
 * The manual calculator page that allows the user to manual entering subjects to get the predicted atar 
 * @param {Object} props - component props
 * @param {boolean } hasTemplate - boolean toggle to determine if the page should be loaded with template or not
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function ManualCalculator({hasTemplate=true}) {
    const [gradeType, setGradeType] = useState(DEFAULT_VALUES['grade_type']);
    const [region, setRegion] = useState(DEFAULT_VALUES['region']);
    initObservers(setGradeType, setRegion);

    return (
        <>
            { hasTemplate ?
                 <Template /> : <></>
            }
            <div className="body-container">
                <GradeTypeDropDownList />
                <RegionAndApplicationIDContainer />
                {
                    (gradeType !== DEFAULT_VALUES['grade_type'] && region !== DEFAULT_VALUES['region']) ?
                    <>
                        <DescriptionContainer />
                        <SubjectSelectionTable gradeType={gradeType} region={region}/>
                        <NoteContainer />
                        <FormSubmissonContainer /> 
                    </> : <div />
                }
            </div>
        </>
    );
} 

function initObservers(setGradeType, setRegion) {
    const gradeTypeObserver = GradeTypeObserver.getInstance();
    const regionObserver = RegionObserver.getInstance();
    gradeTypeObserver.addListener(setGradeType);
    regionObserver.addListener(setRegion);
}

export default ManualCalculator;
