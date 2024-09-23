function updateAnalogClock() {
    const hourHand = document.querySelector('.hour-hand');
    const minuteHand = document.querySelector('.minute-hand');
    const secondHand = document.querySelector('.second-hand');

    const now = new Date();
    const seconds = now.getSeconds();
    const minutes = now.getMinutes();
    const hours = now.getHours();

    const secondDeg = ((seconds / 60) * 360) + 90; // 90 degrees offset
    const minuteDeg = ((minutes / 60) * 360) + ((seconds / 60) * 6) + 90; // +90 degrees offset
    const hourDeg = ((hours / 12) * 360) + ((minutes / 60) * 30) + 90; // +90 degrees offset

    secondHand.style.transform = `translateX(-50%) rotate(${secondDeg}deg)`;
    minuteHand.style.transform = `translateX(-50%) rotate(${minuteDeg}deg)`;
    hourHand.style.transform = `translateX(-50%) rotate(${hourDeg}deg)`;
}

function updateDigitalClock() {
    const now = new Date();
    const digitalClock = document.getElementById('digital-clock');
    digitalClock.innerText = now.toLocaleTimeString();
}

// Update clocks every second
setInterval(() => {
    updateAnalogClock();
    updateDigitalClock();
}, 1000);

// Initial calls
updateAnalogClock();
updateDigitalClock();
