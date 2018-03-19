import * as React from 'react';


export class RegisterElectionView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			clicked: false,
		}
	}

	render() {
		if (!this.state.clicked) {
			return <div>
				<button onClick={() => this.setState({clicked: true})}>
					Want to run? Click here!
				</button>
			</div>
		} else {
			return <div>

			<button onClick={() => this.setState({clicked: false})}>
					Want to run? Click here!
				</button>
			</div>
		}
	}
}