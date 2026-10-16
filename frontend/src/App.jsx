import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import ServerDetails from "./pages/ServerDetails";
import Login from "./pages/Login"
import Register from "./pages/Register";
import VerifyEmail from "./pages/VerifyEmail";
import ProtectedRoute from "./components/ProtectedRoute";
import DeploymentsPage from "./pages/DeploymentsPage";



function App() {

    return (
        <BrowserRouter>
            <Routes>                
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/verify-email" element={<VerifyEmail />} />
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
                <Route path="*" element={<Navigate to="/" replace />} />
            
            </Routes>
        </BrowserRouter>
    );
}

export default App;
