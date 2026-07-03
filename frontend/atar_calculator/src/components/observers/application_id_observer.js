// Package Imports;
import DataObserver from "./data_observer";

class ApplicationIDObserver extends DataObserver {
     /**
     * observer for region value, that automatically updates all relevant listeners
     */
    constructor() {
        super('');
    }

    static getInstance() {
        if (!ApplicationIDObserver.instance) {
            ApplicationIDObserver.instance = new ApplicationIDObserver();
        }
        return ApplicationIDObserver.instance;
    }
}

export default ApplicationIDObserver;