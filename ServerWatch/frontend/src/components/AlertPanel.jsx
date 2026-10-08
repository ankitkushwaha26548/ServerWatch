import { useEffect, useState } from "react";

import {
    getActiveAlerts
} from "../api/serverApi";


function AlertPanel() {

    const [alerts, setAlerts] = useState([]);


    const loadAlerts = async () => {

        try {

            const data =
                await getActiveAlerts();

            setAlerts(data);

        } catch (error) {

            console.error(
                "Failed to load alerts:",
                error
            );

        }
    };


    useEffect(() => {

        loadAlerts();

        const interval =
            setInterval(
                loadAlerts,
                10000
            );

        return () => {
            clearInterval(interval);
        };

    }, []);


    return (
        <div>

            <h2>
                Active Alerts
            </h2>


            {alerts.length === 0 ? (

                <p>
                    🟢 No active alerts
                </p>

            ) : (

                <div>

                    {alerts.map(
                        (alert) => (

                            <div
                                key={alert.id}
                            >

                                <strong>

                                    {alert.severity ===
                                    "critical"
                                        ? "🔴"
                                        : "🟠"}

                                    {" "}

                                    {alert.message}

                                </strong>

                                <p>

                                    Type:
                                    {" "}
                                    {alert.alert_type}

                                </p>

                                <p>

                                    Created:
                                    {" "}
                                    {new Date(
                                        alert.created_at
                                    ).toLocaleString()}

                                </p>

                            </div>

                        )
                    )}

                </div>

            )}

        </div>
    );
}


export default AlertPanel;