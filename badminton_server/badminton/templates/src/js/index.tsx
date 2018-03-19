import * as React from "react";
import * as ReactDOM from "react-dom";
import { GoogleAuthButton } from './components/GoogleAuthButton';
import { Button } from "./components/Button";

const responseGoogle = (response: any) => {
  console.log(response);
}

const failureGoogle = (response: any) => {
  
}

ReactDOM.render(
    <GoogleAuthButton 
      onSuccess={responseGoogle}
      onFailure={failureGoogle}
     />,
    document.querySelector("member-button")
);

ReactDOM.render(
    <Button text="Interested" href="./interested.html"/>,
    document.querySelector("interested-button")
);