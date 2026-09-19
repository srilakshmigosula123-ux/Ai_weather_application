const form = document.querySelector('#weather-form');
const cityInput = document.querySelector('#city');
const button = form.querySelector('button');
const message = document.querySelector('#message');
const card = document.querySelector('#weather-card');

function setText(selector, value) {
  document.querySelector(selector).textContent = value;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();

  if (!city) {
    message.textContent = 'Please enter a city name.';
    cityInput.focus();
    return;
  }

  message.textContent = '';
  button.disabled = true;
  button.textContent = 'Checking...';

  try {
    const response = await fetch('/api/weather', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ city }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Unable to fetch weather.');
    }

    setText('#location', `${data.city}${data.country ? `, ${data.country}` : ''}`);
    setText('#condition', data.condition);
    setText('#temperature', data.temperature);
    setText('#feels-like', `Feels like ${data.feels_like}\u00B0C`);
    setText('#humidity', `${data.humidity}%`);
    setText('#wind', `${data.wind_speed} km/h`);
    setText('#explanation', data.explanation);

    const icon = document.querySelector('#weather-icon');
    icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    icon.alt = data.condition;
    card.hidden = false;
  } catch (error) {
    card.hidden = true;
    message.textContent = error.message || 'Unable to fetch weather.';
  } finally {
    button.disabled = false;
    button.textContent = 'Check weather';
  }
});
