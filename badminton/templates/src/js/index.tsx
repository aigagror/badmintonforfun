import * as React from "react";
import * as ReactDOM from "react-dom";
import { GoogleAuthButton } from './components/GoogleAuthButton';

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
    <button className="interaction-style" onClick={()=>{window.location.href = "./interested.html"}}>Interested</button>,
    document.querySelector("interested-button")
);