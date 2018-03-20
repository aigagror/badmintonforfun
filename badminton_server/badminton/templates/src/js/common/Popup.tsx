import * as React from 'react';

export class Popup extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.state = {
			popup: false,
		}
		this.close = this.close.bind(this);
	}

	close() {
		this.setState({
			popup: true,
		});
		this.props.callback();
	}

	render() {
		if (this.state.popup) {
			return null;
		} else {
			return (<div className="popup-div">
						<div className="grid row">
						<div className="row-1">
						<div className="col-11 popup-title-div">
			    			<h4 className="popup-title">{this.props.title}</h4>
			    		</div>
			    		</div>
			    		<div className="row-1">
			    		<div className="col-offset-1 col-11">
			    			<p className="popup-message">{this.props.message}</p>
			    		</div>
			    		</div>
			    		<div className="row-offset-10">
			    		<div className="col-offset-es-9 col-es-5 row-offset-es-9 col-offset-9 row-offset-11">
			    			<button className="popup-button row-2" onClick={this.close}>✔</button>
			    		</div>
		    			</div>
		    			</div>
		    		</div>)
		}
	}
}