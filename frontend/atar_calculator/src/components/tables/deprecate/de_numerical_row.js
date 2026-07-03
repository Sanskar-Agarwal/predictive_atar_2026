import "../../styles/subject_table_row.css";
import { SubjectDropdownList, SubjectLevelDropdownList } from "./utility/dropdown_list";
import { useState, useEffect } from 'react';

export function NumericalRow(props) {
    const width = `${100 / 4}%`;
    const subjects = props.subjects || [];
    const subjectLevels = props.subjectLevels || {};
    // Initialise subject levels
    subjects.forEach(
        subject => {
            if (!subjectLevels[subject]) 
                subjectLevels[subject] = ["Select"];
        }
    );

    // useState Variables
    // Subject related
    const [selectedSubject, setSelectedSubject] = useState(subjects[0]);
    const [selectedSubjectLevel, setSelectedSubjectLevel] = useState();

    // Mark related
    const [enteredMark, setEnteredMark] = useState(0);
    const [markRange, setMarkRange] = useState({});
    subjects.forEach(
        subject => {
            if (!markRange[subject]) 
                markRange[subject] = 100;
        }
    );
    const [currentMaxMark, setCurrentMaxMark] = useState(markRange[selectedSubject]); 
    
    // Functions for handling marks
    const handleMarkChange = (event) => {
        const currentMark = parseInt(event.target.value);
        if (currentMark <= markRange[selectedSubject])
            setEnteredMark(currentMark);
    }

    const handleMarkRangeChange = (event) => {
        const maxScore = parseInt(event.target.value);
        setCurrentMaxMark(maxScore)
        setMarkRange(
            prevRange => (
                {
                    ...prevRange, 
                    [selectedSubject]: maxScore,
                }
            )
        );
    }
    
    useEffect(
        () => {
            setMarkRange(
                prevRange => (
                    {
                        ...prevRange,
                        [selectedSubject]: prevRange[selectedSubject] || 100 // Set default value if not defined
                    }
                )
            );
            setCurrentMaxMark(markRange[selectedSubject]);
        }, [selectedSubject]
    )
    
    return (
        <div className="table-row">
            <div className="subject-column" style={{width: width}}>
                <SubjectDropdownList options={subjects} setSelectedSubject={setSelectedSubject} />
            </div>
            <div className="assessment-column" style={{width: width}}>
                <SubjectDropdownList options={subjectLevels[selectedSubject]} setSelectedSubject={setSelectedSubjectLevel} />
            </div>
            <div className="mark-column" style={{ width: width}}>
                <input
                        type="number"
                        className="numerical-input"
                        min="0"
                        max={markRange[selectedSubject]}
                        step="1"
                        value={enteredMark} // Here you can set the initial value for the mark column
                        onChange={handleMarkChange}
                    />
            </div>
            <div className="range-column" style={{ width: width}}>
            <input
                        type="number"
                        className="numerical-input"
                        min="0"
                        max={markRange[selectedSubject]}
                        step="1"
                        value={currentMaxMark} // Here you can set the initial value for the mark column
                        onChange={handleMarkRangeChange}
                    />
            </div>
        </div>
    ); 
}
