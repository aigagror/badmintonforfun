import * as React from "react";
import axios from 'axios';

const default_pic_url = "/assets/default_profile.png";

const bio_url = '/api/members/profile/';

export class ProfileView extends React.Component<any, any> {

	constructor(props: any) {
	    super(props);
	    this.state = {
	    	bio: null,
	    	name: null,
	    }
	}

	componentDidMount() {
		axios.get(bio_url, {
			params: {
				id: this.props.member_id
			}
		})
		.then((res) => {
			console.log(res.data);
			this.setState({
				bio: res.data.bio,
				name: res.data.first_name + ' ' + res.data.last_name
			})
		})
		.catch((res) => {
			console.log(res);
		})
	}


	render() {
		if (this.state.bio === null) {
			return null
		}
		var url = default_pic_url;
		if (url === null) {
			url = default_pic_url;
		}
		return <div className="profile-div">
			<div className="grid row row-8">
				<div className="col-6">
				<img className="profile-picture" src={url} alt="Profile picture" />
				</div>
				<div className="col-6">
				<h2>{this.state.name}</h2>
				<p>{this.state.bio}</p>
				</div>
			</div>
			</div>;
	}
}