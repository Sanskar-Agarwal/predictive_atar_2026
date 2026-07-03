class RequestHandler {
    /**
     * Data Handler used to deal with all the related web requests
     */
    constructor() {
        // In local dev (Docker or npm start) this defaults to the separate
        // backend container/process. In production, REACT_APP_API_URL is set
        // to "" at build time so the app calls the same origin it's served
        // from, since Django serves both the API and the built frontend.
        this.path = process.env.REACT_APP_API_URL ?? "http://127.0.0.1:8026";
    }
    
    /**
     * Singleton pattern used to get an instance of RequestHandler
     * @returns {Object} instance of RequestHandler
     */
    static getInstance() {
        if (!RequestHandler.instance) {
            RequestHandler.instance = new RequestHandler();
        }
        return RequestHandler.instance;
    }

    /**
     * request method to get a list of subjects given a region abbreviation from the backend 
     * @param {String} regionAbbr the selected region abbreviation
     * @returns {Array} a list of subjects associated with the region abbreviation
     */
    async getSubjectsByRegionAbbr(regionAbbr) {
        const url = `${this.path}/fill_information/search_subjects_by_region_abbreviation/`;
        // Use fetch or any other HTTP library to send the POST request
        return await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "region_abbr": regionAbbr
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            // console.log('Response from server:', data);
            return this.getSubjectNamesFromResponse(data); // Return the data to handle elsewhere if needed
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
            throw error; // Rethrow the error for higher-level handling
        });
    }
    
    /**
     * used to extract all subject names from a response
     * @param {Object} response 
     * @returns {Array} of subject names
     */
    getSubjectNamesFromResponse(response) {
        let names = [];

        Object.keys(response).forEach(key => {
            const subjects = response[key];
            subjects.forEach( 
                (subject) => { 
                    names.push(subject['subject']);
                }
            )
        });
        return names;
    }
    
    /**
     * request method to get the predicted atar
     * @param {Object} data json value object to be sent to the backend
     * @returns {string} the predicted atar in a string format
     */
    async getAtar(data) { 
        const url = `${this.path}/fill_information/get_atar/`;
        // Use fetch or any other HTTP library to send the POST request
        return await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            // console.log('Response from server:', data);
            // Surface a backend block/error (e.g. NSW <10 units) as a thrown error
            // so it is shown to the user instead of rendering as NaN.
            if (data && data.error) {
                throw new Error(data.error);
            }
            // Return both the atar and any auto-generated note
            return { atar: data['atar'], note: data['note'] || '' };
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
            throw error; // Rethrow the error for higher-level handling
        });
    }

    /**
     * request method to get the description of a selected grade type
     * @param {String} gradeType the selected gradeType
     * @returns {String} the description text of a given grade type
     */
    async getGradeTypeDescription(gradeType) { 
        const url = `${this.path}/fill_information/get_grade_type_description/?label=${gradeType}`;
        return await fetch(url, {
            method: 'GET', 
            headers: { 
                'Content-Type': 'application/json'
            }, 
        })
        .then(response => response.json())
        .then(data => { 
            // console.log('Response from server:', data);
            return data['description'];
        })
        .catch(error => {
            console.error('Error:', error);
            throw error; 
        });
    }

    /**
     * request method that allows the user to login into the system
     * @param {string} email the provided email by the user
     * @param {string} password the provided password by the user
     * @returns {Object} response status from the backend
     */
    async loginUser(email, password) {
        const url = `${this.path}/core/login/`;
        // Use fetch or any other HTTP library to send the POST request
        return await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'email': email, 
                'password': password
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            // console.log('Response from server:', data);
            return data;
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
            throw error; // Rethrow the error for higher-level handling
        });
    }

    /**
     * upload a transcript PDF and get back extracted subjects/marks
     * @param {File} file the transcript PDF selected by the user
     * @returns {Object} { filename, region, grade_format, subjects, usage }
     */
    async uploadTranscript(file) {
        const url = `${this.path}/fill_information/upload_transcript/`;
        const formData = new FormData();
        formData.append('transcript', file);
        // NOTE: do not set Content-Type — the browser sets the multipart boundary.
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || `Upload failed (HTTP ${response.status})`);
        }
        return data;
    }
}

export default RequestHandler;
