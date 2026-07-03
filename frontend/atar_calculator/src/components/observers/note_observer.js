// Package Imports;
import DataObserver from "./data_observer";

class NoteObserver extends DataObserver {
     /**
     * observer for region value, that automatically updates all relevant listeners
     */
    constructor() {
        super('');
    }

    static getInstance() {
        if (!NoteObserver.instance) {
            NoteObserver.instance = new NoteObserver();
        }
        return NoteObserver.instance;
    }
}

export default NoteObserver;