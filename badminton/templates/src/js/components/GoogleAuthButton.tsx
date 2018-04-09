import * as React from 'react';
import { GoogleLogin } from 'react-google-login';

export interface GoogleAuthProps {
	onSuccess: (obj: any) => void;
	onFailure: (obj: any) => void;
	text?: string;
}

export class GoogleAuthButton extends React.Component<GoogleAuthProps, {}> {

	render() {
		return <GoogleLogin
			      clientId="613791656516-s7k2pbsbosa0c83o8omr0m1p1gp9q8vh.apps.googleusercontent.com"
			      buttonText={this.props.text ? this.props.text : "Login"}
			      onSuccess={this.props.onSuccess}
			      onFailure={this.props.onFailure}
			      disabled={false}
			      className="login-button interaction-style"
			    />
	}
}