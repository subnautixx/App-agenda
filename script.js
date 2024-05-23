document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('[data-collapse-toggle="mobile-menu"]');
    const menu = document.querySelector('#mobile-menu');
    toggleButton.addEventListener('click', () => {
        if (menu.classList.contains('hidden')) {
            menu.classList.remove('hidden');
        } else {
            menu.classList.add('hidden');
        }
    });
    fetch('/events')
        .then(response => response.json())
        .then(data => {
            const eventsList = document.getElementById('events_list');
            data.forEach(event => {
                const eventItem = document.createElement('div');
                eventItem.className = 'bg-white p-4 rounded-lg shadow-lg mb-4';
                eventItem.innerHTML = `
                    <h2 class="text-xl font-bold mb-2">${event.event_name}</h2>
                    <p class="text-gray-700">${event.event_date} from ${event.start_time} to ${event.end_time}</p>
                `;
                eventsList.appendChild(eventItem);
            });
        });
});