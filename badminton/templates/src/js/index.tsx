import * as React from "react";
import * as ReactDOM from "react-dom";

ReactDOM.render(
    <button className="interaction-style" onClick={()=>{window.location.href = "/login"}}>Sign In</button>,
    document.querySelector("member-button")
);

ReactDOM.render(
    <button className="interaction-style" onClick={()=>{window.location.href = "./interested.html"}}>Interested</button>,
    document.querySelector("interested-button")
);