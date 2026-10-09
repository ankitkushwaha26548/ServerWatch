import { useEffect, useState } from "react";

import {
    getMonitoredApis,
    checkApi
} from "../api/serverApi";


function ApiMonitor() {

    const [apis, setApis] = useState([]);
    const [loading, setLoading] = useState(true);


    const loadApis = async () => {

        try {

            const data = await getMonitoredApis();

            setApis(data);

        } catch (error) {

            console.error(
                "Failed to load APIs:",
                error
            );

        } finally {

            setLoading(false);

        }
    };


    const handleCheck = async (apiId) => {

        try {

            await checkApi(apiId);

            await loadApis();

        } catch (error) {

            console.error(
                "API check failed:",
                error
            );

        }
    };


    useEffect(() => {

        loadApis();

    }, []);


    if (loading) {
        return <p>Loading APIs...</p>;
    }


    return (
        <div>

            <h2>
                API Services
            </h2>


            {apis.length === 0 ? (

                <p>
                    No APIs are being monitored.
                </p>

            ) : (

                <table>

                    <thead>

                        <tr>

                            <th>
                                Name
                            </th>

                            <th>
                                Status
                            </th>

                            <th>
                                Status Code
                            </th>

                            <th>
                                Response Time
                            </th>

                            <th>
                                Action
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {apis.map((api) => (

                            <tr key={api.id}>

                                <td>
                                    {api.name}
                                </td>


                                <td>

                                    {api.status === "healthy"
                                        ? "🟢 Healthy"
                                        : api.status === "unhealthy"
                                            ? "🟠 Unhealthy"
                                            : api.status === "down"
                                                ? "🔴 Down"
                                                : "⚪ Unknown"
                                    }

                                </td>


                                <td>
                                    {api.last_status_code ?? "---"}
                                </td>


                                <td>
                                    {api.last_response_time !== null
                                        ? `${api.last_response_time} ms`
                                        : "---"
                                    }
                                </td>


                                <td>

                                    <button
                                        onClick={() =>
                                            handleCheck(api.id)
                                        }
                                    >
                                        Check Now
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            )}

        </div>
    );
}


export default ApiMonitor;