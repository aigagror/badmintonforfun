import * as React from 'react';

export class Popup extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.state = {
			popup: false,
		}
		this.close = this.close.bind(this);
		this.popup = this.popup.bind(this);
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
			return null;
		} else {
			return (<div className="popup-div">
	    			<h4 className="popup-title">{this.props.title}</h4>
	    			<p className="popup-message">{this.props.message}</p>
	    			<button className="popup-button" onClick={this.close}>Ok</button>
	    		</div>)
		}
	}
}