// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Пример: Добавление обработчика клика для кнопки "Send Message"
    const sendMessageButton = document.querySelector('.message-form button');
    if (sendMessageButton) {
        sendMessageButton.addEventListener('click', function(event) {
            // Логика для обработки отправки сообщения
            console.log('Send Message button clicked');
        });
    }

    // Пример: Автоматическая прокрутка истории сообщений
    const messageHistory = document.querySelector('.message-history');
    if (messageHistory) {
        messageHistory.scrollTop = messageHistory.scrollHeight;
    }

    // Пример: Применение стилей при наведении на элемент
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        message.addEventListener('mouseover', function() {
            message.style.backgroundColor = '#f0f0f0';
        });
        message.addEventListener('mouseout', function() {
            message.style.backgroundColor = '';
        });
    });
});
