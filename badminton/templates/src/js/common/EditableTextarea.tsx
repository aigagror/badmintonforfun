import * as React from 'react';


export class EditableTextarea extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			readonly: true,
			textValue: this.props.initValue,
		}
	}


	render() {
		return <textarea value={this.state.textValue} 
			onChange={(ev: any) => this.setState({textValue: ev.target.value})}
			readOnly={this.state.readonly}>

		</textarea>
	}
}