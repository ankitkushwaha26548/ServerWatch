import { useEffect, useState } from "react";

import {
    getServerLogs
} from "../api/serverApi";


function LogViewer({ serverId }) {

    const [logs, setLogs] = useState([]);

    const [level, setLevel] = useState("");


    const loadLogs = async () => {

        try {

            const data =
                await getServerLogs(
                    serverId,
                    level
                );

            setLogs(data);

        } catch (error) {

            console.error(
                "Failed to load logs:",
                error
            );

        }
    };


    useEffect(() => {

        loadLogs();

    }, [serverId, level]);


    return (
        <div>

            <h2>
                Server Logs
            </h2>


            <div>

                <label>
                    Filter:
                </label>

                <select
                    value={level}
                    onChange={(event) =>
                        setLevel(
                            event.target.value
                        )
                    }
                >

                    <option value="">
                        All
                    </option>

                    <option value="INFO">
                        INFO
                    </option>

                    <option value="WARNING">
                        WARNING
                    </option>

                    <option value="ERROR">
                        ERROR
                    </option>

                </select>

            </div>


            <br />


            {logs.length === 0 ? (

                <p>
                    No logs found.
                </p>

            ) : (

                <table>

                    <thead>

                        <tr>

                            <th>
                                Time
                            </th>

                            <th>
                                Level
                            </th>

                            <th>
                                Source
                            </th>

                            <th>
                                Message
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {logs.map(
                            (log) => (

                                <tr
                                    key={log.id}
                                >

                                    <td>

                                        {new Date(
                                            log.timestamp
                                        ).toLocaleString()}

                                    </td>


                                    <td>

                                        {log.level === "ERROR"
                                            ? "🔴 ERROR"
                                            : log.level === "WARNING"
                                                ? "🟠 WARNING"
                                                : "🔵 INFO"
                                        }

                                    </td>


                                    <td>
                                        {log.source}
                                    </td>


                                    <td>
                                        {log.message}
                                    </td>

                                </tr>

                            )
                        )}

                    </tbody>

                </table>

            )}
        

        </div>
    );
}


export default LogViewer;