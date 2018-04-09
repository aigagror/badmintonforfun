import * as React from "react";
import * as ReactDOM from "react-dom";
import { GoogleAuthButton } from './components/GoogleAuthButton';

const responseGoogle = (response: any) => {
  console.log(response);
}

const failureGoogle = (response: any) => {
  
}

ReactDOM.render(
    <button className="interaction-style" onClick={()=>{window.location.href = "/sign_in"}}>Sign In</button>,
    document.querySelector("member-button")
);

ReactDOM.render(
    <button className="interaction-style" onClick={()=>{window.location.href = "./interested.html"}}>Interested</button>,
    document.querySelector("interested-button")
);