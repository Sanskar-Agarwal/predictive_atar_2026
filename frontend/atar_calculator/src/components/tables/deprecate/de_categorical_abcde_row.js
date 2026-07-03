import "../../styles/subject_table_row.css";
import { MarkDropdownList, SubjectDropdownList } from "../utility/dropdown_list";
import { useState, useEffect, useMemo } from "react";


function CategoricalABCDE(props) { 
    const subjects = useMemo(() => props.subjects || [], [props.subjects]);
    const subjectLevels = useMemo(() => {
        const levels = { ...props.subjectLevels };
        levels[subjects[0] || ""] = ["Select"];
        return levels;
    }, [props.subjectLevels, subjects]);
    

    // Static Variables
    const markOptions = [
        'Grade', 
        'A', 'B', 'C', 'D', 'E'
    ];
    subjectLevels[subjects[0] || ""] = ["Select"];
    
    // Usestate variables
    const [selectedSubject, setSelectedSubject] = useState(subjects[0] || "");
    const [currentSubjectLevels, setCurrentSubjectLevels] = useState(subjectLevels[selectedSubject] || []);
    const [selectedSubjectLevel, setSelectedSubjectLevel] = useState();
    const [mark, setSelectedMark] = useState(markOptions[0]);


    // UseEffect Section
    useEffect( () => {
        setCurrentSubjectLevels(subjectLevels[selectedSubject]);
        }, [selectedSubject, subjectLevels]
    );


    const width = `${100 / 3}%`;
    return (
        <div className="table-row">
             <div className="subject-column" style={{ width:width}}>
               <SubjectDropdownList options={subjects} setSelectedSubject={setSelectedSubject} />
            </div>
            <div className="assessment-column" style={{ width: width}}>
                <SubjectDropdownList options={currentSubjectLevels} setSelectedSubject={setSelectedSubjectLevel}/>
            </div>
            <div className="mark-column" style={{width: width}}>
                <MarkDropdownList options={markOptions} setSelectedMark={setSelectedMark}/>
            </div>
        </div>
    );
}

export default CategoricalABCDE;