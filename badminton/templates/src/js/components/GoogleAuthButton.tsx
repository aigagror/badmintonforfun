import * as React from 'react';
import { GoogleLogin } from 'react-google-login';

export class GoogleAuthButton extends React.Component<any, any> {

	render() {
		return <GoogleLogin
			      clientId="613791656516-s7k2pbsbosa0c83o8omr0m1p1gp9q8vh.apps.googleusercontent.com"
			      buttonText="Login"
			      onSuccess={this.props.onSuccess}
			      onFailure={this.props.onFailure}
			      disabled={false}
			      className="login-button"
			    />
	}
}