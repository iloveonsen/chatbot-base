document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const lineHeight = parseFloat(window.getComputedStyle(userInput).lineHeight);
    const maxLines = 5;
    const maxHeight = lineHeight * maxLines;

    userInput.addEventListener('input', function() {
        this.style.height = 'auto'; // Reset height to recalculate
        if (this.scrollHeight <= maxHeight) {
            this.style.height = `${Math.max(this.scrollHeight, lineHeight)}px`;
            this.style.overflowY = 'hidden'; // Hide scrollbar when content is within maxLines
        } else {
            this.style.height = `${maxHeight}px`;
            this.style.overflowY = 'scroll'; // Show scrollbar when content exceeds maxLines
        }
    });
});


const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const chatFormTextArea = chatForm.querySelector('#user-input');

chatForm.addEventListener('submit', function (event) {
    // When the route is index, execute ordinary form submission without js intervention
    const currentUrl = window.location.href;
    if (currentUrl.includes('/index')) {
        return; 
    }

    // Otherwise, prevent the default form submission and proceed with custom logic
    event.preventDefault();

    const userInput = chatFormTextArea.value.trim();
    console.log(userInput);
    chatFormTextArea.value = '';
    if (!userInput) {
        return;
    }

    const userProfileData = document.getElementById('user-profile-data');
    const botProfileData = document.getElementById('bot-profile-data');

    const messageItem = document.createElement('div');
    messageItem.classList.add('message');
    messageItem.innerHTML = `
    <div class="message-profile">
        <img src="${userProfileData.dataset.imageUrl}" alt="">
    </div>
    <div class="message-content">
        <div class="message-profile-name">
            ${userProfileData.dataset.name}
        </div>
        <div class="message-text">
            ${userInput}
        </div>
    </div>
    `;
    chatWindow.appendChild(messageItem);

    
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            "csrfmiddlewaretoken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "message": userInput
        }).toString()
    })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response
            const messageItem = document.createElement('div');
            messageItem.classList.add('message');

            messageItem.innerHTML = `
            <div class="message-profile">
                <img src="${botProfileData.dataset.imageUrl}" alt="">
            </div>
            <div class="message-content">
                <div class="message-profile-name">
                    ${botProfileData.dataset.name}
                </div>
                <div class="message-text">
                    ${botResponse}
                </div>
            </div>
            `;
            chatWindow.appendChild(messageItem);
        });
});
