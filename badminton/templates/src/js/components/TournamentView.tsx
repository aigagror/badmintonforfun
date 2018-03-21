import * as React from "react";
import axios from 'axios';
import * as Konva from "konva";
import { Stage, Layer, Rect, Text, Line } from "react-konva";

const tourney_url = '/mock/tournament.json';

const columnWidth = 160;
const rowHeight = 40;
const rowSpacing = 10;
const colSpacing = 50;
const lazyHack =10000000;

const calcX = (col: number) => (columnWidth+colSpacing)*col;
const calcY = (col: number, row: number, maxCols: number): number => {
	if(col === 0) {
		return (rowHeight+rowSpacing)*row + col * ((rowHeight+rowSpacing)/2)
	}

	const numBlocksCenter = Math.pow(2, col);
	const ytop = calcY(0, row*numBlocksCenter, maxCols);
	const ybot = calcY(0, (row+1)*numBlocksCenter-1, maxCols) + rowHeight;

	return (ytop + ybot - rowHeight) / 2;
}

class Matchup extends React.Component<any, any> {


	render() {

		var extra;
		const opts = {
			stroke: "white",
			strokeWidth: 1.25,
			padding: 4,
		}

		if (this.props.data.state === "undecided") {
			extra = <Text text="TBA" {...opts} x={this.props.x} y={this.props.y} height={rowHeight} width={columnWidth} align="center" />
		}
		else if (this.props.data.state === "decided") {
			extra = <>
				<Text text={this.props.data.team1} {...opts} x={this.props.x} y={this.props.y}/>
				<Text text={this.props.data.team2} {...opts} x={this.props.x} y={this.props.y+rowHeight/2}/>
				</>
		} else {
			const convert = (num: number): string => {
				if (num < 10) {
					return "0" + num;
				}

				return "" + num;
			}
			extra = <>
				<Text text={this.props.data.team1} {...opts} x={this.props.x} y={this.props.y}/>
				<Text text={this.props.data.team2} {...opts} x={this.props.x} y={this.props.y+rowHeight/2}/>
				<Text text={convert(this.props.data.team1_score)} {...opts} x={this.props.x+columnWidth-25} y={this.props.y}/>
				<Text text={convert(this.props.data.team2_score)} {...opts} x={this.props.x+columnWidth-25} y={this.props.y+rowHeight/2}/>
				</>
		}
		return (
			<>
		  <Rect
			x={this.props.x}
			y={this.props.y}
			width={columnWidth}
			height={rowHeight}
			fill={"black"}
			shadowEnabled={false}
			cornerRadius={3}
		  />
		  {extra}
		  </>
		);
	}
}

function height(matchups: any): number {
	if (matchups === null) {
		return 0;
	}

	let hgt = Math.max(height(matchups.feeder_lhs), 
		height(matchups.feeder_rhs)) + 1;
	return hgt;
}

class TournamentCell extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.agglomerateData = this.agglomerateData.bind(this);
		this._merge = this._merge.bind(this);
	}

	_merge(aggCall: any, toX: number, toY: number) {
		let [othElems, [othX, othY]] = aggCall;
		const offsetX = 6;
		const midX = othX + columnWidth+offsetX;
		var midY = othY + rowHeight / 2;

		const halfX = midX + colSpacing / 2;
		const offsetY = 9;
		if (toY < midY) {
			toY += offsetY;
		} else {
			toY -= offsetY;
		}
		return [<Line stroke="black" strokeWidth={3} points={[midX, midY, halfX, midY, halfX, toY, toX-offsetX, toY]} />, ...othElems]
	}



	agglomerateData(data: any, row: number, col: number, maxCols: number): any {
		//elements, root
		if (data === null) {
			return [];
		}
		let {feeder_lhs, feeder_rhs, ...rest} = data;
		const x = calcX(col);
		const y = calcY(col, row, maxCols);
		var elems = [<Matchup x={x} y={y} data={rest}/>];
		const entry = y + rowHeight / 2;

		if (data.feeder_lhs !== null) {
			const accumulated = this._merge(this.agglomerateData(data.feeder_lhs, row*2, col-1, maxCols), x, entry);
			elems = elems.concat(accumulated);
		}
		if (data.feeder_rhs !== null) {
			const accumulated = this._merge(this.agglomerateData(data.feeder_rhs, row*2+1, col-1, maxCols), x, entry);
			elems = elems.concat(accumulated);
		}
		return [elems, [x, y]];
	}


	render() {
		const maxHeight = height(this.props.matches);
		let [elems, ...rest] = this.agglomerateData(this.props.matches, 0, maxHeight-1, maxHeight);
		return <Stage width={window.innerWidth} height={window.innerHeight}>
				<Layer>
					{
						elems
					}
				</Layer>
			  </Stage>
	}
}

export class TournamentView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			matches: null,
		}
	}

	componentDidMount() {
		axios.get(tourney_url)
			.then((res) => {
				this.setState({
					matches: res.data.matches,
				})
			})
			.catch((res) => {

			})
	}
	render() {
		if (this.state.matches === null) {
			return null;
		}
		return (
			<div className="tournament-div">
			<TournamentCell matches={this.state.matches} />
			</div>);
	}
}