// Package Imports;
import { DEFAULT_VALUES } from "../../constants/constants";
import DataObserver from "./data_observer";

class RegionObserver extends DataObserver {
     /**
     * observer for region value, that automatically updates all relevant listeners
     */
    constructor() {
        super(DEFAULT_VALUES['region']);
    }

    static getInstance() {
        if (!RegionObserver.instance) {
            RegionObserver.instance = new RegionObserver();
        }
        return RegionObserver.instance;
    }
}

export default RegionObserver;