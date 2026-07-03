// Package Imports;
import DataObserver from "./data_observer";

class ApplicantName extends DataObserver {
     /**
     * observer for region value, that automatically updates all relevant listeners
     */
    constructor() {
        super('');
    }

    static getInstance() {
        if (!ApplicantName.instance) {
            ApplicantName.instance = new ApplicantName();
        }
        return ApplicantName.instance;
    }
}

export default ApplicantName;