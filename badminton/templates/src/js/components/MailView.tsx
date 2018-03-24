import * as React from "react";
import * as ReactDOM from 'react-dom';
import axios from 'axios';
import {getResource, setResource} from '../common/LocalResourceResolver';
import {Select} from '../common/Select';

const mail_list_url = '/mock/mail_lists.json'
const mail_data_location = 'mailData';

export class MailView extends React.Component<any, any> {

	private bodyElem: HTMLTextAreaElement;
	private titleElem: HTMLInputElement;
	private mailingList: any;

	constructor(props: any) {
		super(props);

		this.state = {
			lists: null,
		}
		this.sendMail = this.sendMail.bind(this);
		this.scoopData = this.scoopData.bind(this);
		this.setData = this.setData.bind(this);
		this.switch = this.switch.bind(this);
	}

	componentDidMount() {
		axios.get(mail_list_url)
			.then((res) => {
				this.setState({
					lists: res.data.lists,
				})

				this.mailingList = res.data.lists[0].value;

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

	switch(value: any) {
		this.mailingList = value;
	}

	scoopData() {
		const data = {
			list: this.mailingList,
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

		const selectData = this.state.lists.map((list: any, idx: number) => {
					return {
						value: list.key,
						display: list.name
					}
				});

		/* We don't want this to be a form so that we can type <return>
			Freely */
		return (<div className="mail-view grid">
			<div className="row row-offset-1">
			<div className="col-6 col-es-12">
			<Select 
				options={selectData}
				onChange={this.switch} 
	    		name="mailState" />
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