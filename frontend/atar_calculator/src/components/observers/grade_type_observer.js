// Package Imports;
import { DEFAULT_VALUES } from "../../constants/constants";
import DataObserver from "./data_observer";

class GradeTypeObserver extends DataObserver {
    /**
     * observer for grade type value, that automatically updates all relevant listeners
     */
    constructor() {
        super(DEFAULT_VALUES['grade_type']);
    }

    static getInstance() {
        if (!GradeTypeObserver.instance) {
            GradeTypeObserver.instance = new GradeTypeObserver();
        }
        return GradeTypeObserver.instance;
    }
}

export default GradeTypeObserver;
