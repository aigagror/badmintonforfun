import * as React from "react";
import * as ReactDOM from 'react-dom';
import axios from 'axios';
import {getResource, setResource} from '../common/LocalResourceResolver';
import {Select} from '../common/Select';
import {objectToFormData} from '../common/Utils';

const mail_list_url = '/api/mail/'
const mail_data_location = 'mailData';

export class MailView extends React.Component<any, any> {

	private mailingList: any;

	constructor(props: any) {
		super(props);

		this.state = {
			lists: null,
			bodyText: "",
			titleText: ""
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
			mailing_list: this.mailingList,
			title: this.state.titleText,
			body: this.state.bodyText
		};
		return data;
	}

	setData(data: any) {
		this.setState({
			titleText: data.title,
			bodyText: data.body
		})
		this.mailingList.value = data.list;
	}


	async sendMail(event: any) {
		event.preventDefault();
		const data = this.scoopData();
		console.log("Hello!");
		try {
			await axios.post(mail_list_url, objectToFormData(data));

		} catch (err) {
			console.log(err)
		}
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
				value={this.state.titleText}
				onChange={(ev: any) => this.setState({titleText: ev.target.value})}
				className="mail-title interaction-style"/>
			</div>
			</div>

			<div className="row row-offset-1">
			<div className="col-12">
			<textarea placeholder="Body" 
				value={this.state.bodyText}
				onChange={(ev: any) => this.setState({bodyText: ev.target.value})}
				className="mail-body interaction-style">
			</textarea>
			</div>
			</div>

			<div className="row row-offset-1">
			<div className="col-4">
				<button 
					type="submit" 
					onClick={this.sendMail} 
					className="interaction-style">Submit</button>
			</div>
			</div>
			</div>)
	}
}