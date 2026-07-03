import ReactDOM from 'react-dom/client';

class RootManager {
  /**
   * class used for rendering different page
   */
  constructor() {
    this.root = null;
  }

  /**
   * method used to create the root instance that allows the page to re-render
   */
  createRoot() {
    const rootContainer = document.getElementById('app-container');
    if (!this.root && rootContainer) {
      this.root = ReactDOM.createRoot(rootContainer);
    }
  }

  /**
   * method used to retrived the root manager instance
   * @returns the current root manager instance
   */
  getRoot() { 
    return this.root;
  }

  /**
   * Singleton method for getting the instance of RootManager
   * @returns {Object} the instance of RootManager
   */
  static getInstance() {
    if (!RootManager.instance) {
      RootManager.instance = new RootManager();
    }
    return RootManager.instance;
  }
}

export default RootManager;
