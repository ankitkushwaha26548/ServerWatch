import { useEffect, useState } from "react";

import {
    getDeployments,
    createDeployment
} from "../api/serverApi";


function Deployments() {

    const [deployments, setDeployments] =
        useState([]);

    const [version, setVersion] =
        useState("");

    const [environment, setEnvironment] =
        useState("production");

    const [status, setStatus] =
        useState("SUCCESS");

    const [commitHash, setCommitHash] =
        useState("");

    const [error, setError] =
        useState("");


    const loadDeployments = async () => {

        try {

            const data =
                await getDeployments();

            setDeployments(data);

        } catch (error) {

            console.error(
                "Failed to load deployments:",
                error
            );

            setError(
                "Failed to load deployments"
            );
        }
    };


    useEffect(() => {

        loadDeployments();

    }, []);


    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        setError("");

        try {

            await createDeployment({
                version,
                environment,
                status,
                commit_hash: commitHash
            });

            setVersion("");
            setCommitHash("");

            await loadDeployments();

        } catch (error) {

            console.error(
                "Failed to create deployment:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to create deployment"
            );
        }
    };


    return (
        <div>

            <h1>
                Deployment History
            </h1>


            <form
                onSubmit={handleSubmit}
            >

                <div>

                    <label>
                        Version
                    </label>

                    <input
                        type="text"
                        placeholder="v1.3.0"
                        value={version}
                        onChange={(event) =>
                            setVersion(
                                event.target.value
                            )
                        }
                        required
                    />

                </div>


                <div>

                    <label>
                        Environment
                    </label>

                    <select
                        value={environment}
                        onChange={(event) =>
                            setEnvironment(
                                event.target.value
                            )
                        }
                    >

                        <option value="production">
                            Production
                        </option>

                        <option value="staging">
                            Staging
                        </option>

                        <option value="development">
                            Development
                        </option>

                    </select>

                </div>


                <div>

                    <label>
                        Status
                    </label>

                    <select
                        value={status}
                        onChange={(event) =>
                            setStatus(
                                event.target.value
                            )
                        }
                    >

                        <option value="SUCCESS">
                            SUCCESS
                        </option>

                        <option value="FAILED">
                            FAILED
                        </option>

                    </select>

                </div>


                <div>

                    <label>
                        Commit Hash
                    </label>

                    <input
                        type="text"
                        placeholder="a82f91c"
                        value={commitHash}
                        onChange={(event) =>
                            setCommitHash(
                                event.target.value
                            )
                        }
                        required
                    />

                </div>


                {error && (
                    <p>
                        {error}
                    </p>
                )}


                <button type="submit">
                    Record Deployment
                </button>

            </form>


            <hr />


            <table>

                <thead>

                    <tr>

                        <th>
                            Version
                        </th>

                        <th>
                            Environment
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Commit
                        </th>

                        <th>
                            Deployed At
                        </th>

                    </tr>

                </thead>


                <tbody>

                    {deployments.map(
                        (deployment) => (

                            <tr
                                key={
                                    deployment.id
                                }
                            >

                                <td>
                                    {
                                        deployment.version
                                    }
                                </td>

                                <td>
                                    {
                                        deployment.environment
                                    }
                                </td>

                                <td>
                                    {
                                        deployment.status
                                    }
                                </td>

                                <td>
                                    {
                                        deployment.commit_hash
                                    }
                                </td>

                                <td>
                                    {new Date(
                                        deployment.deployed_at
                                    ).toLocaleString()}
                                </td>

                            </tr>

                        )
                    )}

                </tbody>

            </table>

        </div>
    );
}


export default Deployments;