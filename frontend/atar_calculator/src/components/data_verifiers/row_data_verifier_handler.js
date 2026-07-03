// Package Imports
import {
    ApplicationIDVerifier,
    RegionGradeTypeCompatibilityVerifier,
    SubjectCountVerifier,
    SubjectWeightingVerifier,
    ATARResultVerifier,
    RegionSelectedVerifier
} from './row_data_verifier';

class RowDataVerifierHandler {
    /**
     * handler class used to setup all the verifiers to verify user inputs
     * @param {function} setDisplayMsg method used to set the error message to be displayed
     */
    constructor(setDisplayMsg) {
        this.verifier = new ApplicationIDVerifier(setDisplayMsg);
        this.verifier.setNext(new RegionSelectedVerifier(setDisplayMsg))
                     .setNext(new RegionGradeTypeCompatibilityVerifier(setDisplayMsg))
                     .setNext(new SubjectCountVerifier(setDisplayMsg))
                     .setNext(new SubjectWeightingVerifier(setDisplayMsg))
                     // The following must be at the end
                     .setNext(new ATARResultVerifier(setDisplayMsg))
    }

    /**
     * method used to check if the input data is valid or not
     * @returns {boolean} TRUE if the input data is valid, otherwise FALSE
     */
    isValid() {
        return this.verifier.isValid();
    }
}

export default RowDataVerifierHandler;