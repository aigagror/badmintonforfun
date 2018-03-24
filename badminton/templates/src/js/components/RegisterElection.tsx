import * as React from 'react';
import {Select, Option} from '../common/Select';
import {Popup} from '../common/Popup';

export class RegisterElectionView extends React.Component<any, any> {

	private openDiv: HTMLDivElement;

	private campaignType: string; 

	constructor(props: any) {
		super(props);
		this.change = this.change.bind(this);
		this.close = this.close.bind(this);
		this.submit = this.submit.bind(this);
		this._animationListener = this._animationListener.bind(this);
		this.state = {
			clicked: false,
			pitchValue: ''
		}
		this.campaignType = this.props.roles[0];
	}

	componentDidUpdate() {
		if (this.openDiv) {
			this.openDiv.addEventListener('animationend', () => 
				this.openDiv.scrollIntoView({behavior:"smooth"}));
		}
	}

	change() {
		this.setState({
			clicked: !this.state.clicked
		});
	}

	_animationListener() {
		this.openDiv.classList.remove('register-div-close');
		this.openDiv.removeEventListener('animationend', this._animationListener);
		this.change();
	}

	close() {
		this.openDiv.classList.add('register-div-close');
		this.openDiv.addEventListener('animationend', this._animationListener);
	}

	submit() {
		console.log("Pitch", this.state.pitchValue);
		console.log("State", this.campaignType);
		this.setState({
			popup: <Popup title="Campaign Submitted" 
				message="Election Campaign has been submitted"
				callback={()=>window.location.reload(true)} />
		})
	}

	render() {
		if (!this.state.clicked) {
			return <div>
				<button onClick={this.change}>
					Want to run? Click here!
				</button>
			</div>
		} else {
			const options = this.props.roles.map((role: string, idx: number) => new Option(role, role));
			return <>
			<div className="row-offset-2 register-div" ref={(input) => this.openDiv = input}>

			<h3>Register Election</h3>
			<textarea 
				placeholder="Your pitch goes here..."
				value={this.state.pitchValue}
				onChange={(ev)=>this.setState({pitchValue:ev.target.value})}>
			</textarea>

			<div className="row-offset-1">
			<Select 
			name='registerElection'
			onChange={(op: any) => {this.campaignType = op}}
			options={options} />
			</div>
			<div className="row-offset-1">
			<button onClick={this.close}>Close</button>
			</div>
			<div className="row-offset-1">
			<button onClick={this.submit}>Submit</button>
			</div>
			</div>
			{ this.state.popup && this.state.popup }
			</>
		}
	}
}