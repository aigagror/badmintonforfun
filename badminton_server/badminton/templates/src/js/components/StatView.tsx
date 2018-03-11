import * as React from "react";
import axios from 'axios';

const stat_urls = "/mock/stats.json"

export class StatView extends React.Component<{}, {}> {
	constructor(props: any) {
		super(props);
	}

	componentDidMount() {
		axios.get(stat_urls)
			.then((res: any) => {
				console.log(res);
			})
			.catch((res: any) => {
				console.log(res);
			});
	}

	render() {
		return <p>Hello!</p>
	}
}