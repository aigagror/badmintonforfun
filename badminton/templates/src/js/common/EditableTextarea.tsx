import * as React from 'react';


export class EditableTextarea extends React.Component<any, any> {

	private textarea: any;

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
		console.log(this.props.editableOverride);
		return <div className="editable-textarea-div">
		<textarea className={
			"editable-textarea interaction-style " + (this.state.readonly ? 
				"editable-textarea-frozen" : (this.props.defaultClass ? this.props.defaultClass : ""))}
			value={this.state.textValue} 
			onChange={(ev: any) => {
				const target = ev.target;
				target.style.height = target.scrollHeight+'px';
				this.setState({textValue: target.value}) ;
			}}
			ref={(ta: any) => this.textarea = ta}
			readOnly={this.state.readonly}>
		</textarea>
		{
			!this.props.editableOverride && 
			<>
			{ this.props.onDelete && <button 
				className="editable-textarea-delete-button interaction-style"
				onClick={this.props.onDelete}>
			X
			</button>
		}
		{
			this.state.readonly ?
			<button onClick={() => {
				this.textarea.style.height = '1px';
				this.textarea.style.height = this.textarea.scrollHeight+'px';
				this.setState({readonly:false})} 
			}
				className="editable-textarea-edit-button interaction-style">
				✎
			</button> :
			<button onClick={this.saveEdits} 
				className="editable-textarea-edit-button interaction-style">
				💾 
			</button>
		}
			</>
		}
		</div>
	}
}