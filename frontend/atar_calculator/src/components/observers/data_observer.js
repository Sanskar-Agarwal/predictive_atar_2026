class DataObserver {
    /**
     * observer class that is used to monitor any changes to a certain class, and update all its listeners based=
     * on the informed changed
     * @param {string} value default value stored by the observer
     */
    constructor(value) {
        this.value = value;
        this._listeners = [];
    }

    /**
     * get the current value being stored by the observer 
     * @returns {string} the current value being stored by the observer
     */
    getValue() {
        return this.value;
    }

    /**
     * update the current value being stored and notify all the listeners
     * @param {string} value the updated value to be replaced
     */
    updateValue(value) {
        this.value = value;
        this.notify();
    }

    /**
     * adding a new listener to be updated by the observer
     * @param {function} listener updating function used to update the value
     */
    addListener(listener) {
        if (!this._listeners.includes(listener)) {
            this._listeners.push(listener);
        }
    }

    /**
     * remove existing listener inside the observer if exists
     * @param {function} listener the listener to be removed
     */
    removeListener(listener) {
        const index = this._listeners.indexOf(listener);
        if (index !== -1) {
            this._listeners.splice(index, 1);
        }
    }

    /**
     * iterating through its listeners and update them accoriding to the new values
     */
    notify() {
        this._listeners.forEach((listener) => {
            listener(this.value);
        });
    }
}

export default DataObserver;