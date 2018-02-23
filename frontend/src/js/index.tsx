import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";

/* Keep these in here for the time being */
import '../sass/grid.scss';
import '../sass/style.scss';

ReactDOM.render(
    <Hello compiler="TypeScript" framework="React" />,
    document.getElementById("example")
);