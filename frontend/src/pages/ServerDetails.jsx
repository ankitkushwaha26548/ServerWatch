import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import PerformanceChart from "../components/PerformanceChart";
import { formatUptime } from "../utils/formateUptime";


import { getServers, getServerMetrics } from "../api/serverApi";
import {createWebSocket} from "../api/websocket";


function ServerDetails() {

    const { serverId } = useParams();

    const [server, setServer] = useState(null);
    const [metrics, setMetrics] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {

        loadServerDetails();

    }, [serverId]);

    useEffect(() => {

    const socket = createWebSocket(
        (data) => {

            if (
                data.type === "metric_update" &&
                data.server_id === Number(serverId)
            ) {

                setMetrics((previousMetrics) => {

                    return [
                        data.metric,
                        ...previousMetrics
                    ].slice(0, 100);

                });

            }

        }
    );


    return () => {

        socket.close();

    };

}, [serverId]);

    const loadServerDetails = async () => {

        try {

            const servers = await getServers();

            const selectedServer = servers.find(
                (server) =>
                    server.id === Number(serverId)
            );


            if (!selectedServer) {

                setError("Server not found.");

                return;

            }


            setServer(selectedServer);


            const serverMetrics =
                await getServerMetrics(
                    Number(serverId)
                );


            setMetrics(serverMetrics);

        } catch (error) {

            console.error(error);

            setError(
                "Unable to load server details."
            );

        } finally {

            setLoading(false);

        }
    };


    if (loading) {

        return (
            <h2>
                Loading server details...
            </h2>
        );

    }


    if (error) {

        return (
            <div>

                <h2>
                    {error}
                </h2>

                <Link to="/">
                    Back to Dashboard
                </Link>

            </div>
        );

    }


    if (!server) {

        return (
            <h2>
                Server not found.
            </h2>
        );

    }


    const latestMetric =
        metrics.length > 0
            ? metrics[0]
            : null;


    return (

        <div>

            <Link to="/">
                ← Back to Dashboard
            </Link>


            <h1>
                {server.name}
            </h1>


            <p>
                Status: {server.status}
            </p>


            <p>
                Hostname: {server.hostname}
            </p>


            <p>
                IP Address: {server.ip_address}
            </p>


            <p>
                Operating System:
                {" "}
                {server.operating_system}
            </p>


            <h2>
                Current Performance
            </h2>


            {latestMetric ? (

                <div>

                    <p>
                        CPU:
                        {" "}
                        {latestMetric.cpu_usage}%
                    </p>

                    <p>
                        Memory:
                        {" "}
                        {latestMetric.memory_usage}%
                    </p>

                    <p>
                        Disk:
                        {" "}
                        {latestMetric.disk_usage}%
                    </p>

                    <p>
                        Network Sent:
                        {" "}
                        {latestMetric.network_sent_mb}
                        {" "}MB
                    </p>

                    <p>
                        Network Received:
                        {" "}
                        {latestMetric.network_received_mb}
                        {" "}MB
                    </p>

                    <p>
    Uptime:
    {" "}
    {formatUptime(
        latestMetric.uptime_seconds
    )}
</p>
                </div>

            ) : (

                <p>
                    No monitoring data available.
                </p>

            )}


            <h2>
                Metric History
            </h2>
            {metrics.length > 0 && (

    <div>

        <h2>
            Performance History
        </h2>

        <PerformanceChart
            metrics={metrics}
        />

    </div>

)}

            {metrics.length === 0 ? (

                <p>
                    No historical metrics available.
                </p>

            ) : (

                <table>

                    <thead>

                        <tr>

                            <th>
                                Time
                            </th>

                            <th>
                                CPU
                            </th>

                            <th>
                                Memory
                            </th>

                            <th>
                                Disk
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {metrics.map((metric) => (

                            <tr key={metric.id}>

                                <td>
                                    {new Date(
                                        metric.timestamp
                                    ).toLocaleTimeString()}
                                </td>

                                <td>
                                    {metric.cpu_usage}%
                                </td>

                                <td>
                                    {metric.memory_usage}%
                                </td>

                                <td>
                                    {metric.disk_usage}%
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            )}

        </div>

    );
}


export default ServerDetails;