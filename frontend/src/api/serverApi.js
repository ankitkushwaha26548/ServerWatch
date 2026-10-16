import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.hostname}:8000`;



const api= axios.create({
    baseURL: API_URL

});

api.interceptors.request.use(
    (config) => {

        const token =
            localStorage.getItem(
                "access_token"
            );

        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }

        return config;
    }
);



export const getServers = async () => {
  try {
    const response = await api.get("/servers/");
    return response.data;
    } catch (error) {
    console.error("Error fetching servers:", error);
    throw error;
    }
};  

export const getServerMetrics = async (serverId) => {
    try {
        const response = await api.get(
            `/metrics/${serverId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching server metrics:", error);
        throw error;
    }
};

export const getMonitoredApis = async () => {
    const response = await api.get(
        "/api-monitor/"
    );

    return response.data;
};

export const checkApi = async (apiId) => {
    const response = await api.post(
        `/api-monitor/${apiId}/check`
    );

    return response.data;
};

export const getApiHistory = async (apiId) => {
    const response = await api.get(
        `/api-monitor/${apiId}/history`
    );

    return response.data;
};

export const getActiveAlerts = async () => {

    const response = await api.get(
        "/alerts/active"
    );

    return response.data;
};

export const getServerLogs = async (
    serverId,
    level = ""
) => {

    let url =
        `/logs/${serverId}`;

    if (level) {
        url += `?level=${encodeURIComponent(level)}`;
    }

    const response = await api.get(
        url
    );

    return response.data;
};

export const registerUser = async (
    userData
) => {

    const response = await api.post(
        `${API_URL}/auth/register`,
        userData
    );

    return response.data;
};

export const loginUser = async (
    userData
) => {

    const response = await api.post(
        `${API_URL}/auth/login`,
        userData
    );


    return response.data;
};


export const getDeployments = async () => {

    const response = await api.get(
        "/deployments/"
    );

    return response.data;
};

export const createDeployment = async (
    deploymentData
) => {

    const response = await api.post(
        "/deployments/",
        deploymentData
    );

    return response.data;
};

export const verifyEmail = async (token) => {
    const response = await api.get(
        `/auth/verify-email?token=${encodeURIComponent(token)}`
    );
    return response.data;
};
