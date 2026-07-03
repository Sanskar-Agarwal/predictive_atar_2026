class RowDataHandler {
    /**
     * data handler class used to maintain information of each table row data
     */
    constructor() {
        this.data = {}
    }

    /**
     * Singleton pattern used to get an instance of RowDataHandler
     * @returns {Object} instance of RowDataHandler
     */
    static getInstance() {
        if (!RowDataHandler.instance) {
            RowDataHandler.instance = new RowDataHandler();
        }
        return RowDataHandler.instance;
    }
    
    /**
     * method used to replace the current information given the row id 
     * @param {number} rowId the id of the row to be replaced
     * @param {string} subject the name of the subject associated with the row
     * @param {Object} info other relevant associated with the subject
     */
    insertData(rowId, subject, info) {
        if (!subject || subject === '') { 
            this.data[rowId] = {};
            return; 
        }

        if (!this.data[rowId]) {
            this.data[rowId] = { 'subject': '', 'info': {}}
        }
        this.data[rowId]['subject'] = subject;
        this.data[rowId]['info'] = info;
    }
    
    /**
     * method used to remove a single row's data by its row id (used when a row
     * is deleted so the removed subject is not submitted)
     * @param {number} rowId the id of the row to remove
     */
    removeData(rowId) {
        delete this.data[rowId];
    }

    /**
     * method used to retrieved all row data
     * @returns {Array} an arrays of row data
     */
    getData() {
        return this.data;
    }

    /**
     * method used to clear all the row data
     */
    clear() {
        this.data = {};
    }
}

export default RowDataHandler;