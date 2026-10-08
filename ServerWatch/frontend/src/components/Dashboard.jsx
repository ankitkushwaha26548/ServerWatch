import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ApiMonitor from "./ApiMonitor";
import AlertPanel from "./AlertPanel";

import { getServers, getServerMetrics } from "../api/serverApi";
import { logout } from "../api/auth";


function Dashboard() {

    const [servers, setServers] = useState([]);
    const [metrics, setMetrics] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {

        loadDashboard();

    }, []);


    const loadDashboard = async () => {

        try {

            const serverData = await getServers();

            setServers(serverData);


            const metricsData = {};


            for (const server of serverData) {

                const serverMetrics =
                    await getServerMetrics(server.id);


                if (serverMetrics.length > 0) {

                    metricsData[server.id] =
                        serverMetrics[0];

                }

            }


            setMetrics(metricsData);

        } catch (error) {

            console.error(error);

            setError(
                "Unable to load dashboard data."
            );

        } finally {

            setLoading(false);

        }
    };


    if (loading) {

        return (
            <h2>
                Loading ServerWatch...
            </h2>
        );

    }


    if (error) {

        return (
            <h2>
                {error}
            </h2>
        );

    }
    const totalServers = servers.length;

    const onlineServers = servers.filter(
        (server) => server.status === "online"
    ).length;

    const offlineServers =
        totalServers - onlineServers;

    return (

        <div>

            <h1>
                ServerWatch
            </h1>
            <div>

    <h3>
        Total Servers: {totalServers}
    </h3>

    <h3>
        Online: {onlineServers}
    </h3>

    <h3>
        Offline: {offlineServers}
    </h3>

</div>
<button
    onClick={logout}
>
    Logout
</button>
            <p>
                Mini DevOps Control Center
            </p>


            <h2>
                Servers
            </h2>


            {servers.length === 0 ? (

                <p>
                    No servers found.
                </p>

            ) : (

                servers.map((server) => {

                    const metric =
                        metrics[server.id];


                    return (

                        <div key={server.id}>

                            <h3>
                                <Link to={`/server/${server.id}`}>
        {server.name}
    </Link>

                            </h3>


                            <p>
                                Status:
                                {" "}
                                {server.status}
                            </p>


                            <p>
                                Hostname:
                                {" "}
                                {server.hostname}
                            </p>


                            <p>
                                IP:
                                {" "}
                                {server.ip_address}
                            </p>


                            {metric ? (

                                <div>

                                    <p>
                                        CPU:
                                        {" "}
                                        {metric.cpu_usage}%
                                    </p>

                                    <p>
                                        Memory:
                                        {" "}
                                        {metric.memory_usage}%
                                    </p>

                                    <p>
                                        Disk:
                                        {" "}
                                        {metric.disk_usage}%
                                    </p>

                                </div>

                            ) : (

                                <p>
                                    No metrics available.
                                </p>

                            )}
                            
                            <hr />

                            <AlertPanel />
                            
                            {/* API monitoring */}  
                            <ApiMonitor />
                            <Link to="/deployments">
                                 Deployment History
                            </Link>

                        </div>

                    );

                })

            )}

        </div>

    );
}


export default Dashboard;