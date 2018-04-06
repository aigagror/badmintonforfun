import * as React from 'react';


export class EditableTextarea extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			readonly: true,
			textValue: this.props.initValue,
		}
		this.saveEdits = this.saveEdits.bind(this);
	}

	saveEdits() {
		this.props.onSave(this.state.textValue);
		this.setState({
			readonly: true,
		})
	}


	render() {
		return <div className="editable-textarea-div">
		<textarea className={this.state.readonly ? 
				"editable-textarea-frozen" : (this.props.defaultClass ? this.props.defaultClass : "")}
			value={this.state.textValue} 
			onChange={(ev: any) => this.setState({textValue: ev.target.value})}
			readOnly={this.state.readonly}>
		</textarea>
		{
			this.state.readonly ?
			<button onClick={() => this.setState({readonly:false})} 
				className="editable-textarea-edit-button">
				Edit
			</button> :
			<>
			<button onClick={this.saveEdits} 
				className="editable-textarea-edit-button">
				Save
			</button>
			</>
		}
		</div>
	}
}