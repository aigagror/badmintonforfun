import * as React from "react";
import * as ReactDOM from "react-dom";
import { GoogleLogin } from 'react-google-login';
import { Button } from "./components/Button";

const responseGoogle = (response) => {
  console.log(response);
}

ReactDOM.render(
    <GoogleLogin
	    clientId="613791656516-s7k2pbsbosa0c83o8omr0m1p1gp9q8vh.apps.googleusercontent.com"
	    buttonText="Login"
	    onSuccess={responseGoogle}
	    onFailure={responseGoogle}
	    disabled={false}
  	/>,
    document.querySelector("member-button")
);

ReactDOM.render(
    <Button text="Interested" href="/interested.html"/>,
    document.querySelector("interested-button")
);