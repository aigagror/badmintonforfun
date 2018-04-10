import * as React from "react";
import * as ReactDOM from 'react-dom';
import axios from 'axios';
import {getResource, setResource, xsrfCookieName, xsrfHeaderName, getMemberId} from '../common/LocalResourceResolver';
import {Select} from '../common/Select';
import {objectToFormData} from '../common/Utils';
import { Popup } from '../common/Popup';

axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();

const mail_list_url = '/api/mail/'
const mail_data_location = 'mailData';

export class MailView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			lists: null,
			bodyText: "",
			titleText: "",
			mailingList: "",
			popup: null,
		}
		this.sendMail = this.sendMail.bind(this);
		this.scoopData = this.scoopData.bind(this);
		this.setData = this.setData.bind(this);
		this.switch = this.switch.bind(this);
		this.resetState = this.resetState.bind(this);
	}

	async componentDidMount() {
		try {
			const res = await axios.get(mail_list_url);
			this.setState({
				lists: res.data,
				mailingList: res.data[0].value,
			})

			const item = getResource(this, mail_data_location);

			if (item !== null) {
				this.setData(JSON.parse(item));
			}

			window.setInterval(() => {
				setResource(this, mail_data_location, JSON.stringify(this.scoopData()));
			}, 5000);
		} catch (err) {
			console.log(err);
		}
	}

	switch(value: any) {
		this.setState({
			mailingList: value
		});
	}

	scoopData() {
		const data = {
			mailing_list: this.state.mailingList,
			title: this.state.titleText,
			body: this.state.bodyText
		};
		return data;
	}

	setData(data: any) {
		this.setState({
			titleText: data.title,
			bodyText: data.body,
			mailingList: data.list,
		})
	}

	resetState() {
		this.setState({
			popup: null
		});
	}


	async sendMail(event: any) {
		event.preventDefault();
		const data = this.scoopData();
		try {
			await axios.post(mail_list_url, objectToFormData(data));
			this.setState({
				titleText: "",
				bodyText: "",
				popup: <Popup title="Success" message="Massmail will be incrementally sent"
					callback={this.resetState}/>,
			})
		} catch (err) {
			this.setState({
				popup: <Popup title="Sorry!" message="There was an error on our end, please check back soon"
					callback={this.resetState}/>,
			})
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
			{ this.state.popup !== null && this.state.popup }
			</div>)
	}
}