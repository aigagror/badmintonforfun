import * as React from 'react';

export class Popup extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.state = {
			popup: false,
		}
	}

	close() {
		this.setState({
			popup: false,
		});
		this.props.callback();
	}

	popup() {
		this.setState({
			popup: true,
		});
	}

	render() {
		if (this.state.popup) {
			return (<div></div>);
		} else {
			return (<div className="message-div">
	    			<h4>{this.props.title}</h4>
	    			<p>{this.props.message}</p>
	    			<button onClick={this.close}>Ok</button>
	    		</div>)
		}
	}
}