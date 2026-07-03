// Package Imports
// import Login  from "./pages/login.js";
import { PAGE_COMPONENTS, getPersistedPage } from "./components/navbars/page_registry.js";

// CSS Imports
import './styles/App.css';

function App() {
  // NOTE: the app has no router yet; page switching is handled by the navbar's
  // dropdown re-rendering the root (see RootManager). The Login page is unused
  // (see README). The last-visited page is persisted in localStorage so a
  // refresh doesn't bounce the user back to the default page.
  const CurrentPage = PAGE_COMPONENTS[getPersistedPage()];
  return (
    <div id="app-container">
      <CurrentPage />
    </div>
  );
}


export default App;
