// Library Import
import React, { useState, useEffect } from "react";

// Package Imports
import { GRADE_TYPES, REGIONS, GRADE_TYPE_LABELS, DEFAULT_VALUES } from '../constants/constants.js'; 
import { DropDownList } from './tables/utility/dropdown_list.js';
import CatWalker from '../components/animations/cat_walker.js';
import ClearPageContentCommand from "./commands/clear_page_content_command.js";

// Data Verifier
import RowDataVerifierHandler from '../components/data_verifiers/row_data_verifier_handler.js';

// Data Handler
import RequestHandler from "../components/data_handlers/request_handler.js";
import RowDataHandler from "../components/data_handlers/row_data_handler.js";
import RequestDataHandler from "./data_handlers/request_data_handler.js";

// Observers
import GradeTypeObserver from "./observers/grade_type_observer.js";
import RegionObserver from "./observers/region_observer.js";
import ApplicationIDObserver from "./observers/application_id_observer.js";
import ApplicantNameObserver from "./observers/applicant_name_observer.js";
import NoteObserver from "./observers/note_observer.js";

/**
 * web page dropdown element that allows the user to pick a grade type from a pre-defined list
 * @returns {JSX.Element} The rendered the grade type dropdown list
 */
export function GradeTypeDropDownList() {
    const observer = GradeTypeObserver.getInstance();
    const [gradeType, setGradeType] = useState(observer.getValue());
    observer.addListener(setGradeType);
    
    const handleValueChange = (value) => { 
        UpdateGradeTypeValue(value, observer);
    }

    const style = { 
        'dropdown-option': { 
            zIndex: 99,
        }
    }
    
    return (
        <div className="grade-type-container">
            <DropDownList optionSelected={gradeType} options={GRADE_TYPES} handleValueChange={handleValueChange} style={style}/>
        </div>
    );
}

/**
 * update the relevant information after grade type changed
 * @param {string} gradeType the newly selected grade type
 * @param {Object} observer grade type observer to update all the listeners
 * @returns {string} the newly selected grade type if it's not other, otherwise return the default value
 */
function UpdateGradeTypeValue(gradeType, observer){ 
    const rowDataHandler = RowDataHandler.getInstance(); 
    const requestDataHandler = RequestDataHandler.getInstance();
    ClearDataHandler(rowDataHandler, requestDataHandler);

    if (gradeType === 'Other') {
        observer.updateValue(DEFAULT_VALUES['grade_type']);
        requestDataHandler.setGradeType(DEFAULT_VALUES['grade_type']);
    } else {
        observer.updateValue(gradeType);
        requestDataHandler.setGradeType(gradeType);
    }
}

/**
 * method for clearing all subjects inside request data handler and clearing all values inside row data handler
 * @param {Object} rowDataHandler data handler object that keeps track of row information 
 * @param {Object} requestDataHandler data handler object that keeps track of data inside a request
 */
function ClearDataHandler(rowDataHandler, requestDataHandler) {
    rowDataHandler.clear();
    requestDataHandler.clearGradeTypeData(requestDataHandler.getGradeType());
}

/**
 * web page dropdown elements & application id text field
 * @returns {JSX.Element} The rendered the region dropdown list and application id text field
 */
export function RegionAndApplicationIDContainer() {
    const ins = RequestDataHandler.getInstance();
    const [selectedRegion, setSelectedRegion] = useState(DEFAULT_VALUES['region']);
    const [applicationID, setApplicationID] = useState('');
    const [applicantName, setApplicantName] = useState('');
    const observers = initObservers(setSelectedRegion, setApplicationID, setApplicantName);

    const style = { 
        'dropdown-list-container': { 
            margin: 0,
            width: "10em",
        },
        'selected-option': {
            backgroundColor: 'var(--default-bg-color)',
            color: 'white',
        },
        'option-arrow-down': { 
            borderColor: 'white transparent transparent transparent'
        },
        'dropdown-option': { 
            zIndex: 90,
        }
    }

    const handleRegionChange = (region) => { 
        const ins = RequestDataHandler.getInstance();
        observers['region'].updateValue(region);
        ins.setRegionAbbr(region);
    }
    
    const handleIDChange = (e) => {
        const value = (e.target.value).trim();
        const intValue = parseInt(value);
        if (intValue) {
            observers['application_id'].updateValue(intValue);
            ins.setApplicationID(intValue);
        } else { 
            observers['application_id'].updateValue('');
            ins.setApplicationID('');
        }
    }

    const handleNameChange = (e) => {
        const value = (e.target.value);
        observers['applicant_name'].updateValue(value);
        ins.setApplicantName(value);
    }

    const handleNameBlur = (e) => {
        const value = (e.target.value).trim(); 
        observers['applicant_name'].updateValue(value);
        ins.setApplicantName(value);
    }
    
    return (
        <div className='region-and-app-id-container'>
            <DropDownList optionSelected={selectedRegion || 'Region'} options={REGIONS} handleValueChange={handleRegionChange} style={style}/>
            <input 
                type='text'
                placeholder='Application ID'
                value={applicationID}
                onChange={handleIDChange}
            />
            <input 
                type='text'
                placeholder='Applicant Name'
                value={applicantName}
                onChange={handleNameChange}
                onBlur={handleNameBlur}
            />
        </div>
    );
}

/**
 * initialised region, application id and applicant name observers
 * @param {function} setSelectedRegion updater function for region abbreviation
 * @param {function} setApplicationID updater function for application id
 * @param {function} setApplicantName updater function for applicant name
 * @returns {Object} a key:value pair of observers
 */
function initObservers(setSelectedRegion, setApplicationID, setApplicantName) {
    const regionObserver = RegionObserver.getInstance();
    const applicationIDObserver = ApplicationIDObserver.getInstance();
    const applicantNameObserver = ApplicantNameObserver.getInstance(); 

    regionObserver.addListener(setSelectedRegion);
    applicationIDObserver.addListener(setApplicationID);
    applicantNameObserver.addListener(setApplicantName);

    const observers = { 
        'region': regionObserver,
        'application_id': applicationIDObserver,
        'applicant_name': applicantNameObserver
    };
    return observers;
}

/**
 * web page text box element for showing a grade type description
 * @returns {JSX.Element} The rendered the description text field
 */
export function DescriptionContainer() {
    const observer = GradeTypeObserver.getInstance();
    const [desc, setDesc] = useState('');
    const [gradeType, setGradeType] = useState(observer.getValue());
    observer.addListener(setGradeType);
    
    const baseTitleLength = 'Description'.length;
    const styles = { 
        'description-title-text': {
            width: !gradeType ? `${baseTitleLength}em` : `${baseTitleLength + gradeType.length}rem`,
        }
    }
    
    useEffect(
        () => {
            fetchGradeTypeDescription(gradeType, setDesc);
        }, [gradeType]
    );
    return (
        <div className='description-container'>
            <div className="description-title-text" style={styles['description-title-text']}>
                Description {
                    !gradeType ? 
                    "" : 
                    `\t${gradeType}`
                }
            </div>
            { 
                !desc ? <div /> :
                <div className="description-body-text"> 
                    {desc}
                </div>
            }
        </div>
    );
}

/**
 * method to fetch description from the backend based on the selected grdae type
 * @param {string} gradeType gradeType selected by the user
 * @param {function} setDesc function used to set the current description to be displayed
 */
async function fetchGradeTypeDescription(gradeType, setDesc) { 
    if (!gradeType || [DEFAULT_VALUES['grade_type'], 'Other'].includes(gradeType)  ) {
        setDesc('');
        return; 
    }
    try { 
        const ins = RequestHandler.getInstance(); 
        const fetchedDescriptions = await ins.getGradeTypeDescription(GRADE_TYPE_LABELS[gradeType]);
        setDesc(fetchedDescriptions);
    } catch (error) {
        console.log('Error fetching subjects: ', error);
    }
};

/** 
 * a container for handling the submission of subjects for the calculation of ATAR
 * @param {setGradeType} method used for the clear button to reload the page
 * @returns {JSX.Element} div elements to be displayed on the webpage
 */
export function FormSubmissonContainer() {
    const [displayMsg, setDisplayMsg] = useState(DEFAULT_VALUES['display_message']);
    const [hasError, setHasError] = useState(false);
    const [catAlive, setCatAlive] = useState(false);

    return ( 
        <div className='footer-container'>
            <CatWalker catAlive={catAlive}/>
            <div className='submission-container'>
                <FormSubmissionLeftContainer 
                    hasError={hasError} 
                    catAlive={catAlive} setCatAlive={setCatAlive}
                    displayMsg={displayMsg}/>
                <FormSubmissionRightContainer setHasError={setHasError} setDisplayMsg={setDisplayMsg} />
            </div>
        </div>
    );
} 

/**
 * left components of the form submission container
 * @param {Object} props - component props
 * @param {boolean} hasError - boolean value that determined if there is an error with the verifier
 * @param {function} setDisplayMsg - function used to set the shown messages
 * @param {boolean} catAlive - boolean value to show/hide the cat
 * @param {function} setCatAlive - function used to toggle the cat alive status
 * @returns {JSX.Element} div elements to be displayed on the webpage
 */
function FormSubmissionLeftContainer({hasError, displayMsg, catAlive, setCatAlive}) { 
    const toggleCatLife = () => {
        setCatAlive(!catAlive);
    }

    return (
        <div className='form-submission-left-container'>
            <button className='cat-button' onClick={toggleCatLife}>Cat</button>
            <div className="result-container">
                ATAR Predicted
                <div className="atar-result">
                    {
                        hasError ? 
                            <div className='error-message'>{displayMsg}</div>
                            : <h3>{displayMsg}</h3>
                    }
                </div>
            </div>
        </div>
    );
}

/**
 * right components of the form submission container 
 * @param {Object} props - component props
 * @param {function} setHasError - function used to set if the verifier output any error
 * @param {function} setDisplayMsg - function used to set the shown messages
 * @returns {JSX.Element} div elements to be displayed on the webpage
 */
function FormSubmissionRightContainer({setHasError, setDisplayMsg}) {
    const verifier = new RowDataVerifierHandler(setDisplayMsg);
    const handleOnSubmit = async () => {
        setDisplayMsg('Processing');
        PrepareRequestData();
        await sendDataToBackend(verifier, setHasError, setDisplayMsg);
    }

    const handleClearPage = () => {
        reloadPage(setHasError, setDisplayMsg);
    }

    return ( 
        <div className='form-submission-right-container'>
            <div className='button-container'>
                <button className='clear-button' onClick={handleClearPage}>CLEAR</button>
                <button className="submit-button" onClick={handleOnSubmit}>
                    SUBMIT
                </button>
            </div> 
        </div>
    );
}

/**
 * preparing the data inside a request data handler to ensure that the data is formatted correctly
 */
function PrepareRequestData() { 
    const requestDataHandler = RequestDataHandler.getInstance(); 
    const rowDataHandler = RowDataHandler.getInstance();
    requestDataHandler.clearGradeTypeData(requestDataHandler.getGradeType());
    requestDataHandler.insertSubjects(rowDataHandler.getData());
}

/**
 * method used to send required information to the database to calculate the predicted atar
 * @param {Object} verifier an object for verifying if the entered data are valid
 * @param {function} setHasError if the entered data are invalid, this method is set to TRUE otherwise FALSE
 */
async function sendDataToBackend(verifier, setHasError) { 
    if (!verifier.isValid()) { 
        setHasError(true);
        return;
    }
    setHasError(false);
}

/**
 * method used to simulate a page refresh and clear all contents inside the table 
 * @param {function} setHasError used to indicate the system that there is no longer any error message
 * @param {function} setDisplayMsg used to reset the current display message
 */
function reloadPage(setHasError, setDisplayMsg) {
    const clearPageContentCommand = new ClearPageContentCommand();
    clearPageContentCommand.execute();
    setDisplayMsg(DEFAULT_VALUES['display_message']);
    setHasError(false);
}

/**
 * textarea that allows the user to enter additional note
 * @returns {JSX.Element} renderd note textarea
 */
export function NoteContainer() {
    const observer = NoteObserver.getInstance();
    const [note, setNote] = useState(observer.getValue());
    observer.addListener(setNote);

    const handleOnChange = (e) => { 
        const value = (e.target.value); 
        const ins = RequestDataHandler.getInstance();
        ins.setNote(value);
        observer.updateValue(value);
    }

    return (
        <textarea 
            className='note-container'
            placeholder='Note'
            value={note}
            maxLength='500'
            onChange={handleOnChange}
        />
    );
}
