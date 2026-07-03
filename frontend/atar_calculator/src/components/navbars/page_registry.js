// Package Imports
import ManualCalculator from "../../pages/manual_calculator.js";
import AutomaticCalculator from "../../pages/automatic_calculator.js";
import MirrorMode from "../../pages/mirror_mode.js";

// Single source of truth for the app's page-name -> component mapping, and
// which page name is persisted across a refresh (there's no router yet, so
// the app re-renders the root manually — see RootManager).
export const PAGE_COMPONENTS = {
    'Manual': ManualCalculator,
    'Automatic': AutomaticCalculator,
    'Mirror Mode': MirrorMode,
};

export const DEFAULT_PAGE = 'Manual';
export const CURRENT_PAGE_STORAGE_KEY = 'atar_current_page';

/**
 * read the last-visited page name from localStorage, falling back to the default
 * @returns {string} a valid key of PAGE_COMPONENTS
 */
export function getPersistedPage() {
    const stored = localStorage.getItem(CURRENT_PAGE_STORAGE_KEY);
    return PAGE_COMPONENTS[stored] ? stored : DEFAULT_PAGE;
}

/**
 * persist the given page name so it survives a refresh
 * @param {string} pageName one of PAGE_COMPONENTS' keys
 */
export function setPersistedPage(pageName) {
    localStorage.setItem(CURRENT_PAGE_STORAGE_KEY, pageName);
}
