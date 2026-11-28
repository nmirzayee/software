export default {
	// Student Assignment Organizer – Appsmith JSObject "AssignmentLogic"
	// Same rules, order and messages as the Python version (main.py v1.1).
	MAX_COURSE: 30,
	MAX_TITLE: 80,
	SUCCESS: "Assignment successfully added!",

	// count Unicode code points (Python len()), not UTF-16 units
	len(text) {
		return [...text].length;
	},

	// strip + NFC + reject control/format characters (Python _normalize)
	normalize(value, label) {
		if (typeof value !== "string") {
			throw new Error(label + " must be text.");
		}
		const v = value.trim().normalize("NFC");
		if (/[\p{Cc}\p{Cf}]/u.test(v)) {
			throw new Error(label + " contains unsupported control characters.");
		}
		return v;
	},

	// input validation – returns {course, title} or throws Error(message)
	validate(course, title, list) {
		const c = this.normalize(course, "Course name");
		const t = this.normalize(title, "Assignment title");
		if (this.len(c) === 0) throw new Error("Course name cannot be empty.");
		if (this.len(c) > this.MAX_COURSE) throw new Error("Course name cannot exceed 30 characters.");
		if (this.len(t) === 0) throw new Error("Assignment title cannot be empty.");
		if (this.len(t) > this.MAX_TITLE) throw new Error("Assignment title cannot exceed 80 characters.");
		const dup = list.some(a =>
			a.course.toLowerCase() === c.toLowerCase() &&
			a.title.toLowerCase() === t.toLowerCase());
		if (dup) throw new Error("This assignment already exists in this course.");
		return { course: c, title: t };
	},

	// core logic – pure: returns a NEW list, never mutates the old one
	addTo(list, course, title) {
		const item = this.validate(course, title, list);
		return [...list, item];
	},

	// user-facing output – wired to Button "btn_add" onClick
	async add() {
		const list = appsmith.store.assignments || [];
		try {
			const updated = this.addTo(list, inp_course.text, inp_title.text);
			await storeValue("assignments", updated, false); // session only, like Python's in-memory list
			await storeValue("message", this.SUCCESS, false);
			await storeValue("isError", false, false);
			showAlert(this.SUCCESS, "success");
			resetWidget("inp_course");
			resetWidget("inp_title");
		} catch (e) {
			await storeValue("message", "ERROR: " + e.message, false);
			await storeValue("isError", true, false);
			showAlert(e.message, "error");
		}
	},

	// helper buttons
	async clearAll() {
		await storeValue("assignments", [], false);
		await storeValue("message", "", false);
	},

	async loadSample() {
		let list = [];
		for (const [c, t] of [["Software Engineering", "Assignment 06"],
		                      ["Mathematics", "Homework 01"],
		                      ["Computer Architecture", "Lecture Notes"]]) {
			list = this.addTo(list, c, t);
		}
		await storeValue("assignments", list, false);
		await storeValue("message", "Sample data loaded (3 assignments).", false);
		await storeValue("isError", false, false);
	}
}
