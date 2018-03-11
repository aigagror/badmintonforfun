export abstract class HigherOrderComponent {
	constructor() {
		this.render = this.render.bind(this);
	}

	abstract render(): any;
}