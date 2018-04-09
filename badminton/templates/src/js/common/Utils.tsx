export function objectToFormData(obj: any): FormData {
	const data = new FormData();
	for (let key of Object.keys(obj)) {
		data.append(key, obj[key]);
	}
	return data;
}