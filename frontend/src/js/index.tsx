import * as React from "react";
import * as ReactDOM from "react-dom";

import { Button } from "./components/Button";

ReactDOM.render(
    <Button text="Members" href="/members.html"/>,
    document.querySelector("member-button")
);

ReactDOM.render(
    <Button text="Interested" href="/interested.html"/>,
    document.querySelector("interested-button")
);