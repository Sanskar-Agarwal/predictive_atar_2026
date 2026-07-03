// Pacakge Imports
import { REGION_SUBJECT_COUNT_REQUIRED, REGION_GRADE_TYPES } from '../../constants/constants';
import RequestDataHandler from '../data_handlers/request_data_handler';
import RequestHandler from '../data_handlers/request_handler';
import NoteObserver from '../observers/note_observer';

class RowDataVerifier {
    /**
     * chain of responsibility class used to verify the user input data
     * @param {function} setDisplayMsg method used to set the error message to be displayed on the screen
     */
    constructor(setDisplayMsg) {
        this.setDisplayMsg = setDisplayMsg;
        this.next = null;
    }

    /**
     * set the next chain of command for verifying the user input
     * @param {Object} next the chain of command to be executed next
     * @returns {Object} the next chain of command object for streaming
     */
    setNext(next) {
        this.next = next;
        return next;
    }

    /**
     * template method used to check if the user input data is valid, and passed along the chain
     * if existed
     * @returns {boolean} TRUE if all operations return TRUE, otherwise FALSE
     */
    isValid() {
        const valid = this.verify();
        return this.checkNext(valid);
    }
    
    /**
     * Component of template method that can be overriden
     * @returns {boolean} TRUE if the user input data is valid, otherwise FALSE
     */
    verify() {

    }
    
    /**
     * default component of template method that chain the verifying process
     * by passing the responsibility to the next chain object 
     * @param {boolean} valid the current chain object verified result
     * @returns {boolean} TRUE if all operations in the chain returns TRUE, otherwise FALSE 
     */
    checkNext(valid) {
        if (!valid) {
            return valid;
        }

        if (this.next !== null) {
            return valid && this.next.isValid();
        }
        return valid;
    }
}

export class ApplicationIDVerifier extends RowDataVerifier {
    /**
     * Chain class used to verified if the application has been provided
     * and set the appropriate error message 
     * @returns {boolean} TRUE if application id has been provided, otherwise FALSE
     */
    verify() { 
        const ins = RequestDataHandler.getInstance();
        const valid = ins.hasApplicationID();
        if (!valid) {
            this.setDisplayMsg('No ID Provided');
        }
        return valid; 
    }
}

export class RegionSelectedVerifier extends RowDataVerifier {
    /**
     * Chain class used to check if the user has selected a region
     * @returns {boolean} TRUE if the user has selected a region, otherwise FALSE
     */
    verify() {
        const ins = RequestDataHandler.getInstance();
        const valid = ins.getRegionAbbr() !== '';
        if (!valid) {
            this.setDisplayMsg('Please Select a REGION');
        }
        return valid
    }
}

export class SubjectCountVerifier extends RowDataVerifier {
    /**
     * Chain class used to verified if the given gradeType has enough subject for the calculation
     * With the exception of 'TAS Year'
     * and set the appropriate error message 
     * @returns {boolean} TRUE if the current gradeType has appropriate number of subjects, otherwise FALSE
     */
    verify() {
        const ins = RequestDataHandler.getInstance();
        const region = ins.getRegionAbbr();
        const subjectCount = ins.getSubjectCount();
        let expectedCount = REGION_SUBJECT_COUNT_REQUIRED[region];

        let valid = false;
        valid = subjectCount >= expectedCount;
        if (!valid) {
            this.setDisplayMsg(`Must Provide at least ${expectedCount} subjects`);
        }
        return valid;
    }
}

export class RegionGradeTypeCompatibilityVerifier extends RowDataVerifier {
    /**
     * Chain class used to verify the selected grade type is one the current region's
     * calculator can actually process (see REGION_GRADE_TYPES for why not every
     * grade type works for every region), and set the appropriate error message
     * @returns {boolean} TRUE if the grade type is compatible with the region, otherwise FALSE
     */
    verify() {
        const ins = RequestDataHandler.getInstance();
        const regionAbbr = ins.getRegionAbbr();
        const gradeType = ins.getGradeType();

        const allowedGradeTypes = REGION_GRADE_TYPES[regionAbbr];
        if (!allowedGradeTypes) {
            return true;
        }

        const valid = allowedGradeTypes.includes(gradeType);
        if (!valid) {
            this.setDisplayMsg(
                `This Grade Type is not compatible with this region, please convert to ${allowedGradeTypes.join(', ')} for region ${regionAbbr}`
            );
        }
        return valid;
    }
}

export class SubjectWeightingVerifier extends RowDataVerifier {
    /**
     * Chain class used to verified if the weighting row has valid weightings
     * @returns {boolean} TRUE if none of the weighting is 0, and the total weighting sum up to at most 100%, otherwise FALSE
     */
    verify() {
        const ins = RequestDataHandler.getInstance(); 
        const gradeType = ins.getGradeType(); 
        if (!gradeType.includes('Weight') || gradeType.includes('ACT')) { 
            return true;
        }
        
        const subjects = ins.getSubjects();
        let valid = true; 
        Object.keys(subjects).forEach(
            (subject) => {
                if (!this.hasValidWeighting(subject, subjects[subject])) { 
                    valid = false; 
                    return; 
                }
            }
        )
        return valid;
    }
    
    /**
     * check if the subject assessments weighting are valid
     * @param {string} subject - subject the name of the subject associated with the assessments
     * @param {Object} assessments - object storing all assessments information associated with the subject
     * @returns 
     */
    hasValidWeighting(subject, assessments) {
        let totalWeighting = 0;
        let valid = true;
        Object.keys(assessments).forEach( 
            (assessment) => { 
                const info = assessments[assessment];
                const weighting = info.weighting;
                if (!this.verifyWeightingGreaterThanZero(weighting)) {
                    this.setDisplayMsg(`${subject} - ${assessment} must have weighting > 0`);
                    valid = false;
                    return;
                }
                totalWeighting += weighting; 
            }
        )
        
        if (!this.verifyTotalWeightingIsAtMost100(totalWeighting)) { 
            this.setDisplayMsg(`${subject} total Weighting must add up to 100%`); 
            valid = false; 
        }   
        return valid;
    }
    
    /**
     * check if an assessment weighting is at least greater than zero
     * @param {number} weighting - the weighting of a single assessment
     * @returns {boolean} - TRUE if the assessment weighting is greater than 0
     */
    verifyWeightingGreaterThanZero(weighting) { 
        return weighting > 0;
    }
    
    /**
     * check if the total weighting is at most 100%
     * @param {number} totalWeighting - sum of weighting for all assessments 
     * @returns {boolean} TRUE if total weighting is less than equal to 100
     */
    verifyTotalWeightingIsAtMost100(totalWeighting) {
        return totalWeighting <= 100;
    }
}

export class ATARResultVerifier extends RowDataVerifier {
    /**
     * Chain class used to request the forecasted ATAR
     * NOTE: this class must be the last one in the chain
     * @returns {boolean} TRUE if the database returns no error, otherwise false
     */
    verify() { 
        const requestDataHandler = RequestDataHandler.getInstance(); 
        const valid = this.getAtar(requestDataHandler.getData()); 
        // For debugging purposing
        if (valid) {
            console.log("\nSent Data");
            console.log(requestDataHandler.getData());
        }
        return valid;
    }

    /**
     * method used to get the predicted atar from the backend provided the information is valid
     * @param {Object} data encapuslated data in JSON format to send to the backend
     * @returns {Object} the predicted ATAR if existed, other JSON Object with error message
     */
    async getAtar(data) { 
        try {
            const ins = RequestHandler.getInstance();
            const fetched = await ins.getAtar(data);
            this.setDisplayMsg(parseFloat(fetched.atar).toFixed(2));

            // If the backend returned an auto-note (e.g. NSW <10 units), surface it
            // in the app's Note box. Append once — skip if it's already there so a
            // resubmit doesn't duplicate it.
            if (fetched.note) {
                const noteObserver = NoteObserver.getInstance();
                const current = noteObserver.getValue() || '';
                if (!current.includes(fetched.note)) {
                    const combined = current ? `${current} | ${fetched.note}` : fetched.note;
                    noteObserver.updateValue(combined);
                    RequestDataHandler.getInstance().setNote(combined);
                }
            }
            return true;
        } catch (error) {
            console.error("Error fetching atars:", error);
            // Show the backend's message (e.g. "Must provide at least 10 units ...")
            // rather than a generic string, so the user knows what to fix.
            this.setDisplayMsg(error.message || 'Invalid Data Input');
            return false;
        }
    }

}
