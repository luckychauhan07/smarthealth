function calcBMI() {
	const weightInput = document.getElementById("w").value;
	const heightInput = document.getElementById("h").value;
	const unitSystem = document.getElementById("unitSystem").value;

	if (!weightInput || !heightInput) {
		document.getElementById("bmiOut").innerText =
			"❌ Please enter both weight and height";
		return;
	}

	const weight = parseFloat(weightInput);
	const height = parseFloat(heightInput);

	if (weight <= 0 || height <= 0) {
		document.getElementById("bmiOut").innerText =
			"❌ Values must be greater than zero";
		return;
	}

	let bmi;
	if (unitSystem === "imperial") {
		// weight in pounds, height in inches
		bmi = (weight / (height * height)) * 703;
	} else {
		// metric: weight in kg, height in cm
		const heightMeters = height / 100;
		bmi = weight / (heightMeters * heightMeters);
	}

	const bmiRounded = bmi.toFixed(2);
	let category = "";
	let emoji = "";

	if (bmi < 18.5) {
		category = "Underweight";
		emoji = "📉";
	} else if (bmi >= 18.5 && bmi < 25) {
		category = "Normal Weight";
		emoji = "✅";
	} else if (bmi >= 25 && bmi < 30) {
		category = "Overweight";
		emoji = "⚠️";
	} else {
		category = "Obese";
		emoji = "🔴";
	}

	const rangeHint = "Healthy range: 18.5 - 24.9";

	document.getElementById("bmiOut").innerHTML = `
		<strong>${emoji} BMI: ${bmiRounded}</strong> (${category})
		<div class="text-[11px] text-muted">${rangeHint}</div>
	`;
}

function calcCalories() {
	const ageInput = document.getElementById("age").value;
	const gender = document.getElementById("gender").value;
	const weightInput = document.getElementById("weightCal").value;
	const heightInput = document.getElementById("heightCal").value;
	const activityInput = document.getElementById("activity").value;

	if (!ageInput || !weightInput || !heightInput || !activityInput) {
		document.getElementById("calorieOut").innerText =
			"❌ Please fill age, weight, height, and activity level";
		return;
	}

	const age = parseFloat(ageInput);
	const weight = parseFloat(weightInput); // kg
	const height = parseFloat(heightInput); // cm
	const activity = parseFloat(activityInput);

	if (age <= 0 || weight <= 0 || height <= 0 || activity <= 0) {
		document.getElementById("calorieOut").innerText =
			"❌ Values must be greater than zero";
		return;
	}

	// Mifflin-St Jeor Equation (metric)
	const s = gender === "male" ? 5 : -161;
	const bmr = 10 * weight + 6.25 * height - 5 * age + s;
	const tdee = Math.round(bmr * activity);

	document.getElementById("calorieOut").innerHTML = `
		<strong>🔥 Daily Calories: ${tdee} kcal</strong>
		<div class="text-[11px] text-muted">BMR ${Math.round(bmr)} kcal using Mifflin-St Jeor × activity factor</div>
	`;
}

function calcHydration() {
	const weightInput = document.getElementById("weightHyd").value;
	const activityInput = document.getElementById("activityHyd").value;

	if (!weightInput) {
		document.getElementById("hydrationOut").innerText =
			"❌ Please enter your weight";
		return;
	}

	const weight = parseFloat(weightInput);
	const activityMins = activityInput ? parseFloat(activityInput) : 0;

	if (weight <= 0 || activityMins < 0) {
		document.getElementById("hydrationOut").innerText =
			"❌ Values must be positive";
		return;
	}

	const baseLiters = weight * 0.033; // 33ml per kg
	const extraLiters = activityMins > 0 ? (activityMins / 30) * 0.35 : 0; // 350ml per 30 mins
	const totalLiters = (baseLiters + extraLiters).toFixed(2);

	const detail = activityMins
		? `Base ${baseLiters.toFixed(2)}L + Activity ${extraLiters.toFixed(2)}L`
		: `Base ${baseLiters.toFixed(2)}L`;

	document.getElementById("hydrationOut").innerHTML = `
		<strong>💧 Daily Water: ${totalLiters} L</strong>
		<div class="text-[11px] text-muted">${detail}</div>
	`;
}
