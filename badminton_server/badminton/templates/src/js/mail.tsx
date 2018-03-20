import * as React from "react";
import * as ReactDOM from "react-dom";

import { MailView } from "./components/MailView";

ReactDOM.render(
    <MailView />,
    document.querySelector("mail-form")
);