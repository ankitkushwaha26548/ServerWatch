import { useState } from "react";

import { useNavigate } from "react-router-dom";

import {
    loginUser
} from "../api/serverApi";


function Login() {

    const navigate = useNavigate();

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");


    const handleLogin = async (
        event
    ) => {

        event.preventDefault();

        setError("");


        try {

            const data =
                await loginUser({
                    email,
                    password
                });


            localStorage.setItem(
                "access_token",
                data.access_token
            );


            navigate("/");

        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Login failed"
            );

        }
    };


    return (
        <div>

            <h1>
                ServerWatch Login
            </h1>


            <form
                onSubmit={handleLogin}
            >

                <div>

                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) =>
                            setEmail(
                                event.target.value
                            )
                        }
                        required
                    />

                </div>


                <div>

                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event) =>
                            setPassword(
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

                    Login

                </button>

            </form>

        </div>
    );
}


export default Login;