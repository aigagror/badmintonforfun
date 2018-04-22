export function objectToFormData(obj: any): FormData {
	const data = new FormData();
	for (let key of Object.keys(obj)) {
		var serial = obj[key];
		if (typeof serial === 'object') {
			serial = JSON.stringify(obj[key]);
		}
		data.append(key, serial);
	}
	return data;
}