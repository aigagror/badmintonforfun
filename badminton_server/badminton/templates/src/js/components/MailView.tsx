import * as React from "react";
import axios from 'axios';

const mail_list_url = '/mock/mail_lists.json'

export class MailView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			lists: null,
		}
		this.sendMail = this.sendMail.bind(this);
	}

	componentDidMount() {
		axios.get(mail_list_url)
			.then((res) => {
				this.setState({
					lists: res.data.lists,
				})
			})
			.catch((res) => {

			})
	}

	sendMail(event: any) {
		event.preventDefault();
		console.log("Pressed!");
	}

	render() {
		if (this.state.lists === null) {
			return <p>Loading</p>
		}

		/* We don't want this to be a form so that we can type <return>
			Freely */
		return (<div className="mail-view grid">
			<div className="row">
			<select id="mailId">
				{this.state.lists.map((list: any, idx: number) => {
					return <option value={list.key}>{list.name}</option>
				})}
			</select>
			</div>

			<div className="row">
			<input type="text" value="" placeholder="title" />
			</div>

			<div className="row">
			<textarea placeholder="body">
			</textarea>
			</div>

			<div className="row">
			<button type="submit" onClick={this.sendMail}>Submit</button>
			</div>
			</div>)
	}
}