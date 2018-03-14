import * as React from "react";
import axios from 'axios';

declare var default_pic_url:string;

const bio_url = '/mock/bio.json'

export class ProfileView extends React.Component<any, any> {

	constructor(props: any) {
	    super(props);
	    this.state = {
	    	person: null,
	    }
	}

	componentDidMount() {
		axios.get(bio_url, {
			params: {
				member_id: this.props.member_id
			}
		})
		.then((res) => {
			this.setState({
				person: res.data
			})
		})
		.catch((res) => {
			console.log(res);
		})
	}


	render() {
		if (this.state.person === null) {
			return null
		}
		const person = this.state.person;
		var url = person.picture;
		if (url === null) {
			url = default_pic_url;
		}
		return <div className="profile-div">
			<div className="grid row row-8">
				<div className="col-6">
				<img className="profile-picture" src={url} alt="Profile picture" />
				</div>
				<div className="col-6">
				<h2>{person.name}</h2>
				<p>{person.bio}</p>
				</div>
			</div>
			</div>;
	}
}