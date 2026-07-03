// Package Imports
import { DEFAULT_VALUES } from '../../constants/constants';

class RequestDataHandler { 
    /**
     * Data handler class used to maintain information on data to be encapsulated in a request,
     * which is then sent to the backend
     */
    constructor()  {
        this.initData();
    }    
    
    /**
     * initialisating default data
     */
    initData() {
        this.data = {
            'region_abbr': '',
            'grade_type': '',
            'application_id': '', 
            'applicant_name': '',
            'note': '',
            'subjects': {}
        };
    }
    
    /**
     * Singleton pattern used to get an instance of OutputDataHandler
     * @returns {Object} instance of OutputDataHandler
     */
    static getInstance() {
        if (!RequestDataHandler.instance) {
            RequestDataHandler.instance = new RequestDataHandler();
        }
        return RequestDataHandler.instance;
    }
    
    /**
     * method used to add an array of subjects to the {...} to be sent to the backend
     * @param {Array } subjects array of subjects to be added to the requests
     */
    insertSubjects(subjects) {
        const gradeType = this.data['grade_type'];
        if (gradeType === '' || gradeType === DEFAULT_VALUES['grade_type']) {
            return;
        }

        this.data['subjects'][gradeType] = {};

        for (let rowId in subjects) {
            const subject = subjects[rowId]['subject'];
            if (subject && subject !== '') {
                this.insertDefaultSubjectObject(gradeType, subject);
                const info = subjects[rowId]['info'];
                this.insertSubject(subject, info, gradeType,);
            }
        }
    }
    
    /**
     * Check if the subject existed in data container. If not initialised it as an empty object {}
     * @param {string} gradeType the grade type that the subject is to be added to
     * @param {string} subject the name of the subject to be added
     */
    insertDefaultSubjectObject(gradeType, subject) { 
        if (!this.data['subjects'][gradeType][subject]) {
            this.data['subjects'][gradeType][subject] = {}
        }
    }

    /**
     * Check if the subject has a weighted format or not and inserted them accordingly
     * @param {string} subject the name of the subject to be added
     * @param {Object} info object storing relevant information related to the subjec 
     * @param {string} gradeType the gradetype for the subject & info to be added to
     */
    insertSubject(subject, info, gradeType) {
        if (info['mark'] !== undefined || info['type'] !== undefined) {
            this.data['subjects'][gradeType][subject] = info;
        } else { 
            const assessment = Object.keys(info)[0];
            this.data['subjects'][gradeType][subject][assessment] = info[assessment];
        }
    }

    /**
     * set the 'grade_type' attribute to the provided gradeType
     * @param {string} gradeType the gradeType to be changed to
     */
    setGradeType(gradeType) {
        this.data["grade_type"] = gradeType;
    }

    /**
     * set the 'region_abbr' attribute to the provided regionAbbr
     * @param {string} regionAbbr the regionAbbr to be changed to
     */
    setRegionAbbr(regionAbbr) { 
        this.data["region_abbr"] = regionAbbr;
    }
    
    /**
     * set the 'application_id' attribute to the provided applicaionID
     * @param {string} applicationID the applicationID to be changed to
     */
    setApplicationID(applicationID) { 
        this.data["application_id"] = applicationID;
    }
    
    /**
     * set the 'applicant_name' attribute to the provided applicantName
     * @param {string} applicantName the name of the applicant
    */
    setApplicantName(applicantName) {
        this.data['applicant_name'] = applicantName;
    }

    /**
     * set the 'note' attribute to the provided note
     * @param {string} note the note provided by the user
    */
    setNote(note) {
        this.data['note'] = note;
    }

    /**
     * method to retrieved 'grade_type' attributes 
     * @returns {string} the current value of 'grade_type'
     */
    getGradeType() { 
        return this.data['grade_type'];
    }
    
    /**
     * method to retrieved 'region_abbr' attributes 
     * @returns {string} the current value of 'region_abbr'
     */
    getRegionAbbr() { 
        return this.data['region_abbr']; 
    }

    /**
     * method used to check if an application_id has been provided
     * @returns {boolean} TRUE if an application_id has been provided, otherwise FALSE
     */
    hasApplicationID() { 
        if (!this.data['application_id'])
            return false; 
        return true;
    }
    
    /**
     * method to get the number of subjects associated with a grade type
     * @returns {number} the number of subjects of the current gradeType
     */
    getSubjectCount() {
        return Object.keys(this.data['subjects'][this.getGradeType()]).length;
    }

    /**
     * method used to retrieved all relevant data to be sent to the backend
     * @returns {Object} the encapsulated data
     */
    getData() {
        return this.data;
    }

    /**
     * 
     * @returns {Array} an array of subjects based on the current grade type
     */
    getSubjects() { 
        return this.data['subjects'][this.getGradeType()];
    }

    /**
     * method used to clear all contents
     */
    clearData() {
        this.initData();
    }

    /**
     * method used to clear all subjects associated with a gradeType 
     * @param {string} gradeType the given gradeType to be cleared
     */
    clearGradeTypeData(gradeType) {
        if (gradeType !== 'Grade Type')
            this.data['subjects'][gradeType] = {};
    }
 
}

export default RequestDataHandler;
