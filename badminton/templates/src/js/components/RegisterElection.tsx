import * as React from 'react';


export class RegisterElectionView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.change = this.change.bind(this);
		this.state = {
			clicked: false,
		}
	}

	change() {
		this.setState({
			clicked: !this.state.clicked
		});
	}

	render() {
		if (!this.state.clicked) {
			return <div>
				<button onClick={this.change}>
					Want to run? Click here!
				</button>
			</div>
		} else {
			return <div className="row-offset-2 register-div">

			<h3>Register Election</h3>
			<textarea placeholder="Your pitch goes here...">
			</textarea>

			<div className="row-offset-1">
			<select>
			{
				this.props.roles.map((role: string, idx: number) => {
					return <option value={role} key={idx}>{role}</option>;
				})
			}
			</select>
			</div>
			<div className="row-offset-1">
			<button onClick={this.change}>Close</button>
			</div>
			<div className="row-offset-1">
			<button onClick={this.change}>Submit</button>
			</div>
			</div>
		}
	}
}