import * as React from "react";
import * as ReactDOM from 'react-dom';
import axios from 'axios';
import {getResource, setResource} from '../common/LocalResourceResolver';

const mail_list_url = '/mock/mail_lists.json'
const mail_data_location = 'mailData';

export class MailView extends React.Component<any, any> {

	private mailingList: HTMLSelectElement;
	private bodyElem: HTMLTextAreaElement;
	private titleElem: HTMLInputElement;

	constructor(props: any) {
		super(props);

		this.state = {
			lists: null,
		}
		this.sendMail = this.sendMail.bind(this);
		this.scoopData = this.scoopData.bind(this);
		this.setData = this.setData.bind(this);
	}

	componentDidMount() {
		axios.get(mail_list_url)
			.then((res) => {
				this.setState({
					lists: res.data.lists,
				})

				const item = getResource(this, mail_data_location);

				if (item !== null) {
					this.setData(JSON.parse(item));
				}

				window.setInterval(() => {
					setResource(this, mail_data_location, JSON.stringify(this.scoopData()));
				}, 5000);
			})
			.catch((res) => {

			})
	}

	scoopData() {
		const data = {
			list: this.mailingList.value,
			title: this.titleElem.value,
			body: this.bodyElem.value
		};
		return data;
	}

	setData(data: any) {
		this.mailingList.value = data.list;
		this.titleElem.value = data.title;
		this.bodyElem.value = data.body;
	}


	sendMail(event: any) {
		event.preventDefault();
		const data = this.scoopData();
		console.log(data);
	}


	render() {
		if (this.state.lists === null) {
			return <p>Loading</p>
		}

		/* We don't want this to be a form so that we can type <return>
			Freely */
		return (<div className="mail-view grid">
			<div className="row row-offset-1">
			<div className="col-6">
			<select id="mailId" ref={(input) => { this.mailingList = input; }}>
				{this.state.lists.map((list: any, idx: number) => {
					return <option value={list.key} key={idx}>{list.name}</option>
				})}
			</select>
			</div>
			</div>

			<div className="row row-offset-1">
			<div className="col-8">
			<input type="text" placeholder="Title" 
				ref={(input) => { this.titleElem = input; }}
				className="mail-title"/>
			</div>
			</div>

			<div className="row row-offset-1">
			<div className="col-12">
			<textarea placeholder="Body" 
				ref={(input) => { this.bodyElem = input; }}
				className="mail-body">
			</textarea>
			</div>
			</div>

			<div className="row row-offset-1">
			<div className="col-4">
			<button type="submit" onClick={this.sendMail}>Submit</button>
			</div>
			</div>
			</div>)
	}
}