import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import ServerDetails from "./pages/ServerDetails";
import Login from "./pages/Login"
import ProtectedRoute from "./components/ProtectedRoute";
import DeploymentsPage from "./pages/DeploymentsPage";



function App() {

    return (
        <BrowserRouter>
            <Routes>                
                <Route path="/login" element={<Login />} />
                <Route path="/" element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                } />
                <Route path="/server/:serverId" element={
                    <ProtectedRoute>
                        <ServerDetails />
                    </ProtectedRoute>
                } />
                <Route path="/deployments" element={
                    <ProtectedRoute>
                        <DeploymentsPage />
                    </ProtectedRoute>
                } />
            
            </Routes>
        </BrowserRouter>
    );
}

export default App;