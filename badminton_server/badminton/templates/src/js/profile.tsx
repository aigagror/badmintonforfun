import * as React from "react";
import * as ReactDOM from "react-dom";

import { ProfileView } from "./components/ProfileView";

declare var member_id:number;

ReactDOM.render(
    <ProfileView member_id={member_id} />,
    document.querySelector("profile-view")
);
