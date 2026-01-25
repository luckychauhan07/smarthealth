function calculateBMI() {
	let w = document.getElementById("weight").value;
	let h = document.getElementById("height").value;
	let bmi = (w / (h * h)).toFixed(2);
	document.getElementById("bmiResult").innerText = "Your BMI: " + bmi;
}

function nextStep() {
	document.getElementById("step2").classList.remove("hidden");
}
